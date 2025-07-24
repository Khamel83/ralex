# Ralex V2 Setup Guide

**Get from zero to productive AI coding in 5 minutes.**

## 🚀 **Quick Setup (Recommended)**

### **1. Prerequisites**
- **Python 3.10+** and **Git** installed
- **OpenRouter API key** (free from [openrouter.ai](https://openrouter.ai/))

### **2. Get API Key**
```bash
# Sign up at https://openrouter.ai/ (free)
# Go to Keys tab → Create new key
# Set your API key:
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"

# Make it permanent:
echo 'export OPENROUTER_API_KEY="sk-or-v1-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### **3. Install Ralex**
```bash
# Clone repository
git clone https://github.com/Khamel83/ralex.git
cd ralex

# Install dependencies
python3 -m venv .ralex-env
source .ralex-env/bin/activate
pip install -r requirements.txt

# Make scripts executable
chmod +x ralex-agentos-v2.sh
```

### **4. Test Installation**
```bash
# Test with simple task
./ralex-agentos-v2.sh "fix this simple bug"

# Should show:
# 🧠 AgentOS Analysis:
#    Complexity: low
#    Strategy: Direct execution (cheap model)
```

## ✅ **You're Ready!**

Start coding with:
```bash
./ralex-agentos-v2.sh "your coding request"
```

---

## 🔧 **Advanced Setup Options**

### **Manual Environment Setup**
If you prefer manual control:

```bash
# Create virtual environment
python3 -m venv .ralex-env
source .ralex-env/bin/activate

# Install core dependencies
pip install litellm==1.74.8
pip install openai==1.97.1
pip install httpx==0.28.1
pip install pydantic==2.11.7

# Install development tools (optional)
pip install pytest>=7.0.0
pip install ruff>=0.1.0
pip install black>=22.0.0
```

### **Custom Configuration**

#### **Budget Limits**
Default daily budget is $5.00. To change:

```python
# Edit ralex_core/budget_optimizer.py
DEFAULT_DAILY_LIMIT = 10.00  # Change to your preferred amount
```

#### **Model Preferences**
```json
// Edit config/model_tiers.json to customize model selection
{
  "tiers": {
    "cheap": [
      {"name": "openrouter/google/gemini-flash-1.5", "cost_per_token": 0.000001}
    ],
    "premium": [
      {"name": "openrouter/anthropic/claude-3-sonnet", "cost_per_token": 0.000015}
    ]
  }
}
```

#### **AgentOS Standards**
Customize coding standards by editing:
- `agent_os/standards/python.md` - Python coding rules
- `agent_os/standards/git-workflow.md` - Git workflow preferences
- `agent_os/instructions/testing.md` - Testing requirements

### **Docker Setup** (Optional)
```bash
# Build Docker image
docker build -t ralex-v2 .

# Run with API key
docker run -e OPENROUTER_API_KEY="your-key" -it ralex-v2
```

### **Development Setup**
For contributing to Ralex:

```bash
# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
python test_agentos_integration.py
python health_check.py

# Run linting
ruff check .
black .
```

---

## 🚨 **Troubleshooting**

### **"Command not found" Error**
```bash
# Make scripts executable
chmod +x *.sh

# Check Python path
which python3  # Should show Python 3.10+
```

### **"API key not set" Error**
```bash
# Check if key is set
echo $OPENROUTER_API_KEY  # Should show your key

# Set temporarily
export OPENROUTER_API_KEY="your-key-here"

# Set permanently
echo 'export OPENROUTER_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### **"Network Connection" Error**
```bash
# Test OpenRouter connectivity
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"

# Should return JSON list of models
```

### **"Dependencies Missing" Error**
```bash
# Reinstall virtual environment
rm -rf .ralex-env
python3 -m venv .ralex-env
source .ralex-env/bin/activate
pip install -r requirements.txt
```

### **"Budget Exceeded" Error**
Budget resets daily at midnight UTC. Or check:
```bash
# Check current budget status
python3 health_check.py

# Budget file location
cat /tmp/ralex_litellm_budget.json
```

---

## ⚡ **Performance Tips**

### **Faster Setup**
```bash
# Use UV for faster installs (optional)
pip install uv
uv pip install -r requirements.txt
```

### **Shell Aliases**
Add to your `~/.bashrc`:
```bash
alias ralex="cd /path/to/ralex && ./ralex-agentos-v2.sh"
alias ralex-check="cd /path/to/ralex && python3 health_check.py"
```

### **IDE Integration**
For VS Code, add this to your terminal profile:
```json
{
  "terminal.integrated.profiles.linux": {
    "Ralex": {
      "path": "/bin/bash",
      "args": ["-c", "cd /path/to/ralex && source .ralex-env/bin/activate && bash"]
    }
  }
}
```

---

## 🎯 **Next Steps**

1. **Read**: [USAGE.md](USAGE.md) for daily workflow examples
2. **Learn**: [ARCHITECTURE.md](ARCHITECTURE.md) for technical details  
3. **Customize**: Edit `agent_os/` files for your coding standards
4. **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md) for development

**Happy coding with cost-optimized AI! 🚀**