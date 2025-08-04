#!/usr/bin/env python3
"""
Test the orchestrator integration with OpenRouter Auto Router
"""

import asyncio
import sys
sys.path.append('.')

from ralex_core.litellm_router import OpenRouterAutoRouter


async def test_orchestrator_integration():
    """Test the OpenRouter Auto Router integration"""
    print("🔄 Testing Orchestrator Auto Router Integration...")
    
    try:
        # Initialize router
        router = OpenRouterAutoRouter()
        await router.initialize()
        
        # Test health check
        health = await router.health_check()
        print(f"🏥 Health check: {health['status']} - {health['message']}")
        
        # Test model selection
        selection = await router.select_model("Test prompt", "simple")
        print(f"🎯 Model selection: {selection.model_name}")
        print(f"💰 Estimated cost: ${selection.estimated_cost}")
        print(f"🧠 Reasoning: {selection.reasoning}")
        
        # Test actual request
        messages = [{"role": "user", "content": "Explain Python in one sentence."}]
        response = await router.send_request(messages)
        
        if response["status"] == "success":
            print(f"✅ Request successful!")
            print(f"🤖 Actual model selected: {response['actual_model']}")
            print(f"📝 Response: {response['content'][:100]}...")
            return True
        else:
            print(f"❌ Request failed: {response['message']}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_orchestrator_integration())
    if success:
        print("\n🎉 All tests passed! Auto Router integration is working!")
    else:
        print("\n💥 Tests failed - check errors above")