# Ralex V3 Usage Guide

**🎙️ Master voice-driven AI coding with examples, tips, and best practices.**

## 🚀 **Quick Start: Your First Voice Coding Session**

### **1. Launch Ralex V3**
```bash
./ralex-v3-launch.sh
# Wait for: ✅ Backend API started, ✅ Frontend started
```

### **2. Open Web Interface**
- Visit **http://localhost:3000** in your browser
- Allow microphone access when prompted
- You'll see the Ralex V3 interface with budget tracking

### **3. Try Your First Voice Command**
1. Click the **🎙️ Voice** button
2. Say: **"Create a Python function to calculate fibonacci numbers"**
3. Watch your voice become working code instantly!

---

## 🎙️ **Voice Command Patterns**

### **Auto-Submit Commands**
These phrases automatically submit after voice recognition:

```
🎙️ "Fix this authentication bug, execute"
🎙️ "Refactor the user model, send it"  
🎙️ "Add error handling, go ahead"
🎙️ "Create unit tests, run it"
🎙️ "Optimize database queries, do it"
```

### **Manual Submit Commands**
These require clicking Send after voice input:

```
🎙️ "How does JWT authentication work?"
🎙️ "Review this code for security issues"
🎙️ "Explain the MVC pattern"
🎙️ "What are the best practices for error handling?"
```

### **File-Specific Commands**
Reference files naturally in your voice commands:

```
🎙️ "Fix the bug in user_auth.py, execute"
🎙️ "Add tests to the payment module, send it"
🎙️ "Refactor models.py for better performance, go ahead"
🎙️ "Update the API endpoints in routes.py, do it"
```

---

## 💰 **Budget Management**

### **Real-Time Tracking**
- **Green bar**: Plenty of budget remaining (>50%)
- **Yellow bar**: Moderate usage (20-50%)
- **Red bar**: Low budget (<20%)
- **Live updates**: See costs in real-time via WebSocket

### **Adding Budget**
Click the budget widget buttons:
- **$0.25**: Perfect for quick tests and experiments
- **$1.00**: Good for short coding sessions
- **$5.00**: Full day of development work

### **Budget Tips**
```bash
# Check current budget status
curl http://localhost:8000/api/sessions/stats

# Monitor spending in real-time
# Watch the budget widget for live updates

# Cost examples:
# Simple fixes: ~$0.001 each
# Complex features: ~$0.015 each  
# Full implementations: ~$0.025 each
```

---

## 📱 **Mobile Coding Workflow**

### **Voice Coding on Your Phone**
1. **Open browser** to http://localhost:3000 (or your Tailscale URL)
2. **Tap the 🎙️ button** - it's optimized for touch
3. **Speak your request** clearly
4. **Tap Send** or use auto-submit phrases

### **Mobile-Optimized Commands**
```
🎙️ "Quick fix for login error, execute"
🎙️ "Add validation to form, send it"
🎙️ "Check database connection, go ahead"
🎙️ "Create simple API endpoint, do it"
```

### **Mobile Pro Tips**
- **Use landscape mode** for better code viewing
- **Speak clearly** - mobile mics vary in quality
- **Use shorter commands** for better recognition
- **Auto-submit phrases** work great on mobile

---

## 🧠 **Advanced Voice Patterns**

### **Multi-Step Workflows**
```
🎙️ "Create user authentication system with JWT tokens, database models, and comprehensive tests, execute"

# Ralex V3 will:
# 1. Analyze complexity (high)
# 2. Use smart model for planning
# 3. Break down into specific tasks
# 4. Execute each part efficiently
```

### **Context-Aware Commands**
```
🎙️ "Based on the payment.py file, add refund functionality, go ahead"
🎙️ "Following our project patterns, create order management, send it"
🎙️ "Using the existing auth system, add role-based permissions, execute"
```

### **Performance-Focused Commands**
```
🎙️ "Optimize this database query for better performance, execute"
🎙️ "Refactor this code to reduce memory usage, send it"
🎙️ "Add caching to the API endpoints, go ahead"
🎙️ "Profile and improve the slow functions, do it"
```

---

## 🔄 **Real-Time Collaboration**

### **WebSocket Features**
- **Live budget updates** across all connected devices
- **Typing indicators** when AI is processing
- **Model selection** notifications in real-time
- **System notifications** for important events

### **Multi-Device Workflow**
```bash
# Desktop for heavy development
🎙️ "Implement complete user management system, execute"

# Phone for quick fixes  
🎙️ "Fix the typo in login form, send it"

# Tablet for code review
🎙️ "Review security in authentication module"

# All devices see budget updates instantly via WebSocket
```

---

## 🎯 **Coding Workflow Examples**

### **Bug Fixing Session**
```
# Start with voice input
🎙️ "Analyze the login error in auth.py, execute"

# Follow up based on analysis
🎙️ "Fix the JWT token validation issue, send it"

# Add prevention
🎙️ "Add comprehensive error handling, go ahead"

# Verify solution
🎙️ "Create tests for the auth fix, do it"
```

### **Feature Development**
```
# High-level planning
🎙️ "Design user profile management system with CRUD operations, execute"

# Implementation
🎙️ "Create the database models for user profiles, send it"
🎙️ "Add API endpoints for profile operations, go ahead"  
🎙️ "Create frontend forms for profile editing, do it"

# Quality assurance
🎙️ "Add validation and security checks, execute"
🎙️ "Create comprehensive tests with 90% coverage, send it"
```

### **Code Review Session**
```
# Analysis commands (no auto-submit)
🎙️ "Review the security of this authentication system"
🎙️ "Analyze performance bottlenecks in the database layer"
🎙️ "Check code quality and suggest improvements"

# Implementation of suggestions
🎙️ "Implement the suggested security improvements, execute"
🎙️ "Optimize the slow database queries, send it"
```

---

## 🌟 **Pro Tips & Best Practices**

### **Voice Recognition Optimization**
- **Speak clearly** and at moderate pace
- **Use technical terms** - Ralex understands programming vocabulary
- **Include context** - mention file names and function names
- **End with action words** for auto-submit ("execute", "send it", "go ahead")

### **Budget Optimization**
- **Start small** - use $0.25 for testing voice commands
- **Monitor spending** - watch the real-time budget widget
- **Use simple commands** for quick fixes to save costs
- **Complex requests** are worth the smart model cost for quality

### **Mobile Best Practices**
- **Test voice recognition** in your environment first
- **Use shorter commands** on mobile for better accuracy
- **Portrait mode** for chat, **landscape** for code viewing
- **Touch the voice button** firmly - mobile browsers vary

### **Session Management**
- **Related files** are automatically tracked in context
- **File references** in voice commands add files to session
- **Session state** persists across browser refreshes
- **Multiple devices** can share the same session via URL

---

## 🔧 **Keyboard Shortcuts & UI Tips**

### **Web Interface Shortcuts**
- **Ctrl+Enter**: Send message (when text input focused)
- **Space**: Start/stop voice input (when voice button focused)
- **Tab**: Navigate between UI elements
- **Escape**: Cancel voice input

### **UI Features**  
- **Dark theme**: Optimized for coding environments
- **Responsive design**: Works on any screen size
- **Visual feedback**: Recording animations and status indicators
- **Real-time updates**: Budget, typing indicators, model selection

---

## 🚨 **Troubleshooting Voice Commands**

### **"Voice Recognition Not Working"**
```bash
# Check microphone permissions in browser
# Chrome: chrome://settings/content/microphone
# Allow access for localhost:3000

# Test Web Speech API in console:
# new webkitSpeechRecognition()
```

### **"Commands Not Auto-Submitting"** 
Make sure you end with trigger phrases:
- ✅ "execute", "send it", "go ahead", "do it", "run it"
- ❌ Missing trigger phrases require manual Send

### **"Poor Recognition Accuracy"**
- **Speak clearly** and avoid background noise
- **Use Chrome/Safari** - best Web Speech API support  
- **Check microphone** quality and positioning
- **Avoid Firefox** - limited speech recognition support

### **"Budget Not Updating"**
```bash
# Check WebSocket connection in browser console
# Should see: "WebSocket connected" messages

# Verify backend is running
curl http://localhost:8000/health
```

---

## 📊 **Usage Analytics**

### **Understanding Your Costs**
- **Voice session**: $0.25-0.75/hour typically
- **Simple fixes**: ~$0.001 each (very cheap)
- **Complex features**: ~$0.015 each (smart model planning)
- **Full implementations**: ~$0.025 each (comprehensive)

### **Optimizing Your Workflow**
- **Batch related requests** in single voice commands
- **Use context effectively** - mention related files
- **Start with analysis** for complex tasks
- **Follow up with implementation** commands

### **Session Stats**
```bash
# Check your usage patterns
curl http://localhost:8000/api/sessions/stats

# Monitor real-time spending
# Watch budget widget during development

# Export session data for analysis
curl http://localhost:8000/api/sessions/{session_id}/info
```

---

## 🎉 **Ready to Voice Code Like a Pro!**

**Ralex V3** transforms how you interact with AI for coding:
- **Natural voice commands** replace typing
- **Real-time budget tracking** keeps costs transparent  
- **Mobile coding** makes development possible anywhere
- **Professional quality** through AgentOS standards

**Start your voice coding journey today! 🚀🎙️**

---

## 📚 **Additional Resources**

- **[README.md](README.md)**: Project overview and features
- **[SETUP.md](SETUP.md)**: Installation and configuration
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Technical implementation
- **[RALEX_V3_DETAILED_PLAN.md](RALEX_V3_DETAILED_PLAN.md)**: Complete development roadmap