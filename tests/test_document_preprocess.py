import importlib.util
import sys
import types
from unittest.mock import MagicMock, patch

from langchain_core.documents import Document


def _ensure_optional_native_drivers_for_import():
    """Provide lightweight stubs only when native optional drivers (neo4j/spacy) are absent in local venv."""
    if importlib.util.find_spec("neo4j") is None and "neo4j" not in sys.modules:
        neo4j_stub = types.ModuleType("neo4j")
        neo4j_stub.GraphDatabase = MagicMock()
        sys.modules["neo4j"] = neo4j_stub

    if importlib.util.find_spec("spacy") is None and "spacy" not in sys.modules:
        spacy_stub = types.ModuleType("spacy")
        spacy_stub.Language = MagicMock()
        sys.modules["spacy"] = spacy_stub


_ensure_optional_native_drivers_for_import()

# Prevent circular logger initialization during test module import
_mock_logger = MagicMock()
_mock_logging_util = types.ModuleType("utils.logging_util")
_mock_logging_util.logger = _mock_logger
_mock_logging_util.configure_logger = MagicMock(return_value=_mock_logger)
sys.modules.setdefault("utils.logging_util", _mock_logging_util)

_mock_logger_init = types.ModuleType("utils.logger_init")
_mock_logger_init.logger = _mock_logger
sys.modules.setdefault("utils.logger_init", _mock_logger_init)

from config.common_settings import CommonConfig  # noqa: E402
from preprocess.loader.docx_loader import DocxDocLoader  # noqa: E402
from preprocess.loader.loader_factories import DocumentLoaderFactory  # noqa: E402
from preprocess.loader.pdf_loader import PDFDocLoader  # noqa: E402
from preprocess.loader.text_loader import TextDocLoader  # noqa: E402


SAMPLE_APP_CONFIG = {
    "app": {
        "embedding": {
            "input_path": "/tmp/input",
            "staging_path": "/tmp/staging",
            "archive_path": "/tmp/archive",
            "trunk_size": 120,
            "overlap": 20,
            "vector_store": {"enabled": False, "collection_name": "test_docs"},
            "graph_store": {"enabled": False},
        },
        "models": {
            "embedding": {
                "type": "huggingface",
                "model": "sentence-transformers/all-mpnet-base-v2",
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


def test_common_config_embedding_model_factory():
    """Exercise CommonConfig._get_embedding_model() with mocked HuggingFace network/model boundary."""
    with patch.object(CommonConfig, "load_yaml_file", return_value=SAMPLE_APP_CONFIG), \
         patch("config.common_settings.os.path.exists", return_value=True), \
         patch("config.common_settings.dotenv.load_dotenv"), \
         patch("langchain_huggingface.HuggingFaceEmbeddings") as mock_hf_cls:
        mock_instance = MagicMock()
        mock_hf_cls.return_value = mock_instance

        cfg = CommonConfig()
        embedder = cfg._get_embedding_model()

        assert embedder is mock_instance
        mock_hf_cls.assert_called_once_with(model_name="sentence-transformers/all-mpnet-base-v2")


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
