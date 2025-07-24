#!/usr/bin/env python3
"""
Quick Integration Test for Ralex V2
Tests OpenCode.ai + LiteLLM + OpenRouter without full installation
"""
import subprocess
import os
import sys
import json

def test_opencode_functionality():
    """Test 1.1.1: OpenCode.ai basic functionality"""
    print("🧪 Testing OpenCode.ai...")
    
    # Test if opencode is available
    try:
        result = subprocess.run(
            ["opencode", "--version"], 
            capture_output=True, 
            text=True,
            env={**os.environ, "PATH": "/home/RPI3/.opencode/bin:" + os.environ.get("PATH", "")}
        )
        
        if result.returncode == 0:
            print(f"✅ OpenCode.ai version: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ OpenCode.ai failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ OpenCode.ai not found in PATH")
        return False

def test_openrouter_connectivity():
    """Test 1.1.3: Direct OpenRouter connectivity"""
    print("\n🧪 Testing OpenRouter connectivity...")
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("⚠️ OPENROUTER_API_KEY not set - skipping connectivity test")
        return False
    
    print(f"✅ API key available: {api_key[:8]}...")
    
    # Simple curl test to OpenRouter
    curl_cmd = [
        "curl", "-s", "-X", "POST", 
        "https://openrouter.ai/api/v1/chat/completions",
        "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "X-Title: Ralex-V2-Test",
        "-d", json.dumps({
            "model": "google/gemini-flash-1.5",
            "messages": [{"role": "user", "content": "Say 'test' in one word"}],
            "max_tokens": 5
        })
    ]
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            try:
                response = json.loads(result.stdout)
                if 'choices' in response:
                    content = response['choices'][0]['message']['content']
                    print(f"✅ OpenRouter response: {content}")
                    return True
                else:
                    print(f"⚠️ Unexpected response: {result.stdout}")
                    return False
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON response: {result.stdout}")
                return False
        else:
            print(f"❌ Request failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_model_selection():
    """Test OpenCode.ai model selection capability"""
    print("\n🧪 Testing OpenCode.ai model selection...")
    
    try:
        # Test help output for model options
        result = subprocess.run(
            ["opencode", "--help"], 
            capture_output=True, 
            text=True,
            env={**os.environ, "PATH": "/home/RPI3/.opencode/bin:" + os.environ.get("PATH", "")}
        )
        
        if result.returncode == 0:
            help_text = result.stdout
            if "--model" in help_text:
                print("✅ Model selection available via --model flag")
                return True
            else:
                print("⚠️ No --model flag found in help")
                return False
        else:
            print(f"❌ Help command failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing model selection: {e}")
        return False

def main():
    print("🚀 Ralex V2 Quick Integration Test")
    print("=" * 50)
    
    # Track results
    results = {}
    
    # Test 1: OpenCode.ai functionality
    results['opencode'] = test_opencode_functionality()
    
    # Test 2: Model selection capability
    results['model_selection'] = test_model_selection()
    
    # Test 3: OpenRouter connectivity
    results['openrouter'] = test_openrouter_connectivity()
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("-" * 30)
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test:20}: {status}")
    
    # Overall assessment
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Ready for Phase 1.2 (Integration Testing)")
        return True
    elif passed_tests >= 2:
        print("⚠️ Most tests passed. Can proceed with caution.")
        return True
    else:
        print("❌ Major issues found. Need to resolve before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)