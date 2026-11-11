# Capability: Document Preprocessing Modernization

## Purpose
Modernize the document preprocessing pipeline dependencies to LangChain 1.4.9, modern PyMuPDF, spaCy, and Neo4j drivers to ensure consistent chunking, embedding, and vector indexing.

## ADDED Requirements

### Requirement: Modernize Preprocessing Dependencies
The document preprocessing service dependencies in `requirements.txt` SHALL specify LangChain 1.4.9, LangChain-Core 1.7.6, and compatible parsing libraries.

#### Scenario: Install and resolve updated preprocessing requirements
- **GIVEN** a Python 3.10+ execution environment
- **WHEN** dependencies in `requirements.txt` are resolved
- **THEN** `langchain` 1.4.9, `langchain-core` 1.7.6, `pymupdf>=1.25.0`, and `neo4j>=5.26.0` install without resolution conflicts.

**Acceptance criteria**
- [ ] AC1: `requirements.txt` locks compatible LangChain 1.4.9 and ingestion dependencies (test: tests/test_dependencies.py)

### Requirement: Document Parsing and Embedding Generation
The preprocessing pipeline MUST successfully parse PDF documents and produce embeddings using modern LangChain embeddings models.

#### Scenario: Extract text and embed sample document
- **GIVEN** a valid staging document (PDF or DOCX)
- **WHEN** the preprocessing service executes parsing and chunking
- **THEN** document chunks and embeddings are generated and stored without runtime exceptions.

**Acceptance criteria**
- [ ] AC2: Document parser and embeddings run successfully on test document (test: tests/test_document_preprocess.py)

## Constraints & NFRs
- Parsing memory footprint must remain bounded during large document indexing.

## Out of Scope
- Modifying OCR extraction engines for scanned non-searchable image documents.

## Test Strategy
Automated tests using pytest to verify document loading, text extraction, chunking splitting accuracy, and embedding generation across test PDF fixtures.

