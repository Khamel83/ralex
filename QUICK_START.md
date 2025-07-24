# Ralex V2: Quick Start Guide

## What is Ralex V2?

**Ralex V2** is a terminal AI coding assistant that automatically chooses the cheapest AI model for your task while staying within your daily budget. It's like having Claude Code, but cost-conscious and with "yolo mode" for fast execution.

- 🚀 **Yolo Mode**: Fast AI coding with minimal prompts
- 💰 **Cost Conscious**: Automatically uses cheap models when possible, smart models when needed
- 📊 **Budget Tracking**: $5 daily limit with automatic cost tracking
- 🧠 **Smart Routing**: "fix typo" → cheap model, "refactor code" → smart model

## Prerequisites (2 minutes)

### 1. Get OpenRouter API Key
1. Go to [https://openrouter.ai/](https://openrouter.ai/)
2. Sign up (free - just need email)
3. Go to Keys tab → Create new key
4. Copy your API key
5. Set it in your terminal:
```bash
export OPENROUTER_API_KEY="your-key-here"
echo "export OPENROUTER_API_KEY='your-key-here'" >> ~/.bashrc
```

### 2. Have Python 3.10+ and Git
```bash
python3 --version  # Should be 3.10 or higher
git --version      # Should work
```

## Installation (3 minutes)

### Step 1: Clone and Setup
```bash
# Clone the repository
git clone https://github.com/Khamel83/ralex.git
cd ralex

# Run one-command setup
./setup-budget-tracking.sh
```

That's it! The setup script installs everything automatically.

## Usage (Daily Workflow)

### Step 1: Start the Smart Router (Once per day)
```bash
# In Terminal 1 - start the budget-aware AI router
./start-budget-aware-proxy.sh
```

Leave this running. It shows your budget status and handles all the AI routing.

### Step 2: Code with Budget Awareness (Terminal 2)
```bash
# Use budget-aware AI coding
./yolo-budget-code.sh "fix this bug in my code"
./yolo-budget-code.sh "refactor this function" 
./yolo-budget-code.sh "yolo add error handling quickly"
```

## How It Works

### Automatic Model Selection
- **Simple tasks** → Gemini Flash (ultra-cheap, fast)
- **Complex tasks** → Claude Sonnet (smart, more expensive)
- **Yolo mode** → Always fastest/cheapest

### Budget Intelligence
- **High budget** (>$2): Uses best model for the task
- **Medium budget** ($0.50-$2): Prefers cheap models
- **Low budget** (<$0.50): Cheap models only
- **Budget exceeded**: Stops spending until tomorrow

### Real Examples
```bash
# These use cheap models automatically:
./yolo-budget-code.sh "fix this typo"
./yolo-budget-code.sh "add comments to this function"
./yolo-budget-code.sh "format this code"

# These use smart models when budget allows:
./yolo-budget-code.sh "refactor this entire class"
./yolo-budget-code.sh "analyze this algorithm's complexity"
./yolo-budget-code.sh "design a better architecture"

# Yolo mode (always fast/cheap):
./yolo-budget-code.sh "yolo fix this now"
```

## Check Your Budget

```bash
# See budget status anytime
./check-budget.sh
```

Output:
```json
{
  "current_cost": 1.23,
  "max_budget": 5.00,
  "budget_remaining": 3.77,
  "requests_count": 15
}
```

## Troubleshooting

### "Command not found"
```bash
chmod +x *.sh  # Make scripts executable
```

### "API key not set"
```bash
echo $OPENROUTER_API_KEY  # Should show your key
export OPENROUTER_API_KEY="your-key-here"
```

### "Proxy not running"
Start the proxy first:
```bash
./start-budget-aware-proxy.sh
```

### "Budget exceeded"
Wait until tomorrow (budget resets daily) or increase your limit in `litellm_budget_config.yaml`:
```yaml
max_budget: 10.00  # Change from 5.00 to 10.00
```

## Daily Workflow Summary

```bash
# Morning: Start budget router (Terminal 1)
./start-budget-aware-proxy.sh

# All day: Code with AI (Terminal 2) 
./yolo-budget-code.sh "your coding request"

# Anytime: Check budget
./check-budget.sh
```

## What You Get

- ✅ **$5 daily budget** with automatic tracking
- ✅ **Smart cost optimization** (cheap models for simple tasks)
- ✅ **Yolo mode** for fast execution
- ✅ **No manual model selection** (AI picks the best one)
- ✅ **Budget alerts** when approaching limits
- ✅ **Zero maintenance** (all logic built into LiteLLM)

## Advanced Usage

### Change Budget Limit
Edit `litellm_budget_config.yaml`:
```yaml
max_budget: 10.00  # Daily budget in USD
```

### Add More Models
Add to `litellm_budget_config.yaml`:
```yaml
- model_name: "premium"
  litellm_params:
    model: "openrouter/openai/gpt-4"
    api_key: "os.environ/OPENROUTER_API_KEY"
```

### Direct OpenCode.ai Usage
If you prefer the original OpenCode.ai interface:
```bash
export OPENAI_API_BASE="http://localhost:4000/v1"
export OPENAI_API_KEY="dummy"
opencode "your request"  # Uses smart routing automatically
```

---

**That's it!** You now have a cost-conscious AI coding assistant that automatically optimizes your spending while providing yolo-mode fast execution.

**Questions?** Check the budget with `./check-budget.sh` or restart the proxy with `./start-budget-aware-proxy.sh`.