# Tasks: update-dependencies-get-related-libs

## 1. Dependency Modernization
- [x] 1.1 [TEST] Add test verifying LangChain 1.4.9, LangGraph 1.2.20, partner packages, capped driver bounds, and installed package metadata (`tests/test_dependencies.py`)
  - verify: `pytest --noconftest tests/test_dependencies.py` -> PASS (2 passed)
- [x] 1.2 [IMPL] Update `requirements.txt` with LangChain 1.4.9, langchain-core 1.7.6, langgraph 1.2.20, `langchain-redis==0.2.6`, `requests>=2.32.5`, capped drivers (`pymupdf>=1.25.0,<3`, `neo4j>=5.26.0,<7`, `spacy>=3.8.4,<4`), and direct dependencies (`langchain-text-splitters`, `pydantic`, `qdrant-client`)
  - evidence: `python -m pytest --noconftest tests/test_dependencies.py` -> PASS (2 passed in 0.09s)

## 2. Ingestion & Preprocessing Pipeline Verification
- [x] 2.1 [TEST] Add integration test exercising real `CommonConfig`, `DocumentLoaderFactory`, `PDFDocLoader` (real PDF fixture), `DocxDocLoader`, `TextDocLoader`, real HuggingFace embedding inference, vendored spaCy NLP pipeline, and Neo4j driver compatibility (`tests/test_document_preprocess.py`)
  - verify: `python -m pytest --noconftest tests/test_document_preprocess.py` -> PASS (7 passed in 33.09s)
- [x] 2.2 [IMPL] Fix `pyproject.toml` (`[project] requires-python = ">=3.11"`, `pythonpath = ["."]`), fix `pathlib.Path` and `_get_llm_model` in `config/common_settings.py`, make PGVector import lazy in `preprocess/store/vector_store_helper.py`, and update `.github/workflows/ci.yml` with `pip check` and `timeout-minutes: 15`
  - evidence: `python -m pytest --noconftest tests/test_smoke.py` -> PASS (2 passed in 10.08s)
- [x] 2.3 [TEST] Add full smoke test suite asserting `app.py`, `DocEmbeddingJob`, and `VectorStoreHelper` import and initialize cleanly (`tests/test_smoke.py`)
  - evidence: `python -m pytest --noconftest tests/test_dependencies.py tests/test_document_preprocess.py tests/test_smoke.py` -> PASS (11 passed in 38.97s)
