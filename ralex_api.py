#!/usr/bin/env python3
"""
FastAPI wrapper for RalexBridge - OpenWebUI integration endpoint
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from ralex_bridge import RalexBridge

app = FastAPI(title="Ralex Bridge API", version="4.0.0")
bridge = RalexBridge()

class ChatRequest(BaseModel):
    message: str
    model: str = "ralex-bridge"
    stream: bool = False

class ChatResponse(BaseModel):
    response: str
    model_used: str
    context_saved: bool = True

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """OpenAI-compatible endpoint for OpenWebUI"""
    try:
        # Extract message from request
        prompt = request.message
        
        # Process through RalexBridge
        result = await bridge.process_request(prompt)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Format response for OpenWebUI
        response = {
            "id": "ralex-" + str(hash(prompt))[:8],
            "object": "chat.completion",
            "model": result.get("model_used", "ralex-bridge"),
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": result["response"]
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(result["response"].split()),
                "total_tokens": len(prompt.split()) + len(result["response"].split())
            }
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/models")
async def list_models():
    """List available models for OpenWebUI"""
    return {
        "object": "list",
        "data": [
            {
                "id": "ralex-bridge",
                "object": "model",
                "created": 1672531200,
                "owned_by": "ralex"
            }
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "components": ["AgentOS", "LiteLLM", "OpenRouter", "OpenCode"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)