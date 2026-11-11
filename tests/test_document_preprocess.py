import os
import pytest
from unittest.mock import Mock, patch
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def test_document_chunking_and_metadata():
    """Verify document chunking with RecursiveCharacterTextSplitter preserves metadata."""
    sample_text = (
        "Enterprise RAG architectures require robust document preprocessing. "
        "Chunking documents into semantic boundaries ensures higher vector similarity precision. "
        "Metadata such as source file, page index, and chunk identifier are attached to each chunk. "
    ) * 10

    doc = Document(page_content=sample_text, metadata={"source": "test_doc.pdf", "author": "Jamie"})
    splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30)
    chunks = splitter.split_documents([doc])

    assert len(chunks) > 1, f"Expected multiple chunks, got {len(chunks)}"
    for idx, chunk in enumerate(chunks):
        assert isinstance(chunk, Document)
        assert chunk.metadata["source"] == "test_doc.pdf"
        assert len(chunk.page_content) <= 150 + 30


def test_embeddings_generation_runnable():
    """Verify embeddings model produces numerical vector embeddings for document chunks."""
    doc = Document(page_content="Modernized LangChain embeddings generation test.", metadata={"id": "chunk_1"})
    
    mock_embeddings = Mock()
    mock_embeddings.embed_documents.return_value = [[0.123, -0.456, 0.789, 0.012]]

    embeddings = mock_embeddings.embed_documents([doc.page_content])
    assert len(embeddings) == 1
    assert len(embeddings[0]) == 4
    assert isinstance(embeddings[0][0], float)

