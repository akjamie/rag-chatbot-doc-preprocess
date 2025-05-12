import json
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveJsonSplitter

from .base_loader import BaseLoader


class KnowledgeSnippetLoader(BaseLoader):
    def load(self, source: str) -> List[Document]:
        """Load knowledge snippet from JSON source"""
        try:
            # Parse the JSON source
            snippet_data = json.loads(source)
            
            # Create document with metadata
            doc = Document(
                page_content=snippet_data['content'],
                metadata={
                    'title': snippet_data.get('title', 'Untitled Snippet'),
                    'created_at': snippet_data.get('created_at'),
                    'type': 'knowledge_snippet'
                }
            )
            
            return [doc]
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid knowledge snippet JSON: {str(e)}")

    def get_splitter_for_child(self):
        return RecursiveJsonSplitter(max_chunk_size=self.get_trunk_size() / 4, min_chunk_size=self.get_overlap() / 4)
