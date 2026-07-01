import os
from typing import List
from groq import Groq
from langchain_core.documents import Document
from config import Config

class LLMAgent:
    """Handles LLM-based response generation using Groq."""
    
    def __init__(self):
        self.config = Config()
        self.client = None
        self.model = self.config.GROQ_MODEL
        
        # Initialize Groq
        api_key = self.config.GROQ_API_KEY
        if api_key:
            try:
                self.client = Groq(api_key=api_key)
                print(f"✅ Groq initialized with model: {self.model}")
                print(f"   Rate Limits: 30 req/min, 6,000 tokens/min")
            except Exception as e:
                print(f"⚠️ Groq initialization error: {e}")
                self.client = None
        else:
            print("⚠️ GROQ_API_KEY not found in .env file")
            print("   Please create a .env file with: GROQ_API_KEY=your_key_here")
            self.client = None
        
        # Crop terms for relevance checking
        self.crop_terms = ['maize', 'corn', 'mahindi', 'bean', 'beans', 'maharagwe', 
                           'coffee', 'kahawa', 'sugarcane', 'miwa', 'wheat', 'ngano', 
                           'sweet potato', 'cassava', 'rice', 'tomato', 'onion', 'cabbage',
                           'tea', 'chai', 'cotton', 'pamba', 'sisal']
    
    def generate_response(self, question: str, context: List[Document]) -> str:
        """Generate a response using Groq with context."""
        
        if not self.client:
            return self._fallback_response(question, context)
        
        if not context:
            return self._handle_no_context(question)
        
        # Prepare context
        context_text = "\n\n".join([doc.page_content for doc in context[:5]])
        if len(context_text) > 3000:
            context_text = context_text[:3000] + "..."
        
        # Build prompt
        prompt = self.config.PROMPT_TEMPLATE.format(
            context=context_text,
            question=question
        )
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful agricultural advisor for Kenyan farmers. Always respond in clear, simple English."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=512,
                top_p=0.95,
            )
            
            response = chat_completion.choices[0].message.content
            
            if not response or len(response.strip()) < 20:
                return self._fallback_response(question, context)
            
            return response
            
        except Exception as e:
            print(f"⚠️ Groq API error: {e}")
            return self._fallback_response(question, context)
    
    def _handle_no_context(self, question: str) -> str:
        """Handle when no context is found."""
        return f"""I don't have specific information about '{question}' in my knowledge base.

However, based on general knowledge of Kenyan agriculture:

📌 The Ministry of Agriculture, Livestock, Fisheries, and Cooperatives oversees agricultural policy in Kenya.

📌 KALRO (Kenya Agricultural and Livestock Research Organization) provides research and extension services.

📌 Local agricultural extension officers are available in every county to assist farmers.

Would you like me to help with a specific crop or topic?"""
    
    def _fallback_response(self, question: str, context: List[Document]) -> str:
        """Fallback response when Groq is not available."""
        if not context:
            return self._handle_no_context(question)
        
        context_text = "\n\n".join([doc.page_content for doc in context[:2]])
        
        lines = context_text.split('\n')
        cleaned_lines = []
        skip_patterns = ['www.AgriMoon.Com', 'AgriMoon', 'Diseases of Field Crops']
        for line in lines:
            if not any(pattern.lower() in line.lower() for pattern in skip_patterns):
                cleaned_lines.append(line)
        
        context_text = '\n'.join(cleaned_lines)[:1000]
        
        return f"Based on agricultural documents:\n\n{context_text}"