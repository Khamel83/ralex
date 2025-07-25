#!/usr/bin/env python3
"""
Test script for Ralex V3 integration
Tests the backend API and basic functionality
"""

import requests
import json
import time
import subprocess
import signal
import sys
import os

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Version: {data.get('version')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_models_endpoint():
    """Test the models listing endpoint"""
    try:
        response = requests.get("http://localhost:8000/v1/models", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [model['id'] for model in data.get('data', [])]
            print("✅ Models endpoint working")
            print(f"   Available models: {', '.join(models)}")
            return True
        else:
            print(f"❌ Models endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Models endpoint failed: {e}")
        return False

def test_chat_completion():
    """Test the chat completion endpoint"""
    try:
        payload = {
            "model": "ralex-smart",
            "messages": [
                {"role": "user", "content": "Hello, test message"}
            ],
            "stream": False,
            "user": "test_user"
        }
        
        response = requests.post(
            "http://localhost:8000/v1/chat/completions",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer ralex-api-key"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            message = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            print("✅ Chat completion working")
            print(f"   Response: {message[:100]}...")
            return True
        else:
            print(f"❌ Chat completion failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Chat completion failed: {e}")
        return False

def start_backend():
    """Start the backend server"""
    print("Starting Ralex V3 backend...")
    
    # Change to the correct directory
    os.chdir("/home/RPI3/ralex")
    
    # Start the backend
    process = subprocess.Popen(
        [sys.executable, "-m", "ralex_core.openai_api"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for startup
    time.sleep(5)
    
    return process

def main():
    print("🧪 Testing Ralex V3 Integration")
    print("=" * 40)
    
    # Start backend
    backend_process = start_backend()
    
    try:
        # Test endpoints
        tests = [
            ("Health Check", test_health_check),
            ("Models Endpoint", test_models_endpoint),
            ("Chat Completion", test_chat_completion),
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\nTesting {test_name}...")
            success = test_func()
            results.append((test_name, success))
        
        # Print summary
        print("\n" + "=" * 40)
        print("📊 Test Results:")
        passed = 0
        for test_name, success in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {test_name}: {status}")
            if success:
                passed += 1
        
        print(f"\nPassed: {passed}/{len(results)} tests")
        
        if passed == len(results):
            print("\n🎉 All tests passed! Ralex V3 is working correctly.")
        else:
            print("\n⚠️  Some tests failed. Check the logs for details.")
        
    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
    
    finally:
        # Cleanup
        print("\nCleaning up...")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
        print("✅ Cleanup complete")

if __name__ == "__main__":
    main()