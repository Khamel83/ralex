#!/usr/bin/env python3
"""Test LiteLLM with our original vision"""
import os
import sys
sys.path.insert(0, '.ralex-env/lib/python3.11/site-packages')

import litellm
from litellm import completion

# Set API key
os.environ['OPENROUTER_API_KEY'] = os.getenv('OPENROUTER_API_KEY')

def test_litellm_routing():
    """Test LiteLLM's built-in routing"""
    print("🧪 Testing LiteLLM direct routing...")
    
    try:
        # Simple request - should use cheap model
        print("\n💰 Testing cheap routing:")
        response = completion(
            model="openrouter/google/gemini-flash-1.5",
            messages=[{"role": "user", "content": "fix this simple bug"}],
            max_tokens=50
        )
        print(f"✅ Response: {response.choices[0].message.content[:100]}...")
        print(f"📊 Usage: {response.usage}")
        
        # Complex request - should use smart model  
        print("\n🧠 Testing smart routing:")
        response = completion(
            model="openrouter/anthropic/claude-3-sonnet",
            messages=[{"role": "user", "content": "refactor this complex architecture"}],
            max_tokens=50
        )
        print(f"✅ Response: {response.choices[0].message.content[:100]}...")
        print(f"📊 Usage: {response.usage}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 LiteLLM Integration Test")
    print("=" * 50)
    
    if test_litellm_routing():
        print("\n✅ LiteLLM is working! We can now build the real system!")
    else:
        print("\n❌ LiteLLM test failed - network or config issues")