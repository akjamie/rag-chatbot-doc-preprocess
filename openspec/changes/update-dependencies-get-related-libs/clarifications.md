# Clarifications: update-dependencies-get-related-libs

> Requirement: "update the dependencies to get related libs/models to be updated and get it running,"
> Mode: interactive (grill-me)

## Requirement
"update the dependencies to get related libs/models to be updated and get it running,"

## Settled decisions
- **LangChain & Core Alignment**: Modernize `requirements.txt` to align with the core backend on LangChain `1.4.9`, `langchain-core 1.7.6`, `langchain-community 0.4.2`, and `langchain-huggingface 1.2.3`.
- **Document Ingestion & Preprocessing Tools**: Modernize `pymupdf` (`>=1.25.0`), `spacy` (`>=3.8.4`), `neo4j` (`>=5.26.0`), and `fastapi`/`uvicorn` runtime tools.
- **Workflow & Graph Integration**: Maintain document preprocessing pipelines and ensure embeddings and vector store ingestion execute cleanly with updated LangChain runnables.

## Open questions
<!-- None. All questions settled. -->
