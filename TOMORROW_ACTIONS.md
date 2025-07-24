# Tomorrow's Action Plan
*Setup for immediate use*

## 🎯 Priority 1: Basic Setup (15 minutes)

### Step 1: Get OpenRouter API Key (5 minutes)
1. Go to https://openrouter.ai/
2. Sign up with email (free)
3. Navigate to "Keys" tab
4. Click "Create new key" 
5. Copy the API key

### Step 2: Set Environment Variable (2 minutes)
```bash
export OPENROUTER_API_KEY="your-key-here"
echo "export OPENROUTER_API_KEY='your-key-here'" >> ~/.bashrc
source ~/.bashrc
```

### Step 3: Install and Test (8 minutes)
```bash
cd ralex
./setup-budget-tracking.sh  # Automated installation
```

If network issues persist, try:
```bash
# Manual installation fallback
python3 -m venv .ralex-env
.ralex-env/bin/pip install litellm
```

### Step 4: Quick Test
```bash
# Terminal 1: Start proxy
./start-budget-aware-proxy.sh

# Terminal 2: Test command
./yolo-budget-code.sh "hello world test"
```

---

## 🚀 Priority 2: Daily Workflow (30 minutes)

### Morning Routine
```bash
# Start budget-aware proxy (leave running)
./start-budget-aware-proxy.sh
```

### Coding Session
```bash
# Use throughout the day
./yolo-budget-code.sh "fix this bug"
./yolo-budget-code.sh "refactor this function"  
./yolo-budget-code.sh "add error handling"
./yolo-budget-code.sh "yolo quick syntax fix"
```

### Budget Monitoring
```bash
# Check budget anytime
./check-budget.sh

# Expected output:
# {
#   "current_cost": 1.23,
#   "max_budget": 5.00, 
#   "budget_remaining": 3.77
# }
```

---

## 🔧 Priority 3: Optimization (Optional)

### Increase Budget for Power Users
```bash
# Edit litellm_budget_config.yaml
# Change: max_budget: 5.00
# To:     max_budget: 10.00
```

### AgentOS Integration
Structure prompts to trigger smart routing:
- **Simple tasks**: "fix", "typo", "format", "add comments"
- **Complex tasks**: "refactor", "analyze", "architecture", "design"
- **Emergency**: "yolo", "urgent", "fast", "now"

### GitHub PAT Fix (Optional)
Add `workflow` scope to GitHub Personal Access Token to enable workflow file updates.

---

## 📊 Expected Results

### Cost Efficiency
- Simple tasks: ~$0.0001 each (Gemini Flash)
- Complex tasks: ~$0.01 each (Claude Sonnet) 
- Daily usage: $0.50-3.00 depending on intensity

### Performance
- Simple responses: ~2-3 seconds
- Complex analysis: ~10-15 seconds
- Budget check: Instant
- Pattern recognition: Automatic

---

## 🎉 Success Criteria

✅ **API key working**: OpenRouter connection successful  
✅ **Proxy running**: LiteLLM budget tracking active  
✅ **Smart routing**: Cheap models for simple tasks  
✅ **Budget tracking**: Real-time cost monitoring  
✅ **Yolo mode**: Fast execution for urgent tasks  

**Goal**: Full day of productive AI-assisted coding within $5 budget!

---

## 🆘 Troubleshooting

### "API key not set"
```bash
echo $OPENROUTER_API_KEY  # Should show your key
```

### "Proxy not running"  
```bash
# Check if process is running
ps aux | grep litellm
# Restart if needed
./start-budget-aware-proxy.sh
```

### "Budget exceeded"
Either wait until tomorrow (resets daily) or increase limit in `litellm_budget_config.yaml`

### "Network/installation issues"
Wait for stable connection, then retry `./setup-budget-tracking.sh`

---

**Bottom line**: Everything is ready. Just set API key → run setup → start coding with AI!