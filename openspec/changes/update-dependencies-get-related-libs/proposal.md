# Proposal: Modernize Document Preprocessing Dependencies (LangChain 1.4.9)

## Why
The document preprocessing service transforms, chunks, and indexes documents into vector and graph databases. Aligning its dependencies with the latest LangChain `1.4.9` and `langchain-core` `1.7.6` ecosystem ensures seamless embedding generation, document transformation, and cross-service data consistency with the main chat service.

## What Changes
- Upgrade `requirements.txt`:
  - `langchain==1.4.9`
  - `langchain-core==1.7.6`
  - `langchain-community==0.4.2`
  - `langchain-huggingface==1.2.3`
  - `langchain-qdrant==1.1.0`
  - `langchain-google-genai==4.4.3`
  - `pymupdf>=1.25.0`
  - `neo4j>=5.26.0`
  - `spacy>=3.8.4`
  - `fastapi>=0.115.6`, `uvicorn>=0.32.1`
- Update document chunking and embedding extractors to use modern LangChain 1.4.x runnables and document schema classes.
- Validate ingestion pipeline for PDF, Word, and text documents into Qdrant and Neo4j.

## Capabilities
### Unified Document Ingestion Pipeline
- High-efficiency document parsing with modernized PyMuPDF and spaCy.
- Consistent embeddings generation using updated HuggingFace / Google GenAI embeddings.

## Impact
- **Codebase**: `requirements.txt`, document loaders, preprocessors, ingestion scripts.
- **Data**: Consistent chunk schemas stored in Qdrant and Neo4j.
- **Tests**: Preprocessing and extraction unit/integration tests.

## Out of Scope
- Changing document storage directory layouts (`data/input`, `data/archive`, `data/staging`).

## Dependencies & Assumptions
- Python >= 3.10 runtime environment.
- Access to embedding models (local HuggingFace / remote API).

