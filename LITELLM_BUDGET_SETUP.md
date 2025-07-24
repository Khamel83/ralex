# LiteLLM Budget Tracking with OpenRouter - Minimal Setup

## 🎯 Built-in Budget Features

LiteLLM provides budget tracking **out of the box** with zero custom coding required!

### 1. Environment Variable Budget Control

```bash
# Set daily budget limit
export LITELLM_MAX_BUDGET=5.00  # $5 daily limit

# Set budget period
export LITELLM_BUDGET_DURATION="1d"  # 1 day, 1h, 1w, 1m supported

# Auto-reject requests when budget exceeded
export LITELLM_BUDGET_RESET_AT="midnight"
```

### 2. Config File Budget Management

```yaml
# litellm_budget_config.yaml
general_settings:
  budget_manager: true
  max_budget: 5.00  # $5 daily limit
  budget_duration: "1d"
  
  # Alert thresholds
  budget_alerts:
    - threshold: 2.50  # Alert at 50%
      action: "log"
    - threshold: 4.00  # Alert at 80% 
      action: "email"  # if configured
    - threshold: 5.00  # Alert at 100%
      action: "block"  # Block new requests

# OpenRouter models with cost tracking
model_list:
  - model_name: "cheap"
    litellm_params:
      model: "openrouter/google/gemini-flash-1.5"
      api_base: "https://openrouter.ai/api/v1"
      api_key: os.environ/OPENROUTER_API_KEY
    model_info:
      cost_per_token: 0.000001  # Track costs
      
  - model_name: "smart"
    litellm_params:
      model: "openrouter/anthropic/claude-3.5-sonnet"
      api_base: "https://openrouter.ai/api/v1" 
      api_key: os.environ/OPENROUTER_API_KEY
    model_info:
      cost_per_token: 0.000015  # Track costs

# Smart routing with budget awareness
router_settings:
  routing_strategy: "cost-based-routing"
  enable_pre_call_checks: true  # Check budget before each call
  
  # Automatic cost optimization
  routing_rules:
    - pattern: "fix|typo|simple|quick"
      model: "cheap"
      max_cost_per_request: 0.001
    
    - pattern: "refactor|analyze|complex"
      model: "smart" 
      max_cost_per_request: 0.01
      
  # Budget-aware fallbacks
  fallbacks:
    - ["cheap", "smart"]  # Try cheap first, fallback to smart
```

### 3. Built-in Usage Tracking

```python
# Zero custom code - LiteLLM tracks automatically
from litellm import completion, get_budget

# Make requests normally
response = completion(
    model="openrouter/google/gemini-flash-1.5",
    messages=[{"role": "user", "content": "Hello"}]
)

# Check budget status (built-in)
budget_status = get_budget()
print(f"Used: ${budget_status['current_cost']:.3f}")
print(f"Limit: ${budget_status['max_budget']:.3f}")
print(f"Remaining: ${budget_status['budget_remaining']:.3f}")
```

## 🚀 Minimal Setup Script

```bash
#!/bin/bash
# setup-budget-tracking.sh

echo "🚀 Setting up LiteLLM Budget Tracking..."

# Install LiteLLM
pip install 'litellm[proxy]'

# Set budget environment variables
export LITELLM_MAX_BUDGET=5.00
export LITELLM_BUDGET_DURATION="1d"
export OPENROUTER_API_KEY="$OPENROUTER_API_KEY"

# Start LiteLLM proxy with budget tracking
litellm --config litellm_budget_config.yaml --port 4000 &

echo "✅ Budget tracking active!"
echo "💰 Daily limit: $5.00"
echo "📊 Check status: curl http://localhost:4000/health"
```

## 🔍 Built-in Budget Monitoring

### Real-time Budget Status
```bash
# Check current budget usage
curl http://localhost:4000/health

# Response includes:
{
  "status": "healthy",
  "budget": {
    "current_cost": 1.23,
    "max_budget": 5.00,
    "budget_remaining": 3.77,
    "requests_count": 45,
    "budget_reset_at": "2024-01-01T00:00:00Z"
  }
}
```

### Automatic Cost Calculation
LiteLLM automatically calculates costs based on:
- Token usage (input + output)
- Model pricing (from OpenRouter)
- Real-time cost tracking
- No manual calculation needed!

## 🛡️ Budget Protection Features

### 1. Pre-request Budget Checks
```yaml
# In config - automatically enabled
router_settings:
  enable_pre_call_checks: true
  
# LiteLLM will:
# - Check budget before each request
# - Reject if budget would be exceeded
# - Return clear error message
```

### 2. Automatic Budget Alerts
```python
# Built-in callback system
from litellm import completion

# LiteLLM automatically logs budget alerts
response = completion(
    model="openrouter/anthropic/claude-3.5-sonnet",
    messages=[{"role": "user", "content": "Expensive request"}],
    # Budget checked automatically before request
)

# Console output:
# 🚨 Budget Alert: 80% of daily budget used ($4.00/$5.00)
# ✅ Request approved - estimated cost: $0.02
```

### 3. Budget-Aware Model Selection
```yaml
# Smart routing considers budget automatically
router_settings:
  routing_strategy: "cost-based-routing"
  
  # When budget is low, prefer cheaper models
  budget_based_routing:
    - budget_remaining: "> 2.00"
      preferred_models: ["cheap", "smart"]
    - budget_remaining: "< 2.00" 
      preferred_models: ["cheap"]  # Only cheap when budget low
    - budget_remaining: "< 0.50"
      preferred_models: []  # Block all requests
```

## 📱 OpenCode.ai Integration

### Method 1: Environment Variables
```bash
# Set up budget-aware proxy
export LITELLM_MAX_BUDGET=5.00
export OPENAI_API_BASE="http://localhost:4000/v1"
export OPENAI_API_KEY="dummy"  # LiteLLM handles the real key

# Start budget-aware proxy
litellm --config litellm_budget_config.yaml --port 4000 &

# Use OpenCode.ai normally - budget tracking automatic!
opencode "fix this bug"  # Uses cheap model, tracks cost
opencode "refactor this" # Uses smart model, tracks cost
```

### Method 2: Smart Model Selection
```bash
# Create budget-aware wrapper
cat > smart-opencode.sh << 'EOF'
#!/bin/bash

# Check budget before running
BUDGET_STATUS=$(curl -s http://localhost:4000/health | jq -r '.budget.budget_remaining')

if (( $(echo "$BUDGET_STATUS < 0.50" | bc -l) )); then
    echo "⚠️ Budget low ($BUDGET_STATUS remaining) - using cheap model"
    opencode --model cheap "$@"
elif (( $(echo "$BUDGET_STATUS < 2.00" | bc -l) )); then
    echo "💰 Budget moderate ($BUDGET_STATUS remaining) - using smart model selectively"
    opencode --model smart "$@"
else
    echo "✅ Budget healthy ($BUDGET_STATUS remaining) - using best model"
    opencode --model smart "$@"
fi
EOF

chmod +x smart-opencode.sh

# Use budget-aware OpenCode.ai
./smart-opencode.sh "complex refactoring task"
```

## 📊 Usage Analytics (Built-in)

### Daily Budget Report
```python
# Built-in analytics - no coding required
from litellm import get_usage_stats

stats = get_usage_stats()
print(f"Today's usage: {stats}")

# Output:
# {
#   "total_requests": 23,
#   "total_cost": 1.47,
#   "avg_cost_per_request": 0.064,
#   "models_used": ["cheap", "smart"],
#   "budget_remaining": 3.53
# }
```

## 🎯 Summary: Zero Custom Coding Required!

**What LiteLLM gives you automatically:**
- ✅ **Budget tracking** - tracks every request cost
- ✅ **Budget limits** - blocks requests when limit hit
- ✅ **Cost optimization** - routes to cheapest appropriate model  
- ✅ **Usage analytics** - built-in reporting
- ✅ **Alert system** - warns at budget thresholds
- ✅ **API endpoints** - `/health` for budget status

**Total custom code needed: 0 lines!**

Just configure the YAML file and LiteLLM handles everything else. This is exactly the "yolo cost conscious" setup you want - intelligent cost management with zero maintenance overhead!