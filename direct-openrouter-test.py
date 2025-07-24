#!/usr/bin/env python3
"""
Direct OpenRouter test - bypasses LiteLLM installation issues
Tests the core functionality: budget-aware AI coding with smart routing
"""
import os
import json
import time
import argparse
from urllib.request import Request, urlopen
from urllib.error import URLError

# Budget tracking (simple file-based for testing)
BUDGET_FILE = "/tmp/ralex_budget.json"
DAILY_BUDGET = 5.00

def get_budget_status():
    """Get current budget status"""
    try:
        if os.path.exists(BUDGET_FILE):
            with open(BUDGET_FILE, 'r') as f:
                data = json.load(f)
                # Reset if new day
                if data.get('date') != time.strftime('%Y-%m-%d'):
                    data = {'date': time.strftime('%Y-%m-%d'), 'spent': 0.0}
        else:
            data = {'date': time.strftime('%Y-%m-%d'), 'spent': 0.0}
        
        remaining = DAILY_BUDGET - data['spent']
        return {
            'spent': data['spent'],
            'remaining': remaining,
            'budget': DAILY_BUDGET,
            'can_use_smart': remaining > 0.02,  # Smart models cost ~$0.01
            'can_use_cheap': remaining > 0.001  # Cheap models cost ~$0.0001
        }
    except:
        return {'spent': 0, 'remaining': DAILY_BUDGET, 'budget': DAILY_BUDGET, 'can_use_smart': True, 'can_use_cheap': True}

def update_budget(cost):
    """Update budget with actual cost"""
    try:
        status = get_budget_status()
        new_spent = status['spent'] + cost
        data = {'date': time.strftime('%Y-%m-%d'), 'spent': new_spent}
        with open(BUDGET_FILE, 'w') as f:
            json.dump(data, f)
    except:
        pass

def select_model(prompt):
    """Smart model selection based on prompt patterns"""
    prompt_lower = prompt.lower()
    budget = get_budget_status()
    
    # Pattern-based routing (same as litellm_budget_config.yaml)
    cheap_patterns = ['fix', 'typo', 'simple', 'quick', 'small', 'format', 'add', 'comment']
    smart_patterns = ['refactor', 'analyze', 'complex', 'architecture', 'design', 'review', 'optimize']
    yolo_patterns = ['yolo', 'urgent', 'fast', 'now', 'quickly']
    
    # Check patterns
    is_cheap = any(pattern in prompt_lower for pattern in cheap_patterns)
    is_smart = any(pattern in prompt_lower for pattern in smart_patterns)
    is_yolo = any(pattern in prompt_lower for pattern in yolo_patterns)
    
    # Budget-aware selection
    if not budget['can_use_cheap']:
        return None, "❌ Budget exceeded ($5 daily limit)"
    
    if is_yolo:
        return "google/gemini-flash-1.5", "⚡ YOLO mode - Ultra fast"
    elif is_smart and budget['can_use_smart']:
        return "anthropic/claude-3-sonnet", "🧠 Smart mode - Complex analysis"
    elif is_cheap or not budget['can_use_smart']:
        return "google/gemini-flash-1.5", "💰 Cheap mode - Simple task"
    else:
        return "google/gemini-flash-1.5", "💰 Budget-limited - Using cheap model"

def call_openrouter(model, prompt):
    """Make API call to OpenRouter"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        return "❌ OPENROUTER_API_KEY not set"
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }
    
    try:
        req = Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(data).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'http://localhost:3000',
                'X-Title': 'Ralex V2 Budget Test'
            }
        )
        
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # Extract response and usage
            message = result['choices'][0]['message']['content']
            usage = result.get('usage', {})
            
            # Estimate cost (approximate)
            if 'gemini' in model:
                cost = usage.get('total_tokens', 100) * 0.000001  # ~$0.000001 per token
            else:
                cost = usage.get('total_tokens', 100) * 0.000015  # ~$0.000015 per token
            
            update_budget(cost)
            
            return f"✅ Response: {message}\n\n💰 Cost: ${cost:.6f} | Tokens: {usage.get('total_tokens', '?')}"
            
    except URLError as e:
        return f"❌ Network error: {e}"
    except Exception as e:
        return f"❌ Error: {e}"

def main():
    parser = argparse.ArgumentParser(description='Ralex V2 Direct Test - Budget-Aware AI Coding')
    parser.add_argument('prompt', help='Your coding request')
    parser.add_argument('--budget', action='store_true', help='Show budget status only')
    parser.add_argument('--model', help='Force specific model')
    
    args = parser.parse_args()
    
    if args.budget:
        budget = get_budget_status()
        print(f"📊 Budget Status:")
        print(f"   Spent today: ${budget['spent']:.6f}")
        print(f"   Remaining: ${budget['remaining']:.6f}")
        print(f"   Daily limit: ${budget['budget']:.2f}")
        print(f"   Can use smart models: {'✅' if budget['can_use_smart'] else '❌'}")
        print(f"   Can use cheap models: {'✅' if budget['can_use_cheap'] else '❌'}")
        return
    
    print("🚀 Ralex V2 - Budget-Aware AI Coding Assistant")
    print("=" * 50)
    
    # Budget check
    budget = get_budget_status()
    print(f"💰 Budget: ${budget['remaining']:.6f} remaining of ${budget['budget']:.2f}")
    
    # Model selection
    if args.model:
        model = args.model
        reasoning = f"🎯 User override: {model}"
    else:
        model, reasoning = select_model(args.prompt)
    
    if not model:
        print(reasoning)
        return
    
    print(f"🤖 {reasoning}")
    print(f"📝 Model: {model}")
    print(f"❓ Prompt: {args.prompt}")
    print("-" * 50)
    
    # Make the call
    response = call_openrouter(model, args.prompt)
    print(response)
    
    # Show updated budget
    budget = get_budget_status()
    print(f"\n💰 Updated budget: ${budget['remaining']:.6f} remaining")

if __name__ == "__main__":
    main()