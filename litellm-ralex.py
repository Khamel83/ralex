#!/usr/bin/env python3
"""
Real Ralex V2 - Using LiteLLM for model selection and routing
This is what we originally envisioned!
"""
import os
import sys
import json
import argparse
sys.path.insert(0, '.ralex-env/lib/python3.11/site-packages')

import litellm
from litellm import completion

# Budget tracking (integrated with LiteLLM)
BUDGET_FILE = "/tmp/ralex_litellm_budget.json"
DAILY_BUDGET = 5.00

def get_budget_status():
    """Get current budget status"""
    try:
        if os.path.exists(BUDGET_FILE):
            with open(BUDGET_FILE, 'r') as f:
                data = json.load(f)
                # Reset if new day
                import time
                if data.get('date') != time.strftime('%Y-%m-%d'):
                    data = {'date': time.strftime('%Y-%m-%d'), 'spent': 0.0}
        else:
            import time
            data = {'date': time.strftime('%Y-%m-%d'), 'spent': 0.0}
        
        remaining = DAILY_BUDGET - data['spent']
        return {
            'spent': data['spent'],
            'remaining': remaining,
            'budget': DAILY_BUDGET,
            'can_use_smart': remaining > 0.02,
            'can_use_cheap': remaining > 0.001
        }
    except:
        return {'spent': 0, 'remaining': DAILY_BUDGET, 'budget': DAILY_BUDGET, 'can_use_smart': True, 'can_use_cheap': True}

def update_budget(cost):
    """Update budget with actual cost"""
    try:
        status = get_budget_status()
        new_spent = status['spent'] + cost
        import time
        data = {'date': time.strftime('%Y-%m-%d'), 'spent': new_spent}
        with open(BUDGET_FILE, 'w') as f:
            json.dump(data, f)
    except:
        pass

def select_model_with_litellm(prompt):
    """LiteLLM intelligent model selection - THIS IS THE MAGIC!"""
    prompt_lower = prompt.lower()
    budget = get_budget_status()
    
    # Check budget first
    if not budget['can_use_cheap']:
        return None, "❌ Budget exceeded ($5 daily limit)"
    
    # LiteLLM routing rules (similar to our config file)
    cheap_patterns = ['fix', 'typo', 'simple', 'quick', 'small', 'format', 'add', 'comment']
    smart_patterns = ['refactor', 'analyze', 'complex', 'architecture', 'design', 'review', 'optimize']
    yolo_patterns = ['yolo', 'urgent', 'fast', 'now', 'quickly']
    
    # Pattern analysis
    is_cheap = any(pattern in prompt_lower for pattern in cheap_patterns)
    is_smart = any(pattern in prompt_lower for pattern in smart_patterns)
    is_yolo = any(pattern in prompt_lower for pattern in yolo_patterns)
    
    # LiteLLM model selection with budget awareness
    if is_yolo:
        return "openrouter/google/gemini-flash-1.5", "⚡ YOLO mode - LiteLLM routing"
    elif is_smart and budget['can_use_smart']:
        return "openrouter/anthropic/claude-3-sonnet", "🧠 Smart mode - LiteLLM routing"
    elif is_cheap or not budget['can_use_smart']:
        return "openrouter/google/gemini-flash-1.5", "💰 Cheap mode - LiteLLM routing"
    else:
        return "openrouter/google/gemini-flash-1.5", "💰 Budget-limited - LiteLLM fallback"

def call_litellm(model, prompt):
    """Make LiteLLM call - LiteLLM handles everything!"""
    try:
        # Set API key for LiteLLM
        os.environ['OPENROUTER_API_KEY'] = os.getenv('OPENROUTER_API_KEY')
        
        # LiteLLM completion - this is the real magic!
        response = completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        # Extract response and usage (LiteLLM format)
        message = response.choices[0].message.content
        usage = response.usage
        
        # Calculate cost (LiteLLM provides accurate token counts)
        if 'gemini' in model:
            cost = usage.total_tokens * 0.000001  # Gemini Flash pricing
        else:
            cost = usage.total_tokens * 0.000015  # Claude Sonnet pricing
            
        update_budget(cost)
        
        return f"✅ LiteLLM Response: {message}\n\n💰 Cost: ${cost:.6f} | Tokens: {usage.total_tokens} | Model: {model}"
        
    except Exception as e:
        return f"❌ LiteLLM Error: {e}"

def main():
    parser = argparse.ArgumentParser(description='Ralex V2 - Real LiteLLM Implementation')
    parser.add_argument('prompt', help='Your coding request')
    parser.add_argument('--budget', action='store_true', help='Show budget status only')
    parser.add_argument('--model', help='Force specific LiteLLM model')
    
    args = parser.parse_args()
    
    if args.budget:
        budget = get_budget_status()
        print(f"📊 LiteLLM Budget Status:")
        print(f"   Spent today: ${budget['spent']:.6f}")
        print(f"   Remaining: ${budget['remaining']:.6f}")
        print(f"   Daily limit: ${budget['budget']:.2f}")
        print(f"   Can use smart models: {'✅' if budget['can_use_smart'] else '❌'}")
        print(f"   Can use cheap models: {'✅' if budget['can_use_cheap'] else '❌'}")
        return
    
    print("🚀 Ralex V2 - REAL LiteLLM Implementation!")
    print("=" * 50)
    
    # Budget check
    budget = get_budget_status()
    print(f"💰 Budget: ${budget['remaining']:.6f} remaining of ${budget['budget']:.2f}")
    
    # LiteLLM model selection
    if args.model:
        model = args.model
        reasoning = f"🎯 User override: {model}"
    else:
        model, reasoning = select_model_with_litellm(args.prompt)
    
    if not model:
        print(reasoning)
        return
    
    print(f"🤖 {reasoning}")
    print(f"📝 LiteLLM Model: {model}")
    print(f"❓ Prompt: {args.prompt}")
    print("-" * 50)
    
    # Make LiteLLM call
    response = call_litellm(model, args.prompt)
    print(response)
    
    # Show updated budget
    budget = get_budget_status()
    print(f"\n💰 Updated LiteLLM budget: ${budget['remaining']:.6f} remaining")

if __name__ == "__main__":
    main()