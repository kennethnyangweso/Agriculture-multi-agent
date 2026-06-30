import os
from typing import List, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from config import Config

class VectorStore:
    """Manages the vector database for RAG retrieval with query expansion."""
    
    def __init__(self):
        self.config = Config()
        print("🔄 Loading embedding model...")
        print(f"   Model: {self.config.EMBEDDING_MODEL}")
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("   ✅ Model loaded!")
        
        self.vectorstore: Optional[Chroma] = None
        
        # Crop and disease terms for relevance filtering
        self.crop_terms = ['maize', 'corn', 'mahindi', 'bean', 'coffee', 'kahawa', 
                           'sugarcane', 'miwa', 'wheat', 'ngano', 'sweet potato', 
                           'cassava', 'rice', 'tomato', 'onion', 'cabbage']
        
        self.disease_terms = ['lethal necrosis', 'mln', 'rust', 'blight', 'wilt', 
                              'spot', 'canker', 'mosaic', 'rot', 'mildew', 
                              'anthracnose', 'smut', 'streak', 'mottle']
    
    def create(self, documents: List[Document]) -> Chroma:
        """Create a new vector store from documents."""
        os.makedirs(self.config.VECTOR_STORE_DIR, exist_ok=True)
        
        print("🔄 Creating vector store...")
        print(f"   Processing {len(documents)} chunks")
        
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.config.VECTOR_STORE_DIR
        )
        self.vectorstore.persist()
        
        print(f"✅ Vector store created with {self.vectorstore._collection.count()} vectors")
        print(f"   Saved to: {self.config.VECTOR_STORE_DIR}")
        return self.vectorstore
    
    def load(self) -> Chroma:
        """Load an existing vector store."""
        if not os.path.exists(self.config.VECTOR_STORE_DIR):
            raise FileNotFoundError(f"Vector store not found at {self.config.VECTOR_STORE_DIR}")
        
        print("🔄 Loading existing vector store...")
        
        self.vectorstore = Chroma(
            persist_directory=self.config.VECTOR_STORE_DIR,
            embedding_function=self.embeddings
        )
        
        print(f"✅ Vector store loaded with {self.vectorstore._collection.count()} vectors")
        return self.vectorstore
    
    def retrieve(self, query: str, k: int = None) -> List[Document]:
        """Retrieve relevant documents for a query."""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Call create() or load() first.")
        
        if k is None:
            k = self.config.RETRIEVAL_K
        
        return self.vectorstore.similarity_search(query, k=k)
    
    def retrieve_with_expansion(self, query: str, k: int = None) -> List[Document]:
        """Retrieve documents with query expansion for better results."""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized.")
        
        if k is None:
            k = self.config.RETRIEVAL_K
        
        # Expand query with relevant terms
        expanded_query = self._expand_query(query)
        
        if expanded_query != query:
            print(f"🔍 Query expanded: '{query}' → '{expanded_query}'")
        
        # Retrieve with expanded query
        return self.vectorstore.similarity_search(expanded_query, k=k)
    
    def _expand_query(self, query: str) -> str:
        """Expand the query with relevant agricultural terms."""
        query_lower = query.lower()
        
        # Check if query contains any key terms
        expanded = query
        for key, expansion in self.config.QUERY_EXPANSIONS.items():
            if key in query_lower:
                expanded = f"{query} {expansion}"
                break
        
        # Add common agricultural terms if not present
        if 'disease' in query_lower and 'symptom' not in query_lower:
            expanded += " symptoms signs diagnosis"
        
        if 'treat' in query_lower and 'management' not in query_lower:
            expanded += " management treatment control"
        
        if 'how' in query_lower and 'guide' not in query_lower:
            expanded += " guide steps procedure"
        
        if 'pest' in query_lower and 'control' not in query_lower:
            expanded += " control management prevention"
        
        return expanded
    
    def retrieve_relevant(self, query: str, k: int = None, threshold: float = 0.5) -> List[Document]:
        """Retrieve only relevant documents above a similarity threshold."""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized.")
        
        if k is None:
            k = self.config.RETRIEVAL_K
        
        # Get documents with scores
        results = self.vectorstore.similarity_search_with_score(query, k=k * 3)
        
        # Extract key terms from query
        query_lower = query.lower()
        mentioned_crops = [term for term in self.crop_terms if term in query_lower]
        mentioned_diseases = [term for term in self.disease_terms if term in query_lower]
        
        relevant_docs = []
        
        for doc, score in results:
            doc_text = doc.page_content.lower()
            
            # If specific crops/diseases mentioned, prioritize docs containing them
            if mentioned_crops or mentioned_diseases:
                has_mentioned = False
                for term in mentioned_crops + mentioned_diseases:
                    if term in doc_text:
                        has_mentioned = True
                        break
                
                # Accept if it has the mentioned term OR if score is very good
                if has_mentioned and score < threshold * 1.5:
                    relevant_docs.append(doc)
                    if len(relevant_docs) >= k:
                        break
                elif not has_mentioned and score < threshold * 0.5:
                    # Very high relevance even without mentioned term
                    relevant_docs.append(doc)
                    if len(relevant_docs) >= k:
                        break
            else:
                # No specific crop/disease mentioned, use threshold
                if score < threshold:
                    relevant_docs.append(doc)
                    if len(relevant_docs) >= k:
                        break
        
        # If no docs found, return top k regardless
        if not relevant_docs:
            relevant_docs = [doc for doc, score in results[:k]]
            print(f"⚠️ No highly relevant docs found. Using top {k} results.")
        
        return relevant_docs
    
    def retrieve_with_scores(self, query: str, k: int = None) -> List[tuple]:
        """Retrieve documents with similarity scores."""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized.")
        
        if k is None:
            k = self.config.RETRIEVAL_K
        
        return self.vectorstore.similarity_search_with_score(query, k=k)
    
    def get_document_sources(self, documents: List[Document]) -> List[str]:
        """Extract source names from documents."""
        return list(set([doc.metadata.get('source', 'Unknown') for doc in documents]))

       