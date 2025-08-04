#!/usr/bin/env python3
"""
Quick test of the OpenRouter Auto Router implementation
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv


async def test_auto_router():
    """Test OpenRouter Auto Router with a simple request"""
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ No API key found")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Khamel83/ralex",
        "X-Title": "Ralex Auto Router Test"
    }
    
    payload = {
        "model": "openrouter/auto",
        "messages": [{"role": "user", "content": "What is 2+2? Just give a brief answer."}],
        "max_tokens": 50
    }
    
    print("🔄 Testing OpenRouter Auto Router...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    actual_model = result.get("model", "unknown")
                    content = result["choices"][0]["message"]["content"]
                    
                    print(f"✅ Success!")
                    print(f"🤖 Auto Router selected: {actual_model}")
                    print(f"📝 Response: {content}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Error {response.status}: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(test_auto_router())