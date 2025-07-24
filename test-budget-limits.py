#!/usr/bin/env python3
"""Test budget limits and fallback behavior"""
import json
import os

BUDGET_FILE = "/tmp/ralex_budget.json"

def set_budget(spent):
    """Manually set budget to test limits"""
    data = {'date': '2025-07-24', 'spent': spent}
    with open(BUDGET_FILE, 'w') as f:
        json.dump(data, f)

def test_scenario(spent, description):
    print(f"\n🧪 Testing: {description}")
    print(f"   Setting spent to: ${spent:.6f}")
    set_budget(spent)
    
    # Test smart request (should fail when budget too low)
    os.system('python3 direct-openrouter-test.py "refactor complex code" | head -n 6')

# Test scenarios
print("🧪 BUDGET LIMIT TESTING")
print("=" * 50)

# Normal budget
test_scenario(0.0, "Full budget available")

# Low budget (can't use smart models)  
test_scenario(4.99, "Low budget - should use cheap models only")

# Very low budget (can't use any models)
test_scenario(4.999, "Very low budget - should block requests")

# Exceeded budget
test_scenario(5.01, "Exceeded budget - should block all requests")

print(f"\n✅ Budget testing complete!")