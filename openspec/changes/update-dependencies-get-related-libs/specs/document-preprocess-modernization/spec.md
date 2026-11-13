# Capability: Document Preprocessing Modernization

## Purpose
Modernize the document preprocessing pipeline dependencies to LangChain 1.4.9, capped PyMuPDF (<3), spaCy (<4), and Neo4j (<7) drivers to ensure consistent chunking, embedding, and vector indexing.

## ADDED Requirements

### Requirement: Modernize Preprocessing Dependencies
The document preprocessing service dependencies in `requirements.txt` SHALL specify LangChain 1.4.9, LangChain-Core 1.7.6, and compatible capped parsing and driver libraries (`pymupdf>=1.25.0,<3`, `neo4j>=5.26.0,<7`, `spacy>=3.8.4,<4`).

#### Scenario: Install and resolve updated preprocessing requirements
- **GIVEN** a Python >=3.11 execution environment
- **WHEN** dependencies in `requirements.txt` are resolved
- **THEN** `langchain` 1.4.9, `langchain-core` 1.7.6, `pymupdf>=1.25.0,<3`, and `neo4j>=5.26.0,<7` install without resolution conflicts and pass `pip check`.

**Acceptance criteria**
- [x] AC1: `requirements.txt` locks compatible LangChain 1.4.9 and ingestion dependencies, and installed packages satisfy bounded versions (test: tests/test_dependencies.py)

### Requirement: Document Parsing and Embedding Generation
The preprocessing pipeline MUST successfully parse PDF documents, generate embeddings, load vendored spaCy NLP pipeline, and import the application entry point cleanly without missing driver errors.

#### Scenario: Extract text, embed sample document, and verify app startup
- **GIVEN** a valid staging document (PDF, DOCX, or text)
- **WHEN** the preprocessing service executes parsing, chunking, and embedding generation
- **THEN** document chunks and embeddings are generated without runtime exceptions, and application modules (`app.py`, `DocEmbeddingJob`, `VectorStoreHelper`) import cleanly.

**Acceptance criteria**
- [x] AC2: Document parser and embeddings run successfully on test document with real embeddings generation, vendored spaCy NLP loading, and Neo4j session compatibility (test: tests/test_document_preprocess.py)
- [x] AC3: Application entrypoint (`app.py`), embedding job (`DocEmbeddingJob`), and `VectorStoreHelper` import cleanly without hard dependency on unpinned vector stores (test: tests/test_smoke.py)

## Constraints & NFRs
- Parsing memory footprint must remain bounded during large document indexing.
- Runtime Python environment SHALL be `>=3.11` (matches `datetime.UTC` and CI).

## Out of Scope
- Modifying OCR extraction engines for scanned non-searchable image documents.

## Test Strategy
Automated tests using pytest to verify document loading, text extraction, real embedding generation, spaCy NLP pipeline loading, and application smoke import tests across `tests/test_dependencies.py`, `tests/test_document_preprocess.py`, and `tests/test_smoke.py`.
