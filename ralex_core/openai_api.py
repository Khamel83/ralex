"""
OpenAI-Compatible API Layer for Ralex V3

Provides OpenAI-compatible endpoints for Open WebUI integration while preserving
all Ralex V2 functionality including semantic routing, AgentOS integration,
and intelligent budget management.
"""

import json
import uuid
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional, AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Import existing Ralex components
from ralex_core.semantic_classifier import SemanticClassifier
from ralex_core.router import SmartRouter
from ralex_core.budget import BudgetManager
from ralex_core.agentos_web_integration import AgentOSWebIntegration
from ralex_core.openrouter_client import OpenRouterClient
from ralex_core.web_session import WebSessionManager, session_manager
from ralex_core.websocket_manager import WebSocketManager, websocket_manager


# OpenAI-compatible request/response models
class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: system, user, or assistant")
    content: str = Field(..., description="Message content")
    name: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    model: str = Field(default="ralex-smart", description="Model to use")
    messages: List[ChatMessage] = Field(..., description="Conversation messages")
    stream: bool = Field(default=False, description="Stream response")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=None, gt=0)
    user: Optional[str] = Field(default=None, description="User identifier")


class ChatCompletionChoice(BaseModel):
    index: int
    message: Optional[ChatMessage] = None
    delta: Optional[Dict[str, Any]] = None
    finish_reason: Optional[str] = None


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Dict[str, int] = {}


class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str = "ralex"


# Global instances
semantic_classifier = None
smart_router = None
budget_manager = None
agentos = None
openrouter_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize Ralex components on startup"""
    global semantic_classifier, smart_router, budget_manager, agentos, openrouter_client
    
    print("Starting Ralex V3 API server...")
    
    # Initialize components
    try:
        semantic_classifier = SemanticClassifier()
        smart_router = SmartRouter()
        budget_manager = BudgetManager()
        agentos = AgentOSWebIntegration()
        openrouter_client = OpenRouterClient()
        
        # Start WebSocket background tasks
        await websocket_manager.start_background_tasks()
        
        # Set up WebSocket event handlers
        setup_websocket_handlers()
        
        print("✅ All Ralex components initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing Ralex components: {e}")
        # Continue anyway for testing
    
    yield
    
    # Shutdown components
    await websocket_manager.shutdown()
    session_manager.shutdown()
    print("Shutting down Ralex V3 API server...")


def setup_websocket_handlers():
    """Set up WebSocket event handlers for session integration"""
    
    async def handle_budget_add_request(data):
        """Handle budget addition requests from WebSocket"""
        session_id = data["session_id"]
        connection_id = data["connection_id"]
        amount = data["amount"]
        
        # Add budget to session
        result = session_manager.add_budget_to_session(session_id, amount)
        
        if result:
            # Send confirmation and updated budget
            budget_status = session_manager.get_session_budget_status(session_id)
            await websocket_manager.send_budget_update(session_id, budget_status)
            
            await websocket_manager.send_system_notification(
                session_id, 
                f"Added ${amount:.2f} to budget. New total: ${result['new_limit']:.2f}",
                "success"
            )
        else:
            await websocket_manager.send_to_connection(connection_id, {
                "type": "error",
                "data": {"error": "Failed to add budget"}
            })
    
    async def handle_file_add_request(data):
        """Handle file context addition requests"""
        session_id = data["session_id"]
        connection_id = data["connection_id"]
        file_path = data["file_path"]
        
        # Add file to session context (would read actual file in production)
        session = session_manager.get_session(session_id)
        if session and agentos:
            agentos.add_file_to_session(session_id, file_path, "# File content", {"type": "code"})
            
            await websocket_manager.send_to_connection(connection_id, {
                "type": "file_context_update",
                "data": {
                    "action": "added",
                    "file_path": file_path,
                    "files_count": len(session.file_context.files)
                }
            })
        else:
            await websocket_manager.send_to_connection(connection_id, {
                "type": "error",
                "data": {"error": "Failed to add file to context"}
            })
    
    async def handle_session_info_request(data):
        """Handle session info requests"""
        session_id = data["session_id"]
        connection_id = data["connection_id"]
        
        session = session_manager.get_session(session_id)
        if session:
            session_summary = session.get_session_summary()
            await websocket_manager.send_to_connection(connection_id, {
                "type": "session_info",
                "data": session_summary
            })
    
    # Register event handlers
    websocket_manager.on("budget_add_request", handle_budget_add_request)
    websocket_manager.on("file_add_request", handle_file_add_request)
    websocket_manager.on("session_info_request", handle_session_info_request)


# Create FastAPI app
app = FastAPI(
    title="Ralex V3 API",
    description="OpenAI-compatible API for Ralex AI Coding Assistant",
    version="3.0.0",
    lifespan=lifespan
)

# Add CORS middleware for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_or_create_session(user: Optional[str] = None) -> str:
    """Get or create session ID using session manager"""
    session_id, session = session_manager.get_or_create_session(
        session_id=f"user_{user}" if user else None,
        initial_budget=5.0
    )
    return session_id


async def enhance_with_agentos(user_message: str, session_id: str) -> str:
    """Enhance user message with AgentOS standards and context"""
    if not agentos:
        return user_message
    
    try:
        return agentos.enhance_web_request(user_message, session_id)
    except Exception as e:
        print(f"Warning: AgentOS enhancement failed: {e}")
        return user_message


async def classify_and_route(enhanced_prompt: str, session_id: str) -> Dict[str, Any]:
    """Classify intent and select appropriate model"""
    try:
        # Classify intent
        intent = "default"
        if semantic_classifier:
            intent = semantic_classifier.classify_intent(enhanced_prompt)
        
        # Route to appropriate model
        selected_model = "gpt-3.5-turbo"  # Fallback
        if smart_router:
            session = session_manager.get_session(session_id)
            if session:
                budget_context = {
                    "spent": session.budget.spent,
                    "limit": session.budget.current_limit
                }
                selected_model = smart_router.select_model(intent, enhanced_prompt, budget_context)
        
        return {
            "intent": intent,
            "model": selected_model,
            "reasoning": f"Classified as '{intent}', routed to {selected_model}"
        }
    except Exception as e:
        print(f"Warning: Classification/routing failed: {e}")
        return {
            "intent": "default",
            "model": "gpt-3.5-turbo",
            "reasoning": f"Fallback due to error: {e}"
        }


async def call_ralex_backend(messages: List[ChatMessage], model: str, session_id: str) -> str:
    """Call the actual Ralex backend logic"""
    try:
        if not openrouter_client:
            return "Error: OpenRouter client not initialized"
        
        # Convert messages to format expected by OpenRouter
        openrouter_messages = []
        for msg in messages:
            openrouter_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Make the API call
        response = openrouter_client.create_chat_completion(
            model=model,
            messages=openrouter_messages,
            stream=False
        )
        
        if response and "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0]["message"]["content"]
            
            # Update budget tracking
            if "usage" in response:
                usage = response["usage"]
                # Estimate cost (this would use actual pricing in production)
                estimated_cost = (usage.get("total_tokens", 0) * 0.000002)  # Rough estimate
                
                # Charge session budget
                session_manager.charge_session(
                    session_id, estimated_cost, model, 
                    "Chat completion", usage.get("total_tokens", 0)
                )
                
                # Get updated budget status
                budget_status = session_manager.get_session_budget_status(session_id)
                if budget_status:
                    # Send budget update via WebSocket
                    await websocket_manager.send_budget_update(session_id, budget_status)
            
            return content
        else:
            return "Error: No response from OpenRouter"
    
    except Exception as e:
        print(f"Error calling Ralex backend: {e}")
        return f"Error: {str(e)}"


async def stream_ralex_response(messages: List[ChatMessage], model: str, session_id: str) -> AsyncGenerator[str, None]:
    """Stream response from Ralex backend"""
    try:
        # For now, simulate streaming by chunking the response
        full_response = await call_ralex_backend(messages, model, session_id)
        
        # Split response into chunks for streaming
        words = full_response.split()
        chunk_size = 3  # Words per chunk
        
        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i + chunk_size]
            chunk_content = " " + " ".join(chunk_words)
            
            # Format as OpenAI streaming chunk
            chunk_data = {
                "id": f"chatcmpl-ralex-{uuid.uuid4().hex[:8]}",
                "object": "chat.completion.chunk",
                "created": int(datetime.now().timestamp()),
                "model": model,
                "choices": [{
                    "index": 0,
                    "delta": {"content": chunk_content},
                    "finish_reason": None
                }]
            }
            
            yield f"data: {json.dumps(chunk_data)}\n\n"
            await asyncio.sleep(0.1)  # Small delay for realistic streaming
        
        # Send final chunk
        final_chunk = {
            "id": f"chatcmpl-ralex-{uuid.uuid4().hex[:8]}",
            "object": "chat.completion.chunk",
            "created": int(datetime.now().timestamp()),
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {},
                "finish_reason": "stop"
            }]
        }
        yield f"data: {json.dumps(final_chunk)}\n\n"
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        error_chunk = {
            "id": f"chatcmpl-ralex-error",
            "object": "chat.completion.chunk",
            "created": int(datetime.now().timestamp()),
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {"content": f"\n\nError: {str(e)}"},
                "finish_reason": "stop"
            }]
        }
        yield f"data: {json.dumps(error_chunk)}\n\n"
        yield "data: [DONE]\n\n"


# API Endpoints

@app.get("/v1/models")
async def list_models():
    """List available models (OpenAI-compatible)"""
    models = [
        ModelInfo(
            id="ralex-smart",
            created=int(datetime.now().timestamp()),
        ),
        ModelInfo(
            id="ralex-fast", 
            created=int(datetime.now().timestamp()),
        ),
        ModelInfo(
            id="ralex-budget",
            created=int(datetime.now().timestamp()),
        )
    ]
    return {"object": "list", "data": models}


@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    """Create chat completion (OpenAI-compatible)"""
    
    # Get or create session
    session_id = get_or_create_session(request.user)
    
    # Extract user message
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages cannot be empty")
    
    user_message = request.messages[-1].content
    
    # Check budget before processing
    if not session_manager.can_afford(session_id, 0.01):  # Minimum cost check
        raise HTTPException(status_code=402, detail="Insufficient budget")
    
    # Enhance with AgentOS
    enhanced_prompt = await enhance_with_agentos(user_message, session_id)
    
    # Classify and route
    routing_info = await classify_and_route(enhanced_prompt, session_id)
    selected_model = routing_info["model"]
    
    # Add message to session conversation
    session = session_manager.get_session(session_id)
    if session:
        session.add_message("user", user_message, {
            "enhanced_prompt": enhanced_prompt,
            "intent": routing_info["intent"],
            "reasoning": routing_info["reasoning"]
        })
    
    # Send typing indicator and model selection info
    await websocket_manager.send_typing_indicator(session_id, True, selected_model, "Processing request...")
    await websocket_manager.send_model_selection(session_id, selected_model, routing_info["reasoning"])
    
    if request.stream:
        # Streaming response
        return StreamingResponse(
            stream_ralex_response(request.messages, selected_model, session_id),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
    else:
        # Non-streaming response
        response_content = await call_ralex_backend(request.messages, selected_model, session_id)
        
        # Stop typing indicator
        await websocket_manager.send_typing_indicator(session_id, False)
        
        # Add assistant message to session
        if session:
            session.add_message("assistant", response_content, {
                "model": selected_model,
                "intent": routing_info["intent"]
            })
        
        return ChatCompletionResponse(
            id=f"chatcmpl-ralex-{uuid.uuid4().hex[:8]}",
            created=int(datetime.now().timestamp()),
            model=selected_model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=ChatMessage(role="assistant", content=response_content),
                    finish_reason="stop"
                )
            ],
            usage={
                "prompt_tokens": len(user_message.split()),
                "completion_tokens": len(response_content.split()),
                "total_tokens": len(user_message.split()) + len(response_content.split())
            }
        )


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time updates"""
    
    # Extract client info from headers
    user_agent = websocket.headers.get("user-agent", "")
    client_host = websocket.client.host if websocket.client else ""
    
    connection_id = await websocket_manager.connect(websocket, session_id, user_agent, client_host)
    
    try:
        # Send initial session data
        session = session_manager.get_session(session_id)
        if session:
            budget_status = session_manager.get_session_budget_status(session_id)
            await websocket_manager.send_to_connection(connection_id, {
                "type": "session_info",
                "data": {
                    "session_id": session_id,
                    "budget": budget_status,
                    "files_in_context": len(session.file_context.files),
                    "conversation_length": len(session.conversation)
                }
            })
        
        # Keep connection alive and handle messages
        while True:
            try:
                # Wait for client messages
                data = await websocket.receive_text()
                await websocket_manager.handle_client_message(connection_id, data)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"WebSocket error for {connection_id}: {e}")
                break
    
    finally:
        await websocket_manager.disconnect(connection_id)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "3.0.0",
        "components": {
            "semantic_classifier": semantic_classifier is not None,
            "smart_router": smart_router is not None,
            "budget_manager": budget_manager is not None,
            "agentos": agentos is not None,
            "openrouter_client": openrouter_client is not None
        }
    }


@app.get("/api/sessions/{session_id}/budget")
async def get_session_budget(session_id: str):
    """Get current budget for session"""
    budget_status = session_manager.get_session_budget_status(session_id)
    if not budget_status:
        raise HTTPException(status_code=404, detail="Session not found")
    return budget_status


@app.post("/api/sessions/{session_id}/budget/add")
async def add_session_budget(session_id: str, amount: float):
    """Add budget to session"""
    result = session_manager.add_budget_to_session(session_id, amount)
    if not result:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Notify via WebSocket
    budget_status = session_manager.get_session_budget_status(session_id)
    if budget_status:
        await websocket_manager.send_budget_update(session_id, budget_status)
    
    return result


@app.get("/api/sessions/{session_id}/info")
async def get_session_info(session_id: str):
    """Get session information"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session.get_session_summary()


@app.get("/api/sessions/stats")
async def get_sessions_stats():
    """Get overall session statistics"""
    return session_manager.get_session_stats()


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the FastAPI server"""
    uvicorn.run(
        "ralex_core.openai_api:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    run_server(reload=True)