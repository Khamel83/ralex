#!/usr/bin/env python

import os
import sys
import json
import httpx

from .free_model_selector import NoAvailableFreeModelsError


class OpenRouterClient:
    """A simplified client for making requests to the OpenRouter API."""

    def __init__(self, api_key, model_tiers=None, free_model_selector=None, free_mode_enabled: bool = False):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.model_tiers = model_tiers if model_tiers is not None else {}
        self.free_model_selector = free_model_selector
        self.free_mode_enabled = free_mode_enabled

    async def send_request(self, model, messages, task_complexity: str = "medium", context_size: int = 4096):
        """Sends a request to the specified model and streams the response."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        actual_model = model
        if self.free_mode_enabled and self.free_model_selector:
            if model == "free_base":
                try:
                    selected_free_model = await self.free_model_selector.select_model(task_complexity='simple', context_size=context_size)
                    actual_model = selected_free_model['id']
                except NoAvailableFreeModelsError:
                    print("\n⚠️ No free models available for free_base tier. Using default paid model.")
                    # Fallback to a default paid model if no free model is available
                    actual_model = "openrouter/anthropic/claude-3-haiku" # Example fallback
            elif model == "free_good":
                try:
                    selected_free_model = await self.free_model_selector.select_model(task_complexity='complex', context_size=context_size)
                    actual_model = selected_free_model['id']
                except NoAvailableFreeModelsError:
                    print("\n⚠️ No free models available for free_good tier. Using default paid model.")
                    # Fallback to a default paid model if no free model is available
                    actual_model = "openrouter/anthropic/claude-3.5-sonnet" # Example fallback

        data = {
            "model": actual_model,
            "messages": messages,
            "stream": True,
        }

        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", f"{self.base_url}/chat/completions", headers=headers, json=data, timeout=None) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes():
                        decoded_chunk = chunk.decode("utf-8")
                        for line in decoded_chunk.splitlines():
                            if line.startswith("data: "):
                                json_str = line[len("data: ") :]
                                if json_str.strip() == "[DONE]":
                                    break
                                try:
                                    json_obj = json.loads(json_str)
                                    if "choices" in json_obj and json_obj["choices"]:
                                        if (
                                            "delta" in json_obj["choices"][0]
                                            and "content" in json_obj["choices"][0]["delta"]
                                        ):
                                            yield json_obj["choices"][0]["delta"]["content"]
                                except json.JSONDecodeError:
                                    # Ignore chunks that are not valid JSON
                                    pass
        except httpx.RequestError as e:
            print(f"\nError making request to OpenRouter: {e}", file=sys.stderr)
            return
