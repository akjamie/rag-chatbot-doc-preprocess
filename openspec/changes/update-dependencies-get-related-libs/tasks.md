# Tasks: update-dependencies-get-related-libs

## 1. Dependency Modernization
- [x] 1.1 [TEST] Add test verifying LangChain 1.4.9 and core dependencies specification (`tests/test_dependencies.py`)
  - verify: `pytest --noconftest tests/test_dependencies.py` -> FAILED (AssertionError: Expected langchain==1.4.9, got ==0.3.7)
- [x] 1.2 [IMPL] Update `requirements.txt` with LangChain 1.4.9, langchain-core 1.7.6, and modern libraries
  - evidence: `pytest --noconftest tests/test_dependencies.py` -> PASS (1 passed in 0.03s)

## 2. Ingestion & Preprocessing Pipeline Verification
- [x] 2.1 [TEST] Add integration test for document parsing, chunking, and embeddings generation (`tests/test_document_preprocess.py`)
  - verify: `pytest --noconftest tests/test_document_preprocess.py` -> PASS (2 passed)
- [x] 2.2 [IMPL] Ensure preprocessing loaders, chunkers, and embedding extractors execute cleanly with LangChain 1.4.x runnables
  - evidence: `pytest --noconftest tests/test_dependencies.py tests/test_document_preprocess.py` -> PASS (3 passed in 2.19s)
