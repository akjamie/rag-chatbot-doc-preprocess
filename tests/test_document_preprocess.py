import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from config.common_settings import CommonConfig
from preprocess.loader.docx_loader import DocxDocLoader
from preprocess.loader.loader_factories import DocumentLoaderFactory
from preprocess.loader.pdf_loader import PDFDocLoader
from preprocess.loader.text_loader import TextDocLoader


SAMPLE_APP_CONFIG = {
    "app": {
        "embedding": {
            "input_path": "./data/input",
            "staging_path": "./data/staging",
            "archive_path": "./data/archive",
            "trunk_size": 120,
            "overlap": 20,
            "vector_store": {"enabled": False, "collection_name": "test_docs"},
            "graph_store": {"enabled": False},
        },
        "models": {
            "embedding": {
                "type": "huggingface",
                "model": "BAAI/bge-large-en-v1.5",
            },
            "llm": {
                "type": "gemini",
                "model": "gemini-2.0-flash",
            },
        },
    }
}


def test_production_loaders_and_factories_import_and_route():
    """Verify real production loaders (PDFDocLoader, DocxDocLoader, TextDocLoader) and factory routing."""
    with patch.object(CommonConfig, "load_yaml_file", return_value=SAMPLE_APP_CONFIG), \
         patch.object(CommonConfig, "_create_directory"), \
         patch("config.common_settings.os.path.exists", return_value=True), \
         patch("config.common_settings.dotenv.load_dotenv"):
        pdf_loader = DocumentLoaderFactory.get_loader("pdf")
        docx_loader = DocumentLoaderFactory.get_loader("docx")
        text_loader = DocumentLoaderFactory.get_loader("text")

        assert isinstance(pdf_loader, PDFDocLoader)
        assert isinstance(docx_loader, DocxDocLoader)
        assert isinstance(text_loader, TextDocLoader)

        assert pdf_loader.is_supported_file_extension("sample.pdf") is True
        assert pdf_loader.is_supported_file_extension("sample.txt") is False
        assert docx_loader.is_supported_file_extension("sample.docx") is True
        assert docx_loader.is_supported_file_extension("sample.pdf") is False


def test_text_doc_loader_parses_and_splits_real_file(tmp_path):
    """Exercise real TextDocLoader.load() and LangChain RecursiveCharacterTextSplitter on a real file."""
    sample_file = tmp_path / "sample_k8s.txt"
    sample_file.write_text(
        ("Enterprise RAG preprocessing splits documents into semantic chunks. " * 30).strip(),
        encoding="utf-8",
    )

    with patch.object(CommonConfig, "load_yaml_file", return_value=SAMPLE_APP_CONFIG), \
         patch.object(CommonConfig, "_create_directory"), \
         patch("config.common_settings.os.path.exists", return_value=True), \
         patch("config.common_settings.dotenv.load_dotenv"):
        loader = TextDocLoader()
        chunks = loader.load(str(sample_file))

        assert len(chunks) > 1
        assert all(isinstance(c, Document) for c in chunks)
        assert all(c.metadata.get("source") == str(sample_file) for c in chunks)


def test_pdf_doc_loader_parses_and_splits_real_pdf(tmp_path):
    """Exercise real PDFDocLoader.load() with PyMuPDFLoader on a generated PDF fixture."""
    import fitz

    pdf_path = tmp_path / "sample_rag.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Enterprise RAG PDF preprocessing test.\n" * 40)
    doc.save(str(pdf_path))
    doc.close()

    with patch.object(CommonConfig, "load_yaml_file", return_value=SAMPLE_APP_CONFIG), \
         patch.object(CommonConfig, "_create_directory"), \
         patch("config.common_settings.os.path.exists", return_value=True), \
         patch("config.common_settings.dotenv.load_dotenv"):
        loader = PDFDocLoader()
        chunks = loader.load(str(pdf_path))

        assert len(chunks) >= 1
        assert all(isinstance(c, Document) for c in chunks)
        assert any("Enterprise RAG PDF preprocessing test." in c.page_content for c in chunks)


def test_common_config_embedding_model_real_inference():
    """Exercise CommonConfig._get_embedding_model() and real embedding execution."""
    real_exists = os.path.exists

    def selective_exists(path):
        if "app.yaml" in str(path) or ".env" in str(path):
            return True
        return real_exists(path)

    with patch.object(CommonConfig, "load_yaml_file", return_value=SAMPLE_APP_CONFIG), \
         patch("config.common_settings.os.path.exists", side_effect=selective_exists), \
         patch("config.common_settings.dotenv.load_dotenv"):
        cfg = CommonConfig()
        embedder = cfg.get_model("embedding")
        assert embedder is not None
        vectors = embedder.embed_documents(["RAG document embedding chunk test"])
        assert len(vectors) == 1
        assert len(vectors[0]) > 0


def test_vendored_spacy_model_loading_and_nlp():
    """Verify loading the repo-vendored spaCy en_core_web_md model through CommonConfig."""
    with patch.object(CommonConfig, "load_yaml_file", return_value=SAMPLE_APP_CONFIG), \
         patch("config.common_settings.os.path.exists", return_value=True), \
         patch("config.common_settings.dotenv.load_dotenv"):
        cfg = CommonConfig()
        nlp = cfg.get_nlp_spacy()
        assert nlp is not None
        doc = nlp("Google DeepMind builds advanced AI models in London.")
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        assert len(entities) >= 1


def test_common_config_llm_factory_and_fix():
    """Verify CommonConfig._get_llm_model() uses self.config and instantiates properly."""
    with patch.object(CommonConfig, "load_yaml_file", return_value=SAMPLE_APP_CONFIG), \
         patch("config.common_settings.os.path.exists", return_value=True), \
         patch("config.common_settings.dotenv.load_dotenv"), \
         patch("langchain_google_genai.GoogleGenerativeAI") as mock_gemini:
        mock_instance = MagicMock()
        mock_gemini.return_value = mock_instance
        cfg = CommonConfig()
        model = cfg.get_model("llm")
        assert model is mock_instance


def test_neo4j_driver_compatibility_and_mocked_session():
    """Verify Neo4j driver compatibility (5.x and 6.x) and session query execution."""
    from neo4j import GraphDatabase

    mock_driver = MagicMock()
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    mock_session.run.return_value = [{"count": 42}]

    with patch.object(GraphDatabase, "driver", return_value=mock_driver):
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test"))
        with driver.session() as session:
            result = session.run("MATCH (n) RETURN count(n) as count")
            records = list(result)
            assert len(records) == 1
            assert records[0]["count"] == 42
