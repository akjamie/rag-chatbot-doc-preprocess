"""Integration and smoke tests for full application startup and module imports."""
from unittest.mock import MagicMock, patch

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
    """Verify VectorStoreHelper functions cleanly when langchain_postgres is not installed."""
    import sys
    monkeypatch.setitem(sys.modules, "langchain_postgres", None)
    
    mock_store = MagicMock()
    helper = preprocess.store.vector_store_helper.VectorStoreHelper(mock_store)
    assert helper.vector_store is mock_store

