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

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "ralex-bridge"
    messages: list[Message]
    max_tokens: int = 150
    temperature: float = 0.7
    stream: bool = False

class ChatResponse(BaseModel):
    response: str
    model_used: str
    context_saved: bool = True

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """OpenAI-compatible chat completions endpoint"""
    try:
        # Extract latest message from conversation
        if not request.messages or len(request.messages) == 0:
            raise HTTPException(status_code=400, detail="No messages provided")
        
        # Get the latest user message
        latest_message = request.messages[-1]
        if latest_message.role != "user":
            raise HTTPException(status_code=400, detail="Last message must be from user")
            
        prompt = latest_message.content
        
        # Process through RalexBridge
        result = await bridge.process_request(prompt)
        
        # Handle budget constraint violations
        if "error" in result and "Budget constraint violation" in result["error"]:
            # Return informative budget error in OpenAI format
            budget_info = result.get("budget_status", {})
            error_detail = f"Budget limit exceeded. {budget_info.get('reason', 'Budget exceeded')}. Remaining: ${budget_info.get('remaining_daily', 0):.4f}"
            
            return {
                "id": f"ralex-budget-{hash(prompt) % 10000}",
                "object": "chat.completion", 
                "model": request.model,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": f"Budget constraint: {error_detail}\n\nSuggestion: {budget_info.get('suggestion', 'Try a simpler query or increase budget.')}"
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": len(prompt.split()),
                    "completion_tokens": 20,  # Estimate for budget message
                    "total_tokens": len(prompt.split()) + 20
                }
            }
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Format successful response in OpenAI format
        response_content = result.get("response", "No response generated")
        
        # Calculate realistic token counts
        prompt_tokens = max(len(prompt.split()) * 1.3, 10)  # Estimate with buffer
        completion_tokens = max(len(response_content.split()) * 1.3, 10)
        
        response = {
            "id": f"ralex-{abs(hash(prompt)) % 100000000}",
            "object": "chat.completion",
            "created": int(__import__("time").time()),
            "model": result.get("model_used", request.model),
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_content
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": int(prompt_tokens),
                "completion_tokens": int(completion_tokens), 
                "total_tokens": int(prompt_tokens + completion_tokens)
            }
        }
        
        # Add budget info to response if available
        if "budget_info" in result:
            budget_info = result["budget_info"]
            response["ralex_budget"] = {
                "estimated_cost": budget_info.get("estimated_cost", 0.0),
                "actual_cost": budget_info.get("actual_cost", 0.0),
                "remaining_daily": budget_info.get("remaining_daily", 0.0),
                "philosophy": "Cost-first decision making"
            }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/v1/models")
async def list_models():
    """List available models for mobile app compatibility"""
    return {
        "object": "list",
        "data": [
            {
                "id": "ralex-bridge",
                "object": "model",
                "created": 1672531200,
                "owned_by": "ralex",
                "description": "Ralex cost-first agentic AI with budget constraints"
            },
            {
                "id": "ralex-cheap",
                "object": "model", 
                "created": 1672531200,
                "owned_by": "ralex",
                "description": "Cheap model tier for simple queries"
            },
            {
                "id": "ralex-medium",
                "object": "model",
                "created": 1672531200, 
                "owned_by": "ralex",
                "description": "Medium model tier for complex queries"
            }
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint with budget status"""
    health_status = {
        "status": "healthy", 
        "components": ["AgentOS", "LiteLLM", "OpenRouter", "OpenCode", "BudgetEnforcer"],
        "philosophy": "Cost-first agentic thinking"
    }
    
    # Add budget status if available
    if bridge.budget_enforcer:
        budget_report = bridge.budget_enforcer.generate_budget_report()
        health_status["budget"] = {
            "daily_utilization": f"{budget_report['daily_utilization']:.1f}%",
            "remaining_daily": f"${budget_report['remaining_daily']:.4f}",
            "status": budget_report.get("status", budget_report.get("warning", "OK"))
        }
    
    return health_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)