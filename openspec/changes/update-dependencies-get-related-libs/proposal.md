# Proposal: Modernize Document Preprocessing Dependencies (LangChain 1.4.9)

## Why
The document preprocessing service transforms, chunks, and indexes documents into vector and graph databases. Aligning its dependencies with the latest LangChain `1.4.9` and `langchain-core` `1.7.6` ecosystem ensures seamless embedding generation, document transformation, and cross-service data consistency with the main chat service.

## What Changes
- Upgrade `requirements.txt` (exact pins `==` for LangChain ecosystem, minimum bounds `>=` for native/runtime drivers):
  - `langchain==1.4.9`, `langchain-core==1.7.6`, `langchain-community==0.4.2`, `langgraph==1.2.20`
  - `langchain-huggingface==1.2.3`, `langchain-qdrant==1.1.0`, `langchain-google-genai==4.4.3`
  - `langchain-ollama==1.1.0`, `langchain-anthropic==1.7.6`, `langchain-postgres==0.0.12`, `langchain-redis==0.1.1` (uncommented to match active imports in `config/common_settings.py` and `preprocess/doc_index_log_processor.py`)
  - `pymupdf>=1.25.0`, `neo4j>=5.26.0`, `spacy>=3.8.4`, `fastapi==0.115.6`, `uvicorn==0.32.1`
- Fix `config/common_settings.py` to import `Path` from `pathlib` rather than `spacy.vectors`.
- Add integration tests (`tests/test_dependencies.py`, `tests/test_document_preprocess.py`) verifying pinned/minimum dependency constraints and real production `CommonConfig`, `DocumentLoaderFactory`, `PDFDocLoader`, `DocxDocLoader`, and `TextDocLoader` compatibility.
- Add portable `python -m pytest` runner in `openspec/config.yaml` and `.github/workflows/ci.yml`.

## Capabilities
### Unified Document Ingestion Pipeline
- High-efficiency document parsing with modernized PyMuPDF and spaCy.
- Consistent embeddings generation using updated HuggingFace / Google GenAI embeddings.

## Impact
- **Codebase**: `requirements.txt`, `config/common_settings.py`, `tests/test_dependencies.py`, `tests/test_document_preprocess.py`, `.github/workflows/ci.yml`.
- **Tests**: Preprocessing and extraction unit/integration tests.

## Out of Scope
- Changing document storage directory layouts (`data/input`, `data/archive`, `data/staging`).
- Live external database writes to Qdrant/Neo4j during unit CI runs.

## Dependencies & Assumptions
- Python >= 3.10 runtime environment.
- Access to embedding models (local HuggingFace / remote API).
