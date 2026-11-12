# Tasks: update-dependencies-get-related-libs

## 1. Dependency Modernization
- [x] 1.1 [TEST] Add test verifying LangChain 1.4.9, LangGraph 1.2.20, partner packages, and minimum driver versions (`tests/test_dependencies.py`)
  - verify: `pytest --noconftest tests/test_dependencies.py` -> FAILED (Expected langchain==1.4.9, got ==0.3.7)
- [x] 1.2 [IMPL] Update `requirements.txt` with LangChain 1.4.9, langchain-core 1.7.6, langgraph 1.2.20, `langchain-redis==0.2.6`, `requests>=2.32.5`, `langchain-ollama==1.1.0`, `langchain-anthropic==1.7.6` (and document `langchain-postgres` pending upstream `langchain-core>=1.0`)
  - evidence: `python -m pytest --noconftest tests/test_dependencies.py` -> PASS (1 passed)

## 2. Ingestion & Preprocessing Pipeline Verification
- [x] 2.1 [TEST] Add integration test exercising real `CommonConfig`, `DocumentLoaderFactory`, `PDFDocLoader` (real PDF fixture), `DocxDocLoader`, `TextDocLoader`, and embedding model factory (`tests/test_document_preprocess.py`)
  - verify: `python -m pytest --noconftest tests/test_document_preprocess.py` -> PASS (4 passed)
- [x] 2.2 [IMPL] Fix `pyproject.toml` (`[tool.pytest.ini_options]` `python_files = ["test_*.py"]`), fix `pathlib.Path` import in `config/common_settings.py`, configure portable `python -m pytest` runner, and update `.github/workflows/ci.yml` to run `pip install -r requirements.txt`
  - evidence: `python -m pytest --noconftest tests/test_dependencies.py tests/test_document_preprocess.py` -> PASS (5 passed in 5.73s)
