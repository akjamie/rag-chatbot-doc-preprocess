# Technical Design: Document Preprocessing Modernization

## Architecture & Component Interaction
The preprocessing engine handles incoming documents, converts them to chunks, generates embeddings, and writes graph entities:

```mermaid
flowchart TD
    DocInput[Document Input: PDF / Word / Text] --> PyMuPDF[PyMuPDF / docx2txt Parsers]
    PyMuPDF --> Chunker[Semantic Chunker / spaCy 3.8]
    Chunker --> Embedder[LangChain 1.4 HuggingFace / GenAI Embeddings]
    Embedder --> VectorStore[Qdrant Vector Store]
    Chunker --> GraphExtractor[Entity Extractor]
    GraphExtractor --> Neo4jStore[Neo4j 5.26 Graph Store]
```

## Interface Contracts & Schemas
Documents are transformed into standard `Document` objects with metadata:
- `page_content`: string
- `metadata`: `{ source, page, chunk_id, hash }`

## External API Integration & Resilience
- **LangChain Embeddings**: Batch embedding generation with rate limit handling and retry logic.
- **Neo4j Driver**: Connection pooling and transactional chunk writes.

## Security & Operational NFRs
- Sanitization of uploaded file paths and extensions.
- Processing throughput target: >= 20 pages per second for text extraction.

