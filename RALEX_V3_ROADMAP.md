# Ralex V3: "Vibe Code" Voice-Driven AI Assistant
## Complete Roadmap for Web Frontend + Mobile Voice Integration

---

## 🎯 **V3 Vision: Your Ideal Setup**

**Goal**: Transform Ralex into a voice-first, web-accessible "vibe coding" platform that works seamlessly from phone/desktop with budget-aware AI conversations.

**Key Features**:
- 🎤 **Voice-to-text input** (mobile-friendly)
- 💬 **Conversational UI** with budget tracking
- 🌐 **Web interface** accessible from anywhere
- 💰 **Real-time budget management** ("here's $1, see how far you get")
- 🔄 **Voice feedback loop** (speak → AI responds → speak back)
- 📱 **Mobile-optimized** for "vibe coding" on the go

---

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Web Frontend  │    │   Ralex Backend  │    │   OpenRouter API    │
│                 │    │                  │    │                     │
│ • Voice Input   │◄──►│ • Current V2     │◄──►│ • Model Selection   │
│ • Chat UI       │    │ • Budget Manager │    │ • Cost Tracking     │
│ • Budget Display│    │ • Session State  │    │ • Response Gen      │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
         ▲
         │ HTTPS/WSS
         ▼
┌─────────────────┐
│  Nginx Reverse  │
│     Proxy       │
│ (yourdomain.com)│
└─────────────────┘
```

---

## 📋 **Phase 1: Backend API Foundation (2-3 days)**

### 1.1 **REST API Endpoints**
```python
# ralex_core/web_api.py
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Handle chat messages with budget tracking"""
    
@app.route('/api/budget', methods=['GET'])
def budget_status():
    """Get current budget status"""
    
@app.route('/api/session', methods=['POST'])
def create_session():
    """Create new conversation session"""

@socketio.on('chat_message')
def handle_chat(data):
    """Real-time chat via WebSocket"""
```

### 1.2 **Session Management**
```python
# ralex_core/session_manager.py
class SessionManager:
    def create_session(self, budget_limit: float) -> str:
        """Create session with budget limit"""
        
    def get_session_state(self, session_id: str) -> dict:
        """Get conversation history + budget status"""
        
    def update_budget(self, session_id: str, cost: float):
        """Update session budget tracking"""
```

### 1.3 **Budget Integration**
- Extend current `BudgetManager` with session-based tracking
- Add "budget challenges" ("here's $0.25, see what you can do")
- Real-time budget updates via WebSocket

---

## 📋 **Phase 2: Web Frontend (1-2 days)**

### 2.1 **Frontend Stack Choice**
**Recommendation**: Fork **Open WebUI** (clean, proven chat interface)

**Alternative**: Simple vanilla JS + WebSocket for minimal complexity

### 2.2 **Core Components**
```html
<!-- templates/chat.html -->
<div id="chat-container">
    <div id="messages"></div>
    <div id="budget-display">
        Budget: $<span id="budget-remaining">1.00</span>
    </div>
    <div id="voice-input">
        <button id="voice-btn">🎤 Voice Input</button>
        <textarea id="text-input" placeholder="Or type here..."></textarea>
    </div>
</div>
```

### 2.3 **Voice Integration**
```javascript
// static/js/voice.js
class VoiceInput {
    constructor() {
        this.recognition = new webkitSpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
    }
    
    startListening() {
        this.recognition.start();
    }
    
    onResult(callback) {
        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            callback(transcript);
        };
    }
}
```

### 2.4 **Real-time Budget Display**
```javascript
// static/js/budget.js
const socket = io();

socket.on('budget_update', (data) => {
    document.getElementById('budget-remaining').textContent = 
        data.remaining.toFixed(2);
    
    if (data.remaining <= 0) {
        showBudgetExhaustedModal();
    }
});
```

---

## 📋 **Phase 3: Deployment Setup (1 day)**

### 3.1 **RPI + Nginx Configuration**
```nginx
# /etc/nginx/sites-available/ralex
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 3.2 **SSL Certificate (Let's Encrypt)**
```bash
# Auto HTTPS setup
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 3.3 **Systemd Service**
```ini
# /etc/systemd/system/ralex-web.service
[Unit]
Description=Ralex V3 Web Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ralex
ExecStart=/home/pi/ralex/.venv/bin/python -m ralex_core.web_api
Restart=always
Environment=OPENROUTER_API_KEY=your-key

[Install]
WantedBy=multi-user.target
```

---

## 📋 **Phase 4: Voice Workflow Optimization (1 day)**

### 4.1 **Mobile Voice UX**
- **Large voice button** for easy thumb access
- **Visual feedback** during speech recognition
- **Auto-submit** after speech ends
- **Quick budget presets** ("$0.25", "$1.00", "$5.00")

### 4.2 **Voice Feedback Integration**
Your ideal workflow:
1. **Speak request** → Speech-to-text
2. **AI processes** → Shows response + budget used
3. **You respond vocally** → Next iteration
4. **Budget tracking** → "You have $0.75 left"

### 4.3 **Smart Budget Challenges**
```python
# Budget challenge mode
def start_budget_challenge(amount: float, task: str):
    session = create_session(budget_limit=amount)
    return {
        "session_id": session.id,
        "challenge": f"Complete '{task}' with ${amount}",
        "remaining": amount
    }
```

---

## 📋 **Phase 5: Advanced Features (Optional)**

### 5.1 **Voice Synthesis (Text-to-Speech)**
- Read AI responses aloud
- Hands-free coding sessions
- Background voice updates

### 5.2 **Mobile PWA**
- Offline capability
- Install on phone homescreen
- Push notifications for budget updates

### 5.3 **Multi-Session Management**
- Separate projects with individual budgets
- Session history and resumption
- Team collaboration features

---

## 🛠️ **Implementation Priority**

### **Weekend 1: Core Foundation**
- [ ] Backend API endpoints (Flask + SocketIO)
- [ ] Basic web interface (fork Open WebUI)
- [ ] Voice input integration
- [ ] Budget tracking display

### **Weekend 2: Deployment**
- [ ] RPI + nginx setup
- [ ] Domain + SSL configuration
- [ ] Mobile optimization
- [ ] Voice workflow testing

### **Weekend 3: Polish**
- [ ] Budget challenge features
- [ ] Voice feedback loop
- [ ] Mobile PWA setup
- [ ] Performance optimization

---

## 💰 **Cost Estimate**

**Development Time**: 6-8 days (3 weekends)
**Ongoing Costs**: 
- Domain: $12/year
- Let's Encrypt SSL: Free
- RPI hosting: Free (your existing setup)
- OpenRouter API: Your existing usage

**Total Additional Cost**: ~$12/year

---

## 🚀 **Technical Stack Summary**

**Backend**: 
- Current Ralex V2 core
- Flask web framework
- SocketIO for real-time updates
- Session-based budget management

**Frontend**:
- Fork of Open WebUI or vanilla JS
- Web Speech API for voice input
- WebSocket for real-time updates
- Mobile-responsive design

**Deployment**:
- Your existing RPI
- Nginx reverse proxy
- Let's Encrypt SSL
- Systemd service management

**Result**: Voice-driven, web-accessible AI coding assistant that works perfectly for your "vibe coding" workflow from phone/desktop with real-time budget tracking.

---

## 🎯 **Success Metrics**

After V3 completion, you'll have:
- ✅ Voice-to-text coding from your phone
- ✅ Real-time budget conversations ("here's $1...")
- ✅ Web access from anywhere
- ✅ Perfect mobile "vibe coding" experience
- ✅ All existing V2 functionality preserved

**Ready to build your dream coding interface! 🚀**