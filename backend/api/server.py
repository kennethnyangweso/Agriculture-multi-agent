import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Import your RAG system
from src.main import AgricultureBot

# Initialize FastAPI
app = FastAPI(
    title="Agriculture Multi-Agent API",
    description="AI-powered agricultural assistant for Kenyan farmers",
    version="1.0.0"
)

# CORS middleware - allows frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://agriculture-multi-agent.vercel.app",
        "https://agriculture-multi-agent.netlify.app",
        "*"  # For testing - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the bot
bot = AgricultureBot()

# Rebuild flag (set to True to rebuild vector store on startup)
REBUILD = False

try:
    bot.initialize(rebuild=REBUILD)
    print("✅ Bot initialized successfully!")
except Exception as e:
    print(f"❌ Bot initialization error: {e}")


# Request/Response Models
class QueryRequest(BaseModel):
    question: str
    language: Optional[str] = "auto"  # 'en', 'sw', or 'auto'

class QueryResponse(BaseModel):
    answer: str
    success: bool = True
    error: Optional[str] = None


@app.get("/")
async def root():
    return {
        "name": "Agriculture Multi-Agent API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "/query": "POST - Ask agricultural questions",
            "/health": "GET - Check system health"
        },
        "example": {
            "question": "What are the symptoms of maize disease?"
        }
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "initialized": bot.initialized,
        "agents": ["crops", "livestock", "poultry", "general"]
    }


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Send a query to the Agriculture Multi-Agent system."""
    try:
        if not request.question or len(request.question.strip()) < 2:
            return QueryResponse(
                answer="Please enter a valid question.",
                success=False,
                error="Question too short"
            )
        
        # Get response from bot
        response = bot.query(request.question)
        
        return QueryResponse(
            answer=response.get("answer", "No response generated."),
            success=True
        )
        
    except Exception as e:
        return QueryResponse(
            answer="Sorry, an error occurred while processing your question.",
            success=False,
            error=str(e)
        )


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
