# Proposal: Modernize Document Preprocessing Dependencies (LangChain 1.4.9)

## Why
The document preprocessing service transforms, chunks, and indexes documents into vector and graph databases. Aligning its dependencies with the latest LangChain `1.4.9` and `langchain-core` `1.7.6` ecosystem ensures seamless embedding generation, document transformation, and cross-service data consistency with the main chat service.

## What Changes
- Upgrade `requirements.txt` (exact pins `==` for LangChain ecosystem, capped bounds `<` for native/runtime drivers):
  - `langchain==1.4.9`, `langchain-core==1.7.6`, `langchain-community==0.4.2`, `langgraph==1.2.20`
  - `langchain-huggingface==1.2.3`, `langchain-qdrant==1.1.0`, `langchain-google-genai==4.4.3`
  - `langchain-ollama==1.1.0`, `langchain-anthropic==1.7.6`, `langchain-redis==0.2.6`
  - Explicitly declare direct imports: `langchain-text-splitters==0.3.6`, `pydantic>=2.9.2`, `qdrant-client>=1.12.0`
  - Capped upper bounds on drivers: `pymupdf>=1.25.0,<3`, `neo4j>=5.26.0,<7`, `spacy>=3.8.4,<4`
  - `fastapi==0.115.6`, `uvicorn==0.32.1`, `requests>=2.32.5`, `python-dotenv==1.0.1`
  - Commented `langchain-postgres` pending upstream `langchain-core>=1.0` support.
- Make PGVector import lazy in `preprocess/store/vector_store_helper.py` to prevent service import failure on unpinned backends.
- Fix undefined `config` variable bug in `config/common_settings.py:58` (`_get_llm_model`).
- Fix `config/common_settings.py` `Path` import from `pathlib` rather than `spacy.vectors`.
- Add integration and smoke tests (`tests/test_dependencies.py`, `tests/test_document_preprocess.py`, `tests/test_smoke.py`) verifying installed package bounds, real HuggingFace embeddings generation, vendored spaCy NLP pipeline, Neo4j driver compatibility, and app startup import sanity.
- Update `.github/workflows/ci.yml` with `pip check`, full test suite execution, and `timeout-minutes: 15`.

## Capabilities
### Unified Document Ingestion Pipeline
- High-efficiency document parsing with modernized PyMuPDF and spaCy.
- Consistent embeddings generation using updated HuggingFace / Google GenAI embeddings.
- Robust startup with lazy vector store imports.

## Impact
- **Codebase**: `requirements.txt`, `config/common_settings.py`, `preprocess/store/vector_store_helper.py`, `pyproject.toml`, `.github/workflows/ci.yml`.
- **Tests**: `tests/test_dependencies.py`, `tests/test_document_preprocess.py`, `tests/test_smoke.py`.

## Out of Scope
- Changing document storage directory layouts (`data/input`, `data/archive`, `data/staging`).
- Live external database writes to Qdrant/Neo4j during unit CI runs.

## Dependencies & Assumptions
- Python >= 3.11 runtime environment (aligned with `datetime.UTC` and CI).
- Access to embedding models (local HuggingFace / remote API).
