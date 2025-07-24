#!/usr/bin/env python3
"""
Test script to validate LiteLLM + OpenRouter integration
"""
import os
import sys

# Add venv to path
sys.path.insert(0, '.venv-v2/lib/python3.11/site-packages')

try:
    from litellm import completion
    import openai
    
    # Test basic OpenRouter connection through LiteLLM
    print("🧪 Testing LiteLLM + OpenRouter integration...")
    
    # Check if API key is set
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY not set")
        print("Set it with: export OPENROUTER_API_KEY='your_key'")
        sys.exit(1)
    
    print(f"✅ OpenRouter API key: {api_key[:8]}...")
    
    # Test cheap model (Gemini Flash)
    print("\n🧪 Testing cheap model (Gemini Flash)...")
    try:
        response = completion(
            model="openrouter/google/gemini-flash-1.5",
            messages=[{"role": "user", "content": "Say 'hello' in exactly one word"}],
            api_base="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        print(f"✅ Cheap model response: {response.choices[0].message.content}")
        
        # Estimate cost (rough)
        tokens = len(response.choices[0].message.content.split())
        estimated_cost = tokens * 0.000001  # Rough estimate for Gemini Flash
        print(f"💰 Estimated cost: ${estimated_cost:.6f}")
        
    except Exception as e:
        print(f"❌ Cheap model failed: {e}")
    
    # Test smart model (Claude Sonnet)
    print("\n🧪 Testing smart model (Claude Sonnet)...")
    try:
        response = completion(
            model="openrouter/anthropic/claude-3.5-sonnet",
            messages=[{"role": "user", "content": "Say 'hello' in exactly one word"}],
            api_base="https://openrouter.ai/api/v1", 
            api_key=api_key
        )
        print(f"✅ Smart model response: {response.choices[0].message.content}")
        
        # Estimate cost (rough)
        tokens = len(response.choices[0].message.content.split())
        estimated_cost = tokens * 0.000015  # Rough estimate for Claude Sonnet
        print(f"💰 Estimated cost: ${estimated_cost:.6f}")
        
    except Exception as e:
        print(f"❌ Smart model failed: {e}")
    
    print("\n✅ LiteLLM + OpenRouter integration test complete!")
    print("\n📋 Next steps:")
    print("1. Start LiteLLM proxy: litellm --model openrouter/... --port 4000")
    print("2. Configure OpenCode.ai to use localhost:4000")
    print("3. Test cost-based routing")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("Installing LiteLLM...")
    os.system('.venv-v2/bin/pip install litellm')
    
except Exception as e:
    print(f"❌ Test failed: {e}")