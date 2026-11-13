"""Integration and smoke tests for full application startup and module imports."""
from unittest.mock import MagicMock, patch

from langchain_qdrant import QdrantVectorStore
from config.common_settings import CommonConfig
import preprocess.doc_embedding_job
import preprocess.store.vector_store_helper
import app


def test_app_and_job_modules_import():
    """Verify application entry point and document embedding job import cleanly."""
    assert app.app is not None
    assert preprocess.doc_embedding_job.DocEmbeddingJob is not None
    assert preprocess.store.vector_store_helper.VectorStoreHelper is not None


def test_vector_store_helper_without_langchain_postgres(monkeypatch):
    """Verify VectorStoreHelper.remove_existing_embeddings functions cleanly without langchain_postgres."""
    import sys
    monkeypatch.setitem(sys.modules, "langchain_postgres", None)

    # 1. QdrantVectorStore executes delete without referencing langchain_postgres
    mock_store = MagicMock(spec=QdrantVectorStore)
    mock_point = MagicMock(id="pt-1")
    mock_store.client.scroll.return_value = ([mock_point], None)
    mock_store.collection_name = "test_collection"

    helper = preprocess.store.vector_store_helper.VectorStoreHelper(mock_store)
    helper.remove_existing_embeddings("source.pdf", "pdf", "chk-123")
    mock_store.client.delete.assert_called_once_with(
        collection_name="test_collection",
        points_selector=["pt-1"]
    )

    # 2. PGVector duck-typed store executes safely without AttributeError on self.embeddings
    mock_pg = MagicMock()
    mock_pg.__class__.__name__ = "PGVector"
    mock_doc = MagicMock()
    mock_doc.metadata = {"id": "doc-pg-1"}
    mock_pg.similarity_search_by_vector.return_value = [mock_doc]

    mock_embeddings = MagicMock()
    mock_embeddings.dimension = 768
    pg_helper = preprocess.store.vector_store_helper.VectorStoreHelper(mock_pg, mock_embeddings)
    pg_helper.remove_existing_embeddings("source.pdf", "pdf", "chk-123")
    mock_pg.delete.assert_called_once_with(["doc-pg-1"])
