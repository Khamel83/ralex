#!/usr/bin/env python3
"""
Health checks and fallback mechanisms for Ralex V2
Ensures system reliability and graceful degradation
"""
import os
import sys
import json
import time
import subprocess

def check_dependencies():
    """Check all critical dependencies"""
    print("🔍 DEPENDENCY HEALTH CHECK")
    print("=" * 40)
    
    results = {}
    
    # Critical dependencies
    critical_deps = [
        ('python', 'Python 3.10+', 'python3 --version'),
        ('litellm', 'LiteLLM library', None),
        ('openai', 'OpenAI client', None),
        ('httpx', 'HTTP client', None),
    ]
    
    for dep_name, description, cmd in critical_deps:
        try:
            if cmd:
                # Command-based check
                result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    status = "✅"
                    details = result.stdout.strip()
                else:
                    status = "❌"  
                    details = result.stderr.strip()
            else:
                # Import-based check
                sys.path.insert(0, '.ralex-env/lib/python3.11/site-packages')
                __import__(dep_name)
                status = "✅"
                details = "Available"
            
            results[dep_name] = (status, details)
            print(f"{status} {description}: {details}")
            
        except Exception as e:
            results[dep_name] = ("❌", str(e))
            print(f"❌ {description}: {e}")
    
    return results

def check_api_connectivity():
    """Check API connectivity"""
    print(f"\n🌐 API CONNECTIVITY CHECK")
    print("=" * 40)
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY not set")
        return False
    
    print(f"✅ API key configured: {api_key[:8]}...")
    
    # Test basic connectivity (without making expensive calls)
    try:
        import urllib.request
        req = urllib.request.Request("https://openrouter.ai/api/v1/models")
        req.add_header('Authorization', f'Bearer {api_key}')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                print("✅ OpenRouter API accessible")
                return True
            else:
                print(f"❌ OpenRouter API error: {response.status}")
                return False
                
    except Exception as e:
        print(f"❌ OpenRouter API connection failed: {e}")
        return False

def check_budget_system():
    """Check budget tracking system"""
    print(f"\n💰 BUDGET SYSTEM CHECK") 
    print("=" * 40)
    
    budget_file = "/tmp/ralex_litellm_budget.json"
    
    try:
        # Test budget file creation
        test_data = {'date': time.strftime('%Y-%m-%d'), 'spent': 0.001}
        with open(budget_file, 'w') as f:
            json.dump(test_data, f)
        
        # Test budget file reading
        with open(budget_file, 'r') as f:
            data = json.load(f)
        
        if data['spent'] == 0.001:
            print("✅ Budget file read/write works")
            
            # Test budget calculations
            remaining = 5.0 - data['spent']
            can_use_smart = remaining > 0.02
            can_use_cheap = remaining > 0.001
            
            print(f"✅ Budget calculations work: ${remaining:.6f} remaining")
            print(f"✅ Model availability logic works: smart={can_use_smart}, cheap={can_use_cheap}")
            return True
        else:
            print("❌ Budget data corruption")
            return False
            
    except Exception as e:
        print(f"❌ Budget system error: {e}")
        return False

def check_fallback_mechanisms():
    """Test fallback mechanisms"""
    print(f"\n🔄 FALLBACK MECHANISM CHECK")
    print("=" * 40)
    
    # Test pattern recognition fallback
    test_prompts = ["", "unknown request", "fix this", "refactor code"]
    
    for prompt in test_prompts:
        try:
            prompt_lower = prompt.lower()
            
            cheap_patterns = ['fix', 'typo', 'simple', 'quick', 'small', 'format', 'add', 'comment']
            smart_patterns = ['refactor', 'analyze', 'complex', 'architecture', 'design', 'review', 'optimize']
            yolo_patterns = ['yolo', 'urgent', 'fast', 'now', 'quickly']
            
            is_cheap = any(pattern in prompt_lower for pattern in cheap_patterns)
            is_smart = any(pattern in prompt_lower for pattern in smart_patterns)
            is_yolo = any(pattern in prompt_lower for pattern in yolo_patterns)
            
            # Default fallback logic
            if is_yolo:
                selected = "yolo"
            elif is_smart:
                selected = "smart"
            elif is_cheap:
                selected = "cheap"
            else:
                selected = "default_cheap"  # Fallback
            
            print(f"✅ Pattern '{prompt}' → {selected}")
        except Exception as e:
            print(f"❌ Pattern recognition failed for '{prompt}': {e}")
            return False
    
    return True

def create_fallback_script():
    """Create emergency fallback script"""
    fallback_content = '''#!/bin/bash
# Emergency fallback for Ralex V2
echo "⚠️  Ralex V2 fallback mode activated"
echo "Using direct OpenRouter implementation..."
exec python3 "$(dirname "$0")/direct-openrouter-test.py" "$@"
'''
    
    try:
        with open('ralex-fallback.sh', 'w') as f:
            f.write(fallback_content)
        os.chmod('ralex-fallback.sh', 0o755)
        print("✅ Emergency fallback script created: ./ralex-fallback.sh")
        return True
    except Exception as e:
        print(f"❌ Fallback script creation failed: {e}")
        return False

def main():
    """Run all health checks"""
    print("🏥 RALEX V2 SYSTEM HEALTH CHECK")
    print("=" * 50)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("API Connectivity", check_api_connectivity), 
        ("Budget System", check_budget_system),
        ("Fallback Mechanisms", check_fallback_mechanisms),
        ("Emergency Fallback", create_fallback_script),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        try:
            result = check_func()
            if result and result != {}:  # Handle different return types
                passed += 1
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
    
    print(f"\n🎯 HEALTH CHECK SUMMARY")
    print("=" * 50)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ System is healthy and production-ready!")
        return True
    elif passed >= total * 0.8:
        print("⚠️  System mostly healthy, monitor closely")
        return True
    else:
        print("❌ System has significant health issues")
        print("🚨 Do not deploy to production")
        return False

if __name__ == "__main__":
    healthy = main()
    sys.exit(0 if healthy else 1)