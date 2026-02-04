from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import os

from core.config import settings
from core.agent import agent

app = FastAPI(
    title="Data Analysis Agent API",
    description="AI agent for data analysis with MongoDB, Python, and web search capabilities",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (for images)
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    user_message: Optional[str] = None


class ChatResponse(BaseModel):
    messages: List[Message]
    artifacts: List[str] = []
    error: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Data Analysis Agent API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "llm_provider": settings.llm_provider,
        "mongo_connected": agent.tools["mongo"].connected,
        "web_search_available": agent.tools["web_search"].available
    }


@app.post("/agent/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the agent
    
    Send either:
    - messages: Full conversation history
    - user_message: Just the latest message (for new conversations)
    """
    try:
        # Extract conversation history
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ] if request.messages else []
        
        # Get user message
        if request.user_message:
            user_message = request.user_message
        elif conversation_history and conversation_history[-1]["role"] == "user":
            user_message = conversation_history[-1]["content"]
            conversation_history = conversation_history[:-1]
        else:
            raise HTTPException(status_code=400, detail="No user message provided")
        
        # Run agent
        result = await agent.run(user_message, conversation_history)
        
        # Convert messages back to Pydantic models
        messages = [Message(**msg) for msg in result["messages"]]
        
        return ChatResponse(
            messages=messages,
            artifacts=result.get("artifacts", []),
            error=result.get("error")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """List available tools"""
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in agent.tools.values()
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
