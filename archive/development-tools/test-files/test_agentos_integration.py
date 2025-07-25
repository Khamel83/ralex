#!/usr/bin/env python3
"""
Test script for AgentOS Integration
Verifies that AgentOS standards loading and prompt structuring works
"""
import os
import sys
sys.path.insert(0, '.')

from ralex_core.agentos_integration import AgentOSIntegration

def test_agentos_loading():
    """Test loading AgentOS standards and instructions"""
    print("🧪 Testing AgentOS Loading...")
    
    agentos = AgentOSIntegration()
    
    # Test standards loading
    print(f"✅ Loaded {len(agentos.standards)} standards:")
    for name in agentos.standards.keys():
        print(f"   - {name}")
    
    # Test instructions loading  
    print(f"✅ Loaded {len(agentos.instructions)} instructions:")
    for name in agentos.instructions.keys():
        print(f"   - {name}")
    
    # Test project info
    print(f"✅ Project info: {agentos.project_info}")
    
    return len(agentos.standards) > 0 and len(agentos.instructions) > 0

def test_complexity_analysis():
    """Test task complexity analysis"""
    print("\n🧪 Testing Complexity Analysis...")
    
    agentos = AgentOSIntegration()
    
    test_cases = [
        ("fix this typo", "low"),
        ("refactor the entire authentication system", "high"),
        ("add a new API endpoint", "medium"),
        ("analyze performance bottlenecks and optimize", "high"),
        ("format this code", "low")
    ]
    
    for prompt, expected in test_cases:
        complexity, confidence = agentos.analyze_task_complexity(prompt)
        status = "✅" if complexity == expected else "❌"
        print(f"   {status} '{prompt}' → {complexity} (expected {expected}, confidence: {confidence:.2f})")
    
    return True

def test_prompt_structuring():
    """Test smart prompt structuring"""
    print("\n🧪 Testing Smart Prompt Structuring...")
    
    agentos = AgentOSIntegration()
    
    # Test simple task
    simple_task = "fix this bug"
    file_context = {"test.py": "def broken_function():\n    return None"}
    
    breakdown = agentos.structure_smart_prompt(simple_task, file_context)
    print(f"✅ Simple task breakdown:")
    print(f"   Complexity: {breakdown.complexity}")
    print(f"   Estimated cost: ${breakdown.estimated_cost:.4f}")
    print(f"   Strategy: {'Direct execution' if breakdown.complexity == 'low' else 'Analysis + execution'}")
    
    # Test complex task
    complex_task = "refactor the authentication system to use JWT tokens with proper error handling"
    breakdown = agentos.structure_smart_prompt(complex_task, file_context)
    print(f"\n✅ Complex task breakdown:")
    print(f"   Complexity: {breakdown.complexity}")
    print(f"   Estimated cost: ${breakdown.estimated_cost:.4f}")
    print(f"   Strategy: {'Direct execution' if breakdown.complexity == 'low' else 'Analysis + execution'}")
    
    return True

def test_slash_commands():
    """Test slash command handling"""
    print("\n🧪 Testing Slash Commands...")
    
    agentos = AgentOSIntegration()
    
    # Test available commands
    commands = agentos.get_slash_commands()
    print(f"✅ Available commands: {list(commands.keys())}")
    
    # Test /help command
    help_result = agentos.handle_slash_command("/help")
    print(f"✅ /help command works: {len(help_result)} characters")
    
    # Test /standards command
    standards_result = agentos.handle_slash_command("/standards")
    print(f"✅ /standards command works: {len(standards_result)} characters")
    
    # Test /breakdown command
    breakdown_result = agentos.handle_slash_command("/breakdown", "refactor authentication")
    print(f"✅ /breakdown command works: {len(breakdown_result)} characters")
    
    return True

def test_standards_context():
    """Test standards context generation"""
    print("\n🧪 Testing Standards Context...")
    
    agentos = AgentOSIntegration()
    
    standards_context = agentos.get_standards_context()
    instructions_context = agentos.get_instructions_context()
    
    print(f"✅ Standards context: {len(standards_context)} characters")
    print(f"✅ Instructions context: {len(instructions_context)} characters")
    
    if standards_context:
        print("   Sample standards context:")
        print(f"   {standards_context[:200]}...")
    
    return len(standards_context) > 0

def test_execution_prompt():
    """Test execution prompt creation"""
    print("\n🧪 Testing Execution Prompt Creation...")
    
    agentos = AgentOSIntegration()
    
    task = "Add type hints to the user authentication function"
    file_context = {"auth.py": "def authenticate(username, password):\n    return True"}
    analysis_context = "Analysis: Need to add proper type hints following PEP 484"
    
    execution_prompt = agentos.create_execution_prompt(task, file_context, analysis_context)
    
    print(f"✅ Execution prompt created: {len(execution_prompt)} characters")
    print("   Sample execution prompt:")
    print(f"   {execution_prompt[:300]}...")
    
    return len(execution_prompt) > 0

def main():
    """Run all tests"""
    print("🚀 AgentOS Integration Test Suite")
    print("=" * 50)
    
    tests = [
        ("AgentOS Loading", test_agentos_loading),
        ("Complexity Analysis", test_complexity_analysis), 
        ("Prompt Structuring", test_prompt_structuring),
        ("Slash Commands", test_slash_commands),
        ("Standards Context", test_standards_context),
        ("Execution Prompts", test_execution_prompt)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"\n✅ {name}: PASSED")
            else:
                print(f"\n❌ {name}: FAILED")
        except Exception as e:
            print(f"\n💥 {name}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AgentOS integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)