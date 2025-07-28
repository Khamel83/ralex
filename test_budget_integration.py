#!/usr/bin/env python3
import asyncio
from ralex_bridge import RalexBridge

async def test_budget_enforcement():
    bridge = RalexBridge()
    
    print('🧪 Testing Budget Enforcement Integration')
    
    # Test 1: Normal query within budget
    result1 = await bridge.process_request('what is python')
    print(f'Normal query success: {result1.get("success", False)}')
    if 'budget_info' in result1:
        print(f'Cost tracking: ${result1["budget_info"]["estimated_cost"]:.4f}')
    
    # Test 2: Set very low budget and test enforcement
    if bridge.budget_enforcer:
        bridge.budget_enforcer.daily_limit = 0.001  # Very low limit
        
        result2 = await bridge.process_request('refactor this complex architecture with microservices and distributed systems')
        
        if 'error' in result2:
            print(f'✅ Budget enforcement working: {result2["error"]}')
            if 'budget_status' in result2:
                print(f'Budget details: {result2["budget_status"]["reason"]}')
        else:
            print('❌ Budget enforcement failed - query should have been blocked')
    
    print('✅ Budget enforcement testing complete')

if __name__ == "__main__":
    asyncio.run(test_budget_enforcement())