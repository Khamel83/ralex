# Ralex V3 Setup Guide

**🎙️ Get from zero to voice-driven AI coding in 5 minutes.**

## 🚀 **Quick Setup (Recommended)**

### **1. Prerequisites**
- **Python 3.10+** and **Node.js 18+** installed
- **OpenRouter API key** (free from [openrouter.ai](https://openrouter.ai/))
- **Modern web browser** with microphone access

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

### **3. Install Ralex V3**
```bash
# Clone repository
git clone https://github.com/Khamel83/ralex.git
cd ralex

# Install Python dependencies
python3 -m pip install -r requirements.txt

# Install frontend dependencies
npm install --prefix ralex-frontend

# Make launch script executable
chmod +x ralex-v3-launch.sh
```

### **4. Launch & Test**
```bash
# Start both backend and web interface
./ralex-v3-launch.sh

# Should show:
# 🚀 Starting Ralex V3 - AI Coding Assistant
# ✅ Backend API started (PID: xxxx)
# ✅ Frontend started (PID: xxxx)
# 📱 Web Interface: http://localhost:3000
```

### **5. Test Voice Input**
1. Open **http://localhost:3000** in your browser
2. Click **🎙️ Voice** button and allow microphone access
3. Say: **"Create a Python function to calculate fibonacci numbers"**
4. Watch as your voice becomes working code!

## ✅ **You're Ready for Voice Coding!**

Your Ralex V3 setup includes:
- 🎙️ **Voice input** from any modern browser
- 💰 **Real-time budget tracking** with $5.00 daily limit
- 📱 **Mobile-responsive** interface for coding anywhere
- 🧠 **AgentOS standards** automatically applied
- 🔄 **WebSocket updates** for real-time collaboration

---

## 🌐 **Web Interface Features**

### **Voice Commands**
```
🎙️ "Fix this bug, execute"          → Auto-submits after recognition
🎙️ "Refactor this code, send it"    → Smart auto-submit phrases  
🎙️ "Add tests, go ahead"            → Natural language workflow
🎙️ "Create user authentication"     → Complex feature development
```

### **Budget Management**
- **Real-time tracking** with visual progress bars
- **Add budget** buttons ($0.25, $1.00, $5.00)
- **Transaction history** showing model usage and costs
- **Low budget warnings** when approaching limits

### **Mobile Coding**
- **Touch-optimized** voice button for phones/tablets
- **Responsive design** adapts to any screen size
- **Landscape/portrait** mode support
- **iOS/Android** compatible via browser

---

## 🔧 **Advanced Setup Options**

### **Custom Configuration**

#### **Budget Limits**
```bash
# Edit default budget in web session manager
vim ralex_core/web_session.py

# Change initial_budget default value:
def create_session(self, initial_budget: float = 10.0):  # Changed from 5.0
```

#### **Model Preferences**
```json
// Edit config/model_tiers.json
{
  "tiers": {
    "fast": [
      {"name": "openrouter/google/gemini-flash-1.5", "cost_per_token": 0.000001}
    ],
    "smart": [
      {"name": "openrouter/anthropic/claude-3-sonnet", "cost_per_token": 0.000015}
    ]
  }
}
```

#### **AgentOS Standards**
Customize coding standards for your project:
```bash
# Python coding standards
vim agent_os/standards/python.md

# Git workflow preferences  
vim agent_os/standards/git-workflow.md

# Testing requirements
vim agent_os/instructions/testing.md
```

### **Production Deployment**

#### **Docker Setup**
```bash
# Build multi-service stack
docker-compose up -d

# Access via:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

#### **Tailscale HTTPS**
```bash
# Enable Tailscale certificates
sudo tailscale cert $(tailscale status --json | jq -r '.Self.DNSName')

# Configure nginx reverse proxy
sudo cp nginx/ralex.conf /etc/nginx/sites-enabled/
sudo systemctl reload nginx

# Access securely via: https://your-device.tailnet.ts.net
```

### **Development Setup**
```bash
# Install development tools
pip install pytest ruff black isort

# Run tests
python test-ralex-v3.py

# Run frontend in dev mode
cd ralex-frontend && npm run dev

# Backend with auto-reload
python -m ralex_core.openai_api --reload
```

---

## 🚨 **Troubleshooting**

### **"Microphone Access Denied"**
```bash
# Chrome: chrome://settings/content/microphone
# Firefox: about:preferences#privacy → Permissions → Microphone
# Safari: Safari → Preferences → Websites → Microphone

# Allow access for localhost:3000
```

### **"Backend Connection Failed"** 
```bash
# Check if backend is running
curl http://localhost:8000/health

# Should return: {"status": "healthy", "version": "3.0.0"}

# Check logs
tail -f logs/backend.log
```

### **"Voice Recognition Not Working"**
```bash
# Supported browsers:
# ✅ Chrome/Chromium (best support)
# ✅ Safari (iOS/macOS)
# ✅ Edge
# ❌ Firefox (limited support)

# Test Web Speech API:
# Open browser console → new webkitSpeechRecognition()
```

### **"Frontend Won't Start"**
```bash
# Check Node.js version
node --version  # Should be 18.x or higher

# Reinstall dependencies
cd ralex-frontend
rm -rf node_modules package-lock.json
npm install

# Check for port conflicts
lsof -i :3000  # Kill any conflicting processes
```

### **"API Key Issues"**
```bash
# Verify key is set
echo $OPENROUTER_API_KEY  # Should show your key

# Test API connectivity
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"

# Should return model list JSON
```

### **"Budget Tracking Not Working"**
```bash
# Check WebSocket connection in browser console
# Should see: "WebSocket connected" messages

# Verify WebSocket endpoint
curl -i -N -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  http://localhost:8000/ws/test-session
```

---

## ⚡ **Performance Optimization**

### **Faster Development**
```bash
# Use concurrent backend/frontend development
npm run dev --prefix ralex-frontend & python -m ralex_core.openai_api

# Enable hot reload for both services
export RALEX_DEV_MODE=true
```

### **Shell Aliases**
Add to your `~/.bashrc`:
```bash
alias ralex3="cd /path/to/ralex && ./ralex-v3-launch.sh"
alias ralex-logs="cd /path/to/ralex && tail -f logs/*.log"
alias ralex-health="curl -s http://localhost:8000/health | jq"
```

### **Browser Bookmarks**
- **Ralex Web**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs  
- **Health Check**: http://localhost:8000/health
- **Budget Status**: http://localhost:8000/api/sessions/stats

---

## 🎯 **Next Steps**

1. **Try Voice Coding**: Use microphone for hands-free development
2. **Explore Budget Tracking**: Monitor real-time costs and usage
3. **Mobile Testing**: Code from your phone using the responsive interface
4. **Customize Standards**: Edit `agent_os/` files for your coding style
5. **Deploy Production**: Use Tailscale for secure remote access

### **Pro Tips**
- **Voice Commands**: End with "execute", "send it", or "go ahead" for auto-submit
- **Budget Management**: Add small amounts ($0.25) for testing, larger ($5) for sessions
- **Mobile Workflow**: Voice input works excellently on phones for quick fixes
- **Team Collaboration**: Share your Tailscale URL for real-time coding sessions

**Happy voice coding with Ralex V3! 🚀🎙️**