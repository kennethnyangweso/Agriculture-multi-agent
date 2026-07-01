from typing import List
from langchain_core.documents import Document
from config import Config
from llm_agent import LLMAgent

class BaseAgent:
    """Base class for all agricultural agents."""
    
    def __init__(self, name: str, domain: str):
        self.name = name
        self.domain = domain
        self.config = Config()
        self.llm = LLMAgent()
    
    def format_response(self, query: str, context: List[Document]) -> str:
        """Format response using Groq LLM."""
        response = self.llm.generate_response(query, context)
        return f"🌾 **{self.name} Response:**\n\n{response}"
    
    def get_fallback(self, query: str) -> str:
        """Get fallback response when no context is found."""
        return f"🌾 **{self.name} Response:**\n\nI don't have enough information in my knowledge base. Please consult your local agricultural extension officer or veterinarian."


class CropAgent(BaseAgent):
    def __init__(self):
        super().__init__("Crop Specialist", "crops")
    
    def process(self, query: str, context: List[Document]) -> str:
        if not context:
            return self.get_fallback(query)
        return self.format_response(query, context)


class LivestockAgent(BaseAgent):
    def __init__(self):
        super().__init__("Livestock Specialist", "livestock")
    
    def process(self, query: str, context: List[Document]) -> str:
        if not context:
            return self.get_fallback(query)
        return self.format_response(query, context)


class PoultryAgent(BaseAgent):
    def __init__(self):
        super().__init__("Poultry Specialist", "poultry")
    
    def process(self, query: str, context: List[Document]) -> str:
        if not context:
            return self.get_fallback(query)
        return self.format_response(query, context)


class GeneralAgent(BaseAgent):
    def __init__(self):
        super().__init__("General Agriculture Advisor", "general")
    
    def process(self, query: str, context: List[Document]) -> str:
        if not context:
            return self.get_fallback(query)
        return self.format_response(query, context)


class AgentRouter:
    """Routes queries to the appropriate specialized agent."""
    
    def __init__(self):
        self.agents = {
            'crops': CropAgent(),
            'livestock': LivestockAgent(),
            'poultry': PoultryAgent(),
            'general': GeneralAgent()
        }
        self.config = Config()
    
    def detect_domain(self, query: str) -> str:
        """Detect which domain the query belongs to."""
        query_lower = query.lower()
        
        domain_scores = {}
        for domain, keywords in self.config.DOMAIN_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            domain_scores[domain] = score
        
        best_domain = max(domain_scores, key=domain_scores.get)
        
        if domain_scores[best_domain] == 0:
            crop_terms = ['maize', 'corn', 'mahindi', 'bean', 'coffee', 'kahawa']
            if any(term in query_lower for term in crop_terms):
                return 'crops'
            return 'general'
        
        return best_domain
    
    def route(self, query: str, context: List[Document]) -> str:
        """Route the query to the appropriate agent."""
        domain = self.detect_domain(query)
        print(f"🔀 Routing: Domain={domain}")
        
        agent = self.agents.get(domain, self.agents['general'])
        return agent.process(query, context)