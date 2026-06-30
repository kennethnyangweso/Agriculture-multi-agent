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
                           'sweet potato', 'cassava', 'rice', 'tomato', 'onion', 'cabbage']
        
        # Disease terms for relevance checking (only for disease-related questions)
        self.disease_terms = ['lethal necrosis', 'mln', 'rust', 'blight', 'wilt', 
                              'spot', 'canker', 'mosaic', 'rot', 'mildew', 
                              'anthracnose', 'smut', 'streak', 'mottle']
        
        # Fertilizer/management terms
        self.management_terms = ['fertilizer', 'fertilizers', 'mbolea', 'pest', 'pesticide', 
                                 'dawa', 'weed', 'herbicide', 'fungicide', 'insecticide',
                                 'treat', 'treatment', 'control', 'manage', 'management']
    
    def generate_response(self, question: str, context: List[Document]) -> str:
        """Generate a response using Groq with context relevance checking."""
        
        # If Groq is not available, use fallback
        if not self.client:
            return self._fallback_response(question, context)
        
        if not context:
            return self._handle_no_context(question)
        
        # Prepare context
        context_text = "\n\n".join([doc.page_content for doc in context[:3]])
        if len(context_text) > 3000:
            context_text = context_text[:3000] + "..."
        
        # Detect what the question is about
        question_lower = question.lower()
        mentioned_crops = [term for term in self.crop_terms if term in question_lower]
        mentioned_diseases = [term for term in self.disease_terms if term in question_lower]
        is_management_query = any(term in question_lower for term in self.management_terms)
        
        # Check if context contains the mentioned crops
        context_lower = context_text.lower()
        has_crop_in_context = any(crop in context_lower for crop in mentioned_crops) if mentioned_crops else True
        
        # If crops are mentioned but not in context, warn but still try to answer
        if mentioned_crops and not has_crop_in_context:
            # Check if ANY crop is mentioned in context
            any_crop_in_context = any(crop in context_lower for crop in self.crop_terms)
            if not any_crop_in_context:
                return self._handle_missing_crop_context(question, mentioned_crops)
        
        # If the question is about disease but no disease context
        if mentioned_diseases and not has_crop_in_context:
            # Only trigger if question is explicitly about disease
            if any(term in question_lower for term in ['disease', 'symptom', 'ugonjwa', 'dalili']):
                return self._handle_missing_disease_context(question, mentioned_diseases)
        
        # Prepare prompt
        prompt = self.config.PROMPT_TEMPLATE.format(
            context=context_text,
            question=question
        )
        
        try:
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful agricultural advisor for Kenyan farmers. Always respond in clear, simple English. Use the context provided to answer the question. If the context doesn't contain specific information about the crop asked, say so and provide general guidance based on what you do know."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=512,
                top_p=0.95,
            )
            
            response = chat_completion.choices[0].message.content
            
            # If response is empty or too short, use fallback
            if not response or len(response.strip()) < 20:
                return self._fallback_response(question, context)
            
            return response
            
        except Exception as e:
            print(f"⚠️ Groq API error: {e}")
            return self._fallback_response(question, context)
    
    def _handle_no_context(self, question: str) -> str:
        """Handle when no context is found."""
        return f"""I couldn't find specific information about '{question}' in my knowledge base.

📌 Suggestions:
1. Try asking about a specific crop (e.g., 'maize disease symptoms')
2. Ask about a specific disease or topic (e.g., 'how to treat leaf rust')
3. Consult your local agricultural extension officer for field-specific advice
4. Visit KALRO's official website for more resources

I'm here to help with any other agricultural questions you have!"""
    
    def _handle_missing_crop_context(self, question: str, crops: list) -> str:
        """Handle when context doesn't contain the crop mentioned."""
        crop_text = ', '.join(crops)
        
        return f"""I notice you're asking about **{crop_text}**.

However, my knowledge base doesn't contain specific information about {crop_text} in the context I retrieved. I found information about other crops instead.

📌 For official information on {crop_text}, I recommend:
- KALRO (Kenya Agricultural and Livestock Research Organization)
- Your local agricultural extension officer
- Ministry of Agriculture, Livestock and Fisheries

Would you like to ask about a specific crop that I might have information on?"""
    
    def _handle_missing_disease_context(self, question: str, diseases: list) -> str:
        """Handle when context doesn't contain the disease mentioned."""
        disease_text = ', '.join(diseases)
        
        return f"""I notice you're asking about **{disease_text}**.

However, my knowledge base doesn't contain specific information about this disease in the context I retrieved.

📌 For official information on this disease, I recommend:
- KALRO (Kenya Agricultural and Livestock Research Organization)
- Your local agricultural extension officer
- CABI Plantwise Knowledge Bank

Would you like to ask about a specific crop or disease that I might have information on?"""
    
    def _fallback_response(self, question: str, context: List[Document]) -> str:
        """Fallback response when Groq is not available."""
        if not context:
            return self._handle_no_context(question)
        
        # Combine context
        context_text = "\n\n".join([doc.page_content for doc in context[:2]])
        
        # Clean up raw text
        lines = context_text.split('\n')
        cleaned_lines = []
        skip_patterns = ['www.AgriMoon.Com', 'AgriMoon', 'Diseases of Field Crops']
        for line in lines:
            if not any(pattern.lower() in line.lower() for pattern in skip_patterns):
                cleaned_lines.append(line)
        
        context_text = '\n'.join(cleaned_lines)[:1000]
        
        return f"Based on agricultural documents:\n\n{context_text}\n\n---\n📌 This information is from agricultural documents. For more details, consult your agricultural extension officer."