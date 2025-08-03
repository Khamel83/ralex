#!/usr/bin/env python3
"""
Ralex Integration with Universal Logger
Minimal performance impact, maximum data collection.
"""

from universal_logger import get_logger, log_ai_operation
import functools
import time
from typing import Any, Dict

class RalexLoggerMixin:
    """
    Mixin to add universal logging to any Ralex component.
    Designed to be lightweight and non-intrusive.
    """
    
    def __init__(self):
        self.logger = get_logger()
    
    def log_bridge_operation(self, prompt: str, model: str, response: str, 
                           cost: float = 0.0, thinking: Dict[str, Any] = None):
        """Log RalexBridge operations with full context."""
        return self.logger.log_operation(
            operation_type="ralex_bridge",
            prompt=prompt,
            response=response,
            model=model,
            cost=cost,
            metadata={
                "thinking": thinking,
                "complexity": thinking.get("complexity") if thinking else "unknown",
                "safety_check": thinking.get("safety_check") if thinking else True,
                "requires_code": thinking.get("requires_code") if thinking else False
            }
        )
    
    def log_model_routing(self, original_model: str, selected_model: str, 
                         reasoning: str, cost_estimate: float = 0.0):
        """Log model routing decisions for cost optimization analysis."""
        return self.logger.log_operation(
            operation_type="model_routing",
            model=selected_model,
            cost=cost_estimate,
            metadata={
                "original_model": original_model,
                "selected_model": selected_model,
                "routing_reasoning": reasoning,
                "cost_optimization": True
            }
        )
    
    def log_execution_result(self, operation_id: str, success: bool, 
                           execution_type: str, output: str = ""):
        """Log execution results linked to original operation."""
        return self.logger.log_operation(
            operation_type="execution_result",
            response=output,
            metadata={
                "parent_operation_id": operation_id,
                "success": success,
                "execution_type": execution_type
            }
        )

def log_ralex_operation(operation_type: str):
    """Decorator to automatically log Ralex operations."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            # Execute the operation
            try:
                result = func(*args, **kwargs)
                success = True
                error = None
            except Exception as e:
                result = None
                success = False
                error = str(e)
                raise
            finally:
                # Log the operation
                duration = time.time() - start_time
                log_ai_operation(
                    operation_type=f"ralex_{operation_type}",
                    metadata={
                        "function_name": func.__name__,
                        "success": success,
                        "duration_seconds": duration,
                        "error": error,
                        "args_count": len(args),
                        "kwargs_keys": list(kwargs.keys())
                    }
                )
            
            return result
        return wrapper
    return decorator

# Integration examples for existing Ralex components:

def integrate_with_ralex_bridge():
    """
    Example integration with ralex_bridge.py
    Add this to your RalexBridge class:
    """
    integration_code = '''
    # Add to ralex_bridge.py imports:
    from ralex_logger_integration import RalexLoggerMixin, log_ralex_operation
    
    # Modify RalexBridge class:
    class RalexBridge(RalexLoggerMixin):
        def __init__(self):
            super().__init__()  # Initialize logger
            # ... existing init code
        
        async def process_request(self, prompt: str) -> dict:
            """Enhanced with logging."""
            thinking = self.apply_agentos_thinking(prompt)
            model = self.select_model_via_litellm(thinking)
            
            # Log the routing decision
            routing_id = self.log_model_routing(
                original_model="auto", 
                selected_model=model,
                reasoning=f"Complexity: {thinking['complexity']}, Code required: {thinking['requires_code']}"
            )
            
            ai_response = self.call_openrouter_via_litellm(prompt, model)
            execution_result = self.execute_via_opencode(ai_response, prompt)
            
            # Log the full operation
            operation_id = self.log_bridge_operation(
                prompt=prompt,
                model=model,
                response=ai_response,
                thinking=thinking
            )
            
            # Log execution if it happened
            if execution_result.get("success"):
                self.log_execution_result(
                    operation_id=operation_id,
                    success=True,
                    execution_type="opencode",
                    output=execution_result.get("output", "")
                )
            
            return {
                "success": True,
                "model_used": model,
                "response": ai_response,
                "execution": execution_result,
                "context_saved": True,
                "operation_id": operation_id  # Return for future reference
            }
    '''
    return integration_code

def integrate_with_ralex_api():
    """
    Example integration with ralex_api.py
    Add logging to FastAPI endpoints:
    """
    integration_code = '''
    # Add to ralex_api.py
    from ralex_logger_integration import log_ai_operation
    
    @app.post("/v1/chat/completions")
    async def chat_completions(request: ChatRequest):
        """Enhanced with logging."""
        try:
            prompt = request.message
            
            # Process through RalexBridge (already logged there)
            result = await bridge.process_request(prompt)
            
            if "error" in result:
                # Log the error
                log_ai_operation(
                    operation_type="api_error",
                    prompt=prompt,
                    metadata={
                        "error": result["error"],
                        "endpoint": "/v1/chat/completions",
                        "client_model": request.model
                    }
                )
                raise HTTPException(status_code=500, detail=result["error"])
            
            # Log successful API call
            log_ai_operation(
                operation_type="api_success",
                prompt=prompt,
                response=result["response"],
                model=result.get("model_used", "unknown"),
                metadata={
                    "endpoint": "/v1/chat/completions",
                    "client_model": request.model,
                    "ralex_operation_id": result.get("operation_id"),
                    "prompt_tokens": len(prompt.split()),
                    "completion_tokens": len(result["response"].split())
                }
            )
            
            # Format response for OpenWebUI (existing code)
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
            # Log unexpected errors
            log_ai_operation(
                operation_type="api_exception",
                metadata={
                    "error": str(e),
                    "endpoint": "/v1/chat/completions",
                    "exception_type": type(e).__name__
                }
            )
            raise HTTPException(status_code=500, detail=str(e))
    '''
    return integration_code

if __name__ == "__main__":
    print("Ralex Logger Integration Examples:")
    print("\n1. RalexBridge Integration:")
    print(integrate_with_ralex_bridge())
    print("\n2. RalexAPI Integration:")
    print(integrate_with_ralex_api())