# Ralex V2: CORRECTED Stack (OpenCode.ai + LiteLLM + AgentOS)

## Correct V2 Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   OpenCode.ai   │───▶│   LiteLLM    │───▶│ OpenRouter  │
│   (Terminal UI  │    │   Proxy      │    │ (Models)    │
│   + Yolo Mode)  │    │ (Routing)    │    │             │
└─────────────────┘    └──────────────┘    └─────────────┘
         │
         ▼
┌─────────────────┐
│   AgentOS       │
│   (Standards &  │
│    Workflows)   │
└─────────────────┘
```

## Component Roles (CORRECTED)
- **OpenCode.ai**: Terminal coding interface with "yolo" execution mode
- **LiteLLM**: Cost-optimized routing to OpenRouter only
- **AgentOS**: Development standards and workflow patterns  
- **OpenRouter**: Unified API to all models (Claude, GPT, etc.)

## Minimal Config Files (Target: <100 lines total)

### 1. LiteLLM Config (OpenRouter Only)
```yaml
# litellm_openrouter.yaml (~40 lines)
model_list:
  - model_name: "cheap"
    litellm_params:
      model: "openrouter/google/gemini-flash-1.5"
      api_base: "https://openrouter.ai/api/v1"
      api_key: "${OPENROUTER_API_KEY}"
  
  - model_name: "smart"
    litellm_params:
      model: "openrouter/anthropic/claude-3.5-sonnet"
      api_base: "https://openrouter.ai/api/v1" 
      api_key: "${OPENROUTER_API_KEY}"

router_settings:
  routing_strategy: "cost-based-routing"
  fallbacks:
    - ["cheap", "smart"]
  budget_manager:
    daily_limit: 5.00
    
# Route simple tasks to cheap models
routing_rules:
  - pattern: "fix|typo|simple|quick"
    model: "cheap"
  - pattern: "refactor|complex|analyze|review"
    model: "smart"
```

### 2. Yolo Launcher Script
```bash
#!/bin/bash
# yolo-ralex.sh (~15 lines)
export OPENROUTER_API_KEY="$OPENROUTER_API_KEY"

# Start LiteLLM proxy (OpenRouter only)
litellm --config litellm_openrouter.yaml --port 4000 &
sleep 2

# Launch OpenCode.ai with proxy
opencode --llm-proxy http://localhost:4000 --yolo-mode

echo "🚀 Yolo Ralex V2: OpenCode + LiteLLM + OpenRouter"
```

### 3. AgentOS Integration Script  
```bash
#!/bin/bash
# setup-agentos.sh (~20 lines)
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup.sh | bash

# Custom standards for OpenCode.ai
cat > ~/.agent-os/standards/opencode-integration.md << EOF
# OpenCode.ai Integration Standards

## Yolo Mode Guidelines
- Use 'cheap' models for simple fixes/typos
- Use 'smart' models for complex refactoring
- Always route through LiteLLM proxy at localhost:4000

## Cost Optimization
- Daily budget: $5.00
- Alert at: $4.00  
- Prefer gemini-flash for speed, claude-sonnet for quality
EOF
```

### 4. Simple Cost Tracker
```python
# cost_tracker.py (~30 lines)
import json
from datetime import datetime

class SimpleBudget:
    def __init__(self, daily_limit=5.0):
        self.daily_limit = daily_limit
        self.spend_file = "daily_spend.json"
    
    def log_request(self, model, cost):
        today = datetime.now().strftime("%Y-%m-%d")
        try:
            with open(self.spend_file, 'r') as f:
                data = json.load(f)
        except:
            data = {}
        
        if today not in data:
            data[today] = {"total": 0, "requests": []}
        
        data[today]["total"] += cost
        data[today]["requests"].append({"model": model, "cost": cost, "time": datetime.now().isoformat()})
        
        with open(self.spend_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        if data[today]["total"] > self.daily_limit:
            print(f"⚠️  Daily budget exceeded: ${data[today]['total']:.3f}")
        
        return data[today]["total"]

if __name__ == "__main__":
    tracker = SimpleBudget()
    print(f"Today's spend: ${tracker.log_request('test', 0):.3f}")
```

## Test Implementation Plan

### Step 1: Install OpenCode.ai
```bash
# How do we install OpenCode.ai? Need to check their docs
npm install -g opencode-ai  # or pip install opencode-ai?
```

### Step 2: Test LiteLLM with OpenRouter Only
```bash
python -m venv .venv-v2
source .venv-v2/bin/activate
pip install litellm

# Test OpenRouter connection
export OPENROUTER_API_KEY="your_key"
litellm --model openrouter/google/gemini-flash-1.5 --api_base https://openrouter.ai/api/v1
```

### Step 3: Test Integration
```bash
# Start proxy
litellm --config litellm_openrouter.yaml --port 4000 &

# Test with OpenCode.ai
opencode --llm-proxy http://localhost:4000
```

## What We're Testing/Validating

1. **OpenCode.ai installation method** - npm? pip? 
2. **LiteLLM → OpenRouter compatibility** - does routing work?
3. **Cost tracking integration** - can we intercept requests?
4. **Yolo mode activation** - does OpenCode.ai have this flag?

## Target: <100 Lines Total Config

Current estimate:
- `litellm_openrouter.yaml`: 40 lines
- `yolo-ralex.sh`: 15 lines  
- `setup-agentos.sh`: 20 lines
- `cost_tracker.py`: 30 lines
- **Total**: 105 lines (close to target!)

## Questions to Resolve

1. How exactly do we install OpenCode.ai?
2. Does OpenCode.ai support `--llm-proxy` flag?
3. Does it have `--yolo-mode` or equivalent?
4. Can LiteLLM intercept and route OpenCode.ai requests?

Let's test these components one by one!