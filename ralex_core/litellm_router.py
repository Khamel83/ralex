"""
OpenRouter Auto Router - Direct Integration

Replaces LiteLLM with direct OpenRouter API calls using their Auto Router
powered by NotDiamond for quality-per-dollar optimization.
"""

import asyncio
import logging
import os
import aiohttp
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class ModelSelection:
    """Model selection result"""

    model_name: str
    estimated_cost: float = 0.0
    reasoning: str = ""
    provider: str = "openrouter"


class OpenRouterAutoRouter:
    """Direct OpenRouter integration with Auto Router"""

    def __init__(self, api_key: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        
        if not self.api_key:
            raise ValueError("OpenRouter API key not found. Set OPENROUTER_API_KEY environment variable.")

    async def initialize(self):
        """Initialize OpenRouter Auto Router"""
        self.logger.info("OpenRouter Auto Router initialized with NotDiamond quality-per-dollar optimization")

    async def select_model(self, enhanced_prompt, complexity: str) -> ModelSelection:
        """
        Use OpenRouter Auto Router (NotDiamond) for optimal quality-per-dollar selection.
        The complexity parameter is ignored since Auto Router makes intelligent decisions.
        """
        return ModelSelection(
            model_name="openrouter/auto",
            estimated_cost=0.0001,  # Auto Router optimizes cost dynamically
            reasoning="Using OpenRouter Auto Router (NotDiamond) for optimal quality-per-dollar selection",
            provider="openrouter"
        )

    async def send_request(self, messages: list, model: str = "openrouter/auto", 
                          max_tokens: int = 1000, temperature: float = 0.7) -> Dict[str, Any]:
        """Send request directly to OpenRouter API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/Khamel83/ralex",
            "X-Title": "Ralex AI Assistant"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # Log which model was actually selected by Auto Router
                        actual_model = result.get("model", "unknown")
                        self.logger.info(f"OpenRouter Auto Router selected: {actual_model}")
                        
                        return {
                            "status": "success",
                            "response": result,
                            "actual_model": actual_model,
                            "content": result["choices"][0]["message"]["content"]
                        }
                    else:
                        error_text = await response.text()
                        self.logger.error(f"OpenRouter API error {response.status}: {error_text}")
                        return {
                            "status": "error",
                            "message": f"API error {response.status}: {error_text}"
                        }
                        
            except Exception as e:
                self.logger.error(f"OpenRouter request failed: {e}")
                return {
                    "status": "error",
                    "message": f"Request failed: {str(e)}"
                }

    async def get_session_budget(self, session_id: str) -> float:
        """Get session budget - configurable default"""
        return float(os.getenv("RALEX_SESSION_BUDGET", "5.0"))

    async def health_check(self) -> Dict[str, Any]:
        """Health check for OpenRouter connection"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/models",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        return {
                            "status": "healthy", 
                            "message": "OpenRouter Auto Router operational"
                        }
                    else:
                        return {
                            "status": "unhealthy",
                            "message": f"API returned status {response.status}"
                        }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Health check failed: {str(e)}"
            }

    async def shutdown(self):
        """Shutdown router - no cleanup needed for direct API calls"""
        self.logger.info("OpenRouter Auto Router shutdown complete")
