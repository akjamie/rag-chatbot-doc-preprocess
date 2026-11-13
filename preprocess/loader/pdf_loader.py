from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.document_loaders import BaseLoader

from preprocess.loader.base_loader import DocumentLoader


class PDFDocLoader(DocumentLoader):
    def get_loader(self, file_path: str) -> BaseLoader:
        if self.is_supported_file_extension(file_path):
            return PyMuPDFLoader(file_path)


    def is_supported_file_extension(self, file_path: str) -> bool:
        if None != file_path and file_path.endswith(".pdf"):
            return True

        return False
