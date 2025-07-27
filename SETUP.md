# Ralex V4 Setup Guide

**🚀 Get from zero to AI coding orchestration in 5 minutes.**

## 🚀 **Quick Setup (Recommended)**

### **1. Prerequisites**
- **Python 3.10+** installed
- **OpenRouter API key** (free from [openrouter.ai](https://openrouter.ai/))
- **8GB+ RAM** (4GB minimum for Raspberry Pi)

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

### **3. Install Ralex V4**
```bash
# Clone repository
git clone https://github.com/Khamel83/ralex.git
cd ralex

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **4. Launch Ralex V4**
```bash
# Start the full stack (API + WebUI)
python start_ralex_v4.py

# Should show:
# 🎯 Starting Ralex V4 - Full Stack Integration
# ✅ RalexBridge API started successfully
# ✅ OpenWebUI configured to use RalexBridge
# ✅ OpenWebUI started on port 3000
```

### **5. Access Your AI Coding Assistant**
1. **Local Access**: http://localhost:3000
2. **Network Access**: http://YOUR-IP:3000
3. **Tailscale Access**: http://TAILSCALE-IP:3000

## ✅ **What You Get with Ralex V4**

- 🌐 **OpenWebUI Interface** - Modern chat-based coding interface
- 🔄 **RalexBridge API** - Intelligent model routing via OpenRouter
- 🏗️ **AgentOS Integration** - Automated coding standards and workflows
- 💰 **Cost Optimization** - Smart model selection for budget efficiency
- 🔧 **Multi-Provider Support** - OpenRouter, LiteLLM, and more

---

## 🍓 **Raspberry Pi Setup**

Ralex V4 is optimized for ARM devices like Raspberry Pi with special lightweight configurations:

### **Raspberry Pi Quick Setup**
```bash
# Same basic setup as above, but V4 automatically detects ARM architecture
# and uses ultra-minimal requirements for compatibility

# Clone and setup
git clone https://github.com/Khamel83/ralex.git
cd ralex
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start (ARM-optimized automatically)
export OPENROUTER_API_KEY="your-key-here"
python start_ralex_v4.py
```

### **ARM Compatibility Features**
- ✅ **Auto-detects ARM architecture** and skips heavy PyTorch dependencies
- ✅ **Ultra-minimal OpenWebUI** requirements for faster startup
- ✅ **Memory-efficient** configurations for 4GB+ Raspberry Pi models
- ✅ **No illegal instruction errors** - ARM-compatible package selection

---

## 🔧 **Services & Ports**

After startup, you'll have these services running:

| Service | Port | Purpose | URL |
|---------|------|---------|-----|
| **RalexBridge API** | 8000 | AI orchestration backend | http://localhost:8000 |
| **OpenWebUI** | 3000 | Web-based chat interface | http://localhost:3000 |

### **Health Checks**
```bash
# Check RalexBridge API
curl http://localhost:8000/health
# Returns: {"status":"healthy","components":["AgentOS","LiteLLM","OpenRouter","OpenCode"]}

# Check if OpenWebUI is running
curl -I http://localhost:3000
# Returns: HTTP/1.1 404 Not Found (this is normal for root path)
```

---

## 🚨 **Troubleshooting**

### **"OpenWebUI Won't Start"**
```bash
# Check if ultra-minimal requirements exist
ls requirements-webui-ultraminimal.txt

# If missing, the startup script will fall back to minimal or full requirements
# On ARM devices, ensure PyTorch-based packages are avoided
```

### **"Illegal Instruction Error"**
```bash
# This happens on ARM devices with incompatible PyTorch
# V4 automatically prevents this by using ultra-minimal requirements

# If you encounter this, manually remove problematic packages:
pip uninstall -y sentence-transformers torch transformers

# Then restart
python start_ralex_v4.py
```

### **"Dependency Installation Takes Forever"**
```bash
# Normal on Raspberry Pi - V4 has 5-minute timeout protection
# Heavy packages (PyTorch, transformers) are skipped on ARM

# Check what's installing:
ps aux | grep pip
```

### **"Backend Connection Failed"**
```bash
# Check if RalexBridge API is running
ps aux | grep ralex_api.py

# Check the health endpoint
curl http://localhost:8000/health

# Restart if needed
pkill -f ralex_api.py
export OPENROUTER_API_KEY="your-key-here"
python ralex_api.py &
```

### **"OpenRouter API Key Issues"**
```bash
# Verify key is set
echo $OPENROUTER_API_KEY

# Test OpenRouter connectivity
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

---

## 🌐 **Remote Access Setup**

### **Network Access**
```bash
# Get your local IP
hostname -I

# Access from other devices on your network:
# http://YOUR-LOCAL-IP:3000
```

### **Tailscale Setup (Recommended)**
```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Authenticate
sudo tailscale up

# Get your Tailscale IP
tailscale ip -4

# Access securely from anywhere:
# http://YOUR-TAILSCALE-IP:3000
```

---

## ⚡ **Performance Tips**

### **Raspberry Pi Optimization**
- Use **Class 10 or better SD card** for better I/O performance
- Ensure **adequate cooling** during AI processing
- **4GB+ RAM** recommended for smooth operation
- Consider **USB 3.0 SSD** for storage if doing heavy development

### **Memory Management**
```bash
# Monitor memory usage
free -h

# If running low, restart services
pkill -f uvicorn
pkill -f ralex_api.py
python start_ralex_v4.py
```

---

## 🎯 **Next Steps**

1. **Open the WebUI**: http://localhost:3000
2. **Start a conversation**: Ask it to create a simple Python function
3. **Test model routing**: Try different types of requests (simple vs complex)
4. **Explore the API**: Check http://localhost:8000/docs for API documentation
5. **Set up remote access**: Use Tailscale for secure access from anywhere

### **Example First Conversation**
```
You: "Create a Python function to calculate the Fibonacci sequence"
Ralex: [Provides optimized code with proper error handling]

You: "Now add unit tests for that function"
Ralex: [Creates comprehensive pytest tests]

You: "Run the tests and fix any issues"
Ralex: [Executes tests and fixes any problems]
```

**Happy coding with Ralex V4! 🚀🤖**