import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import Config

class PDFLoader:
    """Loads and processes PDF documents for RAG."""
    
    def __init__(self):
        self.config = Config()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " ", ""],
            length_function=len,
        )
    
    def load_pdf(self, pdf_folder: str = None, limit: int = None) -> List[Document]:
        """Load all PDFs from the data/agriculture_data/ folder."""
        if pdf_folder is None:
            pdf_folder = self.config.PDF_DIR
        
        if not os.path.exists(pdf_folder):
            raise FileNotFoundError(f"PDF folder not found: {pdf_folder}")
        
        pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
        
        if not pdf_files:
            raise ValueError(f"No PDF files found in {pdf_folder}")
        
        print(f"📄 Found {len(pdf_files)} PDF files")
        
        documents = []
        for i, filename in enumerate(pdf_files):
            if limit is not None and i >= limit:
                break
                
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"   Loading: {filename}")
            
            try:
                loader = PyPDFLoader(pdf_path)
                pages = loader.load()
                for page in pages:
                    page.metadata['source'] = filename
                documents.extend(pages)
                print(f"   ✅ Loaded {len(pages)} pages")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print(f"✅ Loaded {len(documents)} pages total")
        return documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into smaller chunks."""
        chunks = self.text_splitter.split_documents(documents)
        print(f"✅ Created {len(chunks)} chunks")
        return chunks
