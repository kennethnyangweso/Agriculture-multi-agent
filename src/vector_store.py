import os
from typing import List, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from config import Config

class VectorStore:
    """Handles the creation and management of a vector store for RAG."""

    def __init__(self):
        self.config = Config()
        print("Loading embedding model...")
        print(f"Model: {self.config.EMBEDDING_MODEL}")

        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.config.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}

        )
        print ("Embedding model loaded successfully.")

        self.vector_store: Optional[Chroma] = None  

    def create(self, documents: List[Document]) -> Chroma:
            """Create a new vector store from the documents"""
        os.makedirs(self.config.VECTOR_STORE_DIR, exist_ok=True)

        print("Creating vector store...")
        print(f"Processing {len(documents)} chunks...")
    
        self.vector_store = Chroma.from_documents(
              documents=documents,
              embedding=self.embeddings,
              persist_directory=self.config.VECTOR_STORE_DIR

        )
    
        self.vector_store.persist()
    
        print(f"Vector store created and persisted at {self.vector_store._collection.count()} vectors")
        return self.vector_store

    def load(self) -> Chroma:
          
        """Load an existing vector store"""

        if not os.path.exists(self.config.VECTOR_STORE_DIR):
            raise FileNotFoundError(f"Vector store directory does not exist: {self.config.VECTOR_STORE_DIR}")

        print("Loading vector store...")
        self.vector_store = Chroma(
            persist_directory=self.config.VECTOR_STORE_DIR,
            embedding_function=self.embeddings
        )
        print(f"Vector store loaded with {self.vector_store._collection.count()} vectors")
        return self.vector_store
    
    def load(self) -> Chroma:
        """Load an existing vector store"""
        if not os.path.exists(self.config.VECTOR_STORE_DIR):
            raise FileNotFoundError(f"Vector store directory does not exist: {self.config.VECTOR_STORE_DIR}")

        print("Loading vector store...")
        self.vector_store = Chroma(
            persist_directory=self.config.VECTOR_STORE_DIR,
            embedding_function=self.embeddings
        )
        print(f"Vector store loaded with {self.vector_store._collection.count()} vectors")
        return self.vector_store
    
    def retrieve(self, query : str, k: int = None) -> List[Document]:
        """Retrieve relevant documents from the vector store based on a query."""
        if self.vector_store is None:
            raise ValueError("Vector store is not loaded. Please load or create the vector store first.")

        if k is None:
            k = self.config.RETRIEVAL_K

        return self.vector_store.similarity_search(query, k=k)
    
    def retrieve_with_score(self, query: str, k: int = None) -> List[tuple]:
        """Retrieve relevant documents along with their similarity scores."""
        if self.vector_store is None:
            raise ValueError("Vector store is not loaded. Please load or create the vector store first.")

        if k is None:
            k = self.config.RETRIEVAL_K

        return self.vector_store.similarity_search_with_score(query, k=k)


       