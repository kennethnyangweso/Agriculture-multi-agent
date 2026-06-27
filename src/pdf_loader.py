import os
from typing import List
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from config import Config

class PDFLoader:
    """Loads and processes PDF documents for the RAG."""


    def __init__(self):
        self.config = Config()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP
            separators = ["\n\n", "\n", " ", ""],
            length_function = len,

        
        )

    def load_pdf(self, pdf_folder: str= None) -> List[Document]:
        """Load and process PDF documents from the specified folder."""
        if pdf_folder is None:
            pdf_folder = self.config.PDF_DIR

        if not os.path.exists(pdf_folder):
            raise FileNotFoundError(f"The specified PDF folder does not exist: {pdf_folder}")
        
        pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

        if not pdf_files:
            raise FileNotFoundError(f"No PDF files found in the specified folder: {pdf_folder}")
        
        print(f"Found {len(pdf_files)} PDF files in {pdf_folder}. Loading and processing...")


        documents = []

        for filename in pdf_files:
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Loading PDF: {pdf_path}")

            try:
                loader = PyPDFLoader(pdf_path)
                pages = loader.load()
                for page in pages:
                    page.metadata["source"] = filename
                documents.extend(pages)
                print(f"loaded {len(pages)}")

            except Exception as e:
                print(f"Error loading {e}")

        print(f"Total documents loaded: {len(documents)}")
        return documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into smaller chunks for RAG."""
        chunks = self.text_splitter.split_documents(documents)
        print(f"Total chunks created: {len(chunks)}")
        return chunks
      