import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_loader import PDFLoader
from vector_store import VectorStore
from agents import AgentRouter
from config import Config

class AgricultureBot:
    """Main application class for the Agriculture Multi-Agent RAG system."""
    
    def __init__(self):
        self.config = Config()
        self.pdf_loader = PDFLoader()
        self.vector_store = VectorStore()
        self.router = AgentRouter()
        self.initialized = False
    
    def initialize(self, rebuild: bool = False):
        """Initialize the system by loading or creating the vector store."""
        try:
            if rebuild or not os.path.exists(self.config.VECTOR_STORE_DIR):
                print("\n🔄 Building vector store from PDFs...")
                documents = self.pdf_loader.load_pdf()
                chunks = self.pdf_loader.chunk_documents(documents)
                self.vector_store.create(chunks)
            else:
                self.vector_store.load()
            
            self.initialized = True
            
            print("\n" + "=" * 50)
            print("🌾 Agriculture Multi-Agent RAG System")
            print("=" * 50)
            print("✅ System initialized successfully!")
            print("📚 Knowledge base: 45+ PDF documents")
            print("🤖 Agents: Crop, Livestock, Poultry, General")
            print("⚡ LLM: Groq (Fast, High-Quality Responses)")
            print(f"   Model: {self.config.GROQ_MODEL}")
            print("🔍 Query expansion enabled")
            print("🎯 Relevance filtering enabled")
            print("🌍 Responses: Always in English")
            print("=" * 50 + "\n")
            
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            raise
    
    def query(self, question: str) -> dict:
        """Query the system with a question."""
        if not self.initialized:
            raise ValueError("System not initialized.")
        
        # Retrieve relevant documents with relevance filtering
        documents = self.vector_store.retrieve_relevant(
            question, 
            k=self.config.RETRIEVAL_K,
            threshold=0.5
        )
        
        if not documents:
            return {
                "answer": f"I couldn't find specific information about '{question}' in my knowledge base.\n\n📌 Suggestions:\n1. Try asking about a specific crop (e.g., 'maize disease symptoms')\n2. Ask about a specific disease (e.g., 'how to treat leaf rust')\n3. Consult your local agricultural extension officer\n4. Visit KALRO's official website for more resources"
            }
        
        # Route to appropriate agent
        answer = self.router.route(question, documents)
        
        return {"answer": answer}


def main():
    """Command-line interface for the Agriculture Multi-Agent system."""
    print("=" * 50)
    print("🌾 Agriculture Multi-Agent RAG System")
    print("⚡ Powered by Groq")
    print("=" * 50)
    
    # Check for Groq API key
    if not Config.GROQ_API_KEY:
        print("\n⚠️ WARNING: GROQ_API_KEY not found in .env file")
        print("   Please create a .env file with: GROQ_API_KEY=your_key_here")
        print("   The bot will run in fallback mode (direct retrieval only).\n")
    
    bot = AgricultureBot()
    
    rebuild = input("\n🔄 Rebuild vector store from PDFs? (y/n): ").strip().lower()
    bot.initialize(rebuild=(rebuild == 'y'))
    
    print("\n💬 Ask agricultural questions. Type 'exit' or 'quit' to stop.")
    print("\n📝 Examples:")
    print("   'What are the symptoms of maize disease?'")
    print("   'Dalili za ugonjwa wa mahindi ni zipi?' (Swahili is OK!)")
    print("   'How do I treat coccidiosis in chickens?'")
    print("   'What fertilizers are recommended for beans?'")
    print()
    
    while True:
        try:
            question = input("❓ You: ").strip()
            
            if question.lower() in ['exit', 'quit', 'q', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not question:
                continue
            
            response = bot.query(question)
            print(f"\n🤖 {response['answer']}")
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()