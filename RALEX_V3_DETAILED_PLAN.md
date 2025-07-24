# Ralex V3 Implementation Plan: Open WebUI + AgentOS Integration

## 🎯 **Project Overview**

Transform Ralex V2 into a voice-first, web-accessible AI coding assistant using Open WebUI's proven interface with AgentOS workflow integration, deployed via Tailscale.

**Core Architecture:**
```
Voice Input → Open WebUI Frontend → Ralex Backend → OpenRouter API
     ↓              ↓                    ↓               ↓
Web Speech API → WebSocket → AgentOS + Semantic Router → Model Selection
```

---

## 📋 **Phase 1: Backend API Transformation (12-16 hours)**

### Task 1.1: OpenAI-Compatible API Layer (4-5 hours)
**Goal**: Make Ralex backend compatible with Open WebUI's expectations

**File Changes:**
- `ralex_core/openai_api.py` (NEW) - OpenAI-compatible endpoints
- `ralex_core/launcher.py` - Add FastAPI web server
- `requirements.txt` - Add fastapi, uvicorn, websockets

**Implementation Details:**
```python
# ralex_core/openai_api.py
from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse
import json

app = FastAPI()

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """OpenAI-compatible chat endpoint for Open WebUI"""
    
    # 1. Extract user message and context
    user_message = request.messages[-1]["content"]
    conversation_history = request.messages[:-1]
    
    # 2. AgentOS Integration - Apply standards and context
    agentos = AgentOSIntegration()
    enhanced_prompt = agentos.enhance_with_standards(user_message)
    project_context = agentos.get_project_context()
    
    # 3. Semantic classification and routing
    classifier = SemanticClassifier()
    intent = classifier.classify_intent(enhanced_prompt)
    
    router = SmartRouter()
    selected_model = router.select_model(intent, enhanced_prompt, budget_context)
    
    # 4. Budget tracking integration
    budget_manager = BudgetManager()
    session_budget = budget_manager.get_session_budget(request.user_id)
    
    if request.stream:
        return StreamingResponse(
            stream_ralex_response(enhanced_prompt, selected_model, session_budget),
            media_type="text/plain"
        )
    else:
        # Non-streaming response
        response = await get_ralex_response(enhanced_prompt, selected_model)
        return format_openai_response(response)

async def stream_ralex_response(prompt, model, budget):
    """Stream responses in OpenAI format"""
    # Call existing Ralex logic but format as OpenAI chunks
    for chunk in ralex_streaming_response(prompt, model):
        openai_chunk = {
            "id": "chatcmpl-ralex",
            "object": "chat.completion.chunk",
            "choices": [{
                "delta": {"content": chunk},
                "index": 0,
                "finish_reason": None
            }]
        }
        yield f"data: {json.dumps(openai_chunk)}\n\n"
```

**Deliverables:**
- [ ] FastAPI server integration with existing launcher
- [ ] OpenAI-compatible `/v1/chat/completions` endpoint
- [ ] Streaming response support
- [ ] Error handling and validation
- [ ] Integration with existing semantic routing

### Task 1.2: AgentOS Standards Integration (3-4 hours)
**Goal**: Enhance all AI requests with AgentOS standards and project context

**File Changes:**
- `ralex_core/agentos_integration.py` - Enhanced integration
- `agent_os/standards/` - Update standards for web usage
- `ralex_core/context_manager.py` (NEW) - File context for web interface

**Implementation Details:**
```python
# ralex_core/agentos_integration.py (Enhanced)
class AgentOSWebIntegration(AgentOSIntegration):
    def __init__(self):
        super().__init__()
        self.web_standards = self.load_web_standards()
    
    def enhance_web_request(self, user_message: str, session_context: dict) -> str:
        """Enhance user request with AgentOS standards for web interface"""
        
        # 1. Apply project-specific standards
        project_context = self.get_project_context()
        
        # 2. Add file context if files are referenced
        file_context = self.extract_file_context(user_message, session_context)
        
        # 3. Apply coding standards and best practices
        standards_prompt = self.build_standards_prompt()
        
        # 4. Combine into enhanced prompt
        enhanced_prompt = f"""
{standards_prompt}

Project Context:
{project_context}

File Context:
{file_context}

User Request:
{user_message}

Please follow all standards above and provide code that adheres to the project patterns.
"""
        return enhanced_prompt
    
    def load_web_standards(self) -> dict:
        """Load standards optimized for web-based interactions"""
        return {
            "response_format": "Provide code in properly formatted blocks",
            "file_handling": "Always specify full file paths",
            "explanations": "Keep explanations concise for web UI",
            "error_handling": "Include error scenarios and edge cases"
        }
```

**Deliverables:**
- [ ] Web-optimized standards integration
- [ ] File context management for web sessions
- [ ] Project context extraction
- [ ] Standards prompt building for web UI

### Task 1.3: Session and Budget Management (2-3 hours)
**Goal**: Web-compatible session management with real-time budget tracking

**File Changes:**
- `ralex_core/web_session.py` (NEW) - Web session management
- `ralex_core/budget.py` - Enhanced for web sessions
- `ralex_core/websocket_manager.py` (NEW) - Real-time updates

**Implementation Details:**
```python
# ralex_core/web_session.py
import uuid
from datetime import datetime, timedelta

class WebSessionManager:
    def __init__(self):
        self.active_sessions = {}
        self.session_budgets = {}
    
    def create_session(self, initial_budget: float = 5.0) -> str:
        """Create new web session with budget"""
        session_id = str(uuid.uuid4())
        self.active_sessions[session_id] = {
            "created_at": datetime.now(),
            "conversation_history": [],
            "file_context": {},
            "project_context": None
        }
        self.session_budgets[session_id] = {
            "initial": initial_budget,
            "remaining": initial_budget,
            "spent": 0.0,
            "transactions": []
        }
        return session_id
    
    def update_budget(self, session_id: str, cost: float, model: str, task: str):
        """Update session budget and broadcast via WebSocket"""
        if session_id in self.session_budgets:
            budget = self.session_budgets[session_id]
            budget["remaining"] -= cost
            budget["spent"] += cost
            budget["transactions"].append({
                "timestamp": datetime.now().isoformat(),
                "cost": cost,
                "model": model,
                "task": task
            })
            
            # Broadcast update via WebSocket
            websocket_manager.broadcast_budget_update(session_id, budget)
```

**Deliverables:**
- [ ] Session creation and management
- [ ] Real-time budget tracking
- [ ] WebSocket budget updates
- [ ] Session persistence options

### Task 1.4: WebSocket Integration (3-4 hours)
**Goal**: Real-time communication for chat and budget updates

**File Changes:**
- `ralex_core/websocket_manager.py` (NEW) - WebSocket handling
- `ralex_core/openai_api.py` - WebSocket endpoints
- Frontend integration planning

**Implementation Details:**
```python
# ralex_core/websocket_manager.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.session_connections: Dict[str, List[str]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Connect new WebSocket for session"""
        await websocket.accept()
        connection_id = str(uuid.uuid4())
        self.active_connections[connection_id] = websocket
        
        if session_id not in self.session_connections:
            self.session_connections[session_id] = []
        self.session_connections[session_id].append(connection_id)
        
        return connection_id
    
    async def broadcast_budget_update(self, session_id: str, budget_data: dict):
        """Broadcast budget updates to all session connections"""
        if session_id in self.session_connections:
            message = {
                "type": "budget_update",
                "data": budget_data
            }
            for connection_id in self.session_connections[session_id]:
                if connection_id in self.active_connections:
                    await self.active_connections[connection_id].send_text(
                        json.dumps(message)
                    )
    
    async def broadcast_typing_indicator(self, session_id: str, is_typing: bool):
        """Show AI typing indicator"""
        message = {
            "type": "typing_indicator",
            "data": {"is_typing": is_typing}
        }
        # Similar broadcast logic...
```

**Deliverables:**
- [ ] WebSocket connection management
- [ ] Real-time budget updates
- [ ] Typing indicators
- [ ] Connection cleanup and error handling

---

## 📋 **Phase 2: Open WebUI Customization (8-10 hours)**

### Task 2.1: Fork and Setup Open WebUI (1-2 hours)
**Goal**: Set up customized Open WebUI instance for Ralex

**Steps:**
1. **Fork Open WebUI repository**
```bash
git clone https://github.com/open-webui/open-webui.git ralex-webui
cd ralex-webui

# Update configuration for Ralex backend
cp .env.example .env
```

2. **Configure for Ralex backend**
```env
# .env
OPENAI_API_BASE_URL=http://localhost:8000/v1
ENABLE_OPENAI_API=true
WEBUI_SECRET_KEY=your-secret-key
ENABLE_SIGNUP=false
DEFAULT_MODELS=ralex-smart,ralex-fast,ralex-budget
RALEX_BACKEND_URL=http://localhost:8000
```

3. **Customize branding and naming**
- Update title to "Ralex Voice Coding Assistant"
- Update logos and favicon
- Modify color scheme to match Ralex branding

**Deliverables:**
- [ ] Forked and configured Open WebUI
- [ ] Ralex-specific environment configuration
- [ ] Basic branding customization
- [ ] Development environment setup

### Task 2.2: Voice Input Integration (3-4 hours)
**Goal**: Add voice input capabilities to Open WebUI interface

**File Changes:**
- `src/lib/components/chat/MessageInput.svelte` - Add voice button
- `src/lib/utils/voice.js` (NEW) - Voice input handling
- `src/lib/stores/voice.js` (NEW) - Voice state management

**Implementation Details:**
```javascript
// src/lib/utils/voice.js
export class VoiceInputManager {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.initializeRecognition();
    }
    
    initializeRecognition() {
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.onTranscript(transcript);
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.isListening = false;
            };
        }
    }
    
    startListening(callback) {
        if (this.recognition && !this.isListening) {
            this.onTranscript = callback;
            this.recognition.start();
            this.isListening = true;
        }
    }
    
    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
            this.isListening = false;
        }
    }
}
```

```svelte
<!-- src/lib/components/chat/MessageInput.svelte (Enhanced) -->
<script>
    import { VoiceInputManager } from '$lib/utils/voice.js';
    import { voiceStore } from '$lib/stores/voice.js';
    
    let voiceManager = new VoiceInputManager();
    let isRecording = false;
    
    const startVoiceInput = () => {
        isRecording = true;
        voiceManager.startListening((transcript) => {
            prompt = transcript;
            isRecording = false;
            // Auto-submit or wait for user confirmation
            if (autoSubmitVoice) {
                submitPrompt();
            }
        });
    };
    
    const stopVoiceInput = () => {
        voiceManager.stopListening();
        isRecording = false;
    };
</script>

<div class="voice-input-container">
    <button 
        class="voice-button {isRecording ? 'recording' : ''}"
        on:click={isRecording ? stopVoiceInput : startVoiceInput}
        title={isRecording ? 'Stop recording' : 'Start voice input'}
    >
        {#if isRecording}
            🔴 Recording...
        {:else}
            🎤 Voice
        {/if}
    </button>
</div>

<style>
    .voice-button {
        @apply px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600;
        transition: all 0.2s ease;
    }
    
    .voice-button.recording {
        @apply bg-red-500 hover:bg-red-600;
        animation: pulse 1s infinite;
    }
</style>
```

**Deliverables:**
- [ ] Voice input button in chat interface
- [ ] Web Speech API integration
- [ ] Visual feedback for recording state
- [ ] Auto-submit option for voice input
- [ ] Error handling for unsupported browsers

### Task 2.3: Budget Display Integration (2-3 hours)
**Goal**: Real-time budget display and management in UI

**File Changes:**
- `src/lib/components/layout/Sidebar.svelte` - Add budget widget
- `src/lib/components/budget/BudgetWidget.svelte` (NEW) - Budget display
- `src/lib/stores/budget.js` (NEW) - Budget state management
- `src/lib/utils/websocket.js` - WebSocket for budget updates

**Implementation Details:**
```svelte
<!-- src/lib/components/budget/BudgetWidget.svelte -->
<script>
    import { budgetStore } from '$lib/stores/budget.js';
    import { onMount } from 'svelte';
    
    let budgetData = {};
    
    onMount(() => {
        // Subscribe to budget updates
        budgetStore.subscribe(value => {
            budgetData = value;
        });
        
        // Connect to WebSocket for real-time updates
        connectBudgetWebSocket();
    });
    
    const addBudget = (amount) => {
        budgetStore.addBudget(amount);
    };
    
    const resetBudget = () => {
        budgetStore.resetBudget();
    };
</script>

<div class="budget-widget">
    <div class="budget-header">
        <h3>Session Budget</h3>
        <div class="budget-amount {budgetData.remaining < 1 ? 'low' : ''}">
            ${budgetData.remaining?.toFixed(2) || '0.00'}
        </div>
    </div>
    
    <div class="budget-progress">
        <div class="progress-bar">
            <div 
                class="progress-fill" 
                style="width: {(budgetData.spent / budgetData.initial) * 100}%"
            ></div>
        </div>
        <div class="progress-text">
            ${budgetData.spent?.toFixed(2) || '0.00'} of ${budgetData.initial?.toFixed(2) || '0.00'} spent
        </div>
    </div>
    
    <div class="budget-actions">
        <button on:click={() => addBudget(1.00)}>Add $1</button>
        <button on:click={() => addBudget(5.00)}>Add $5</button>
        <button on:click={() => addBudget(0.25)}>Add $0.25</button>
        <button on:click={resetBudget} class="reset">Reset</button>
    </div>
    
    {#if budgetData.transactions?.length > 0}
        <div class="recent-transactions">
            <h4>Recent Usage</h4>
            {#each budgetData.transactions.slice(-3) as transaction}
                <div class="transaction">
                    <span class="task">{transaction.task}</span>
                    <span class="cost">${transaction.cost.toFixed(3)}</span>
                    <span class="model">{transaction.model}</span>
                </div>
            {/each}
        </div>
    {/if}
</div>
```

**Deliverables:**
- [ ] Budget widget in sidebar
- [ ] Real-time budget updates via WebSocket
- [ ] Budget addition buttons ($0.25, $1, $5)
- [ ] Transaction history display
- [ ] Visual warnings for low budget

### Task 2.4: Ralex-Specific UI Customizations (2-3 hours)
**Goal**: Customize Open WebUI for coding-focused workflows

**File Changes:**
- `src/lib/components/chat/MessageInput.svelte` - Coding shortcuts  
- `src/lib/components/chat/Messages.svelte` - Code block improvements
- `src/app.html` - Custom CSS and branding
- `src/lib/components/layout/Navbar.svelte` - Ralex branding

**Implementation Details:**
```svelte
<!-- Enhanced MessageInput with coding shortcuts -->
<script>
    const codingShortcuts = [
        { label: "Fix Bug", prompt: "Please analyze and fix this bug: " },
        { label: "Refactor", prompt: "Please refactor this code for better performance and readability: " },
        { label: "Add Tests", prompt: "Please add comprehensive tests for: " },
        { label: "Code Review", prompt: "Please review this code and suggest improvements: " },
        { label: "Explain", prompt: "Please explain how this code works: " }
    ];
    
    const insertShortcut = (shortcut) => {
        prompt = shortcut.prompt;
        textarea.focus();
    };
</script>

<div class="coding-shortcuts">
    {#each codingShortcuts as shortcut}
        <button 
            class="shortcut-btn"
            on:click={() => insertShortcut(shortcut)}
        >
            {shortcut.label}
        </button>
    {/each}
</div>
```

**Enhanced Features:**
- Coding-specific quick prompts
- Better syntax highlighting for code blocks
- File context indicators
- Model selection indicators (Smart/Fast/Budget)
- Dark theme optimization for coding

**Deliverables:**
- [ ] Coding-focused quick prompts
- [ ] Enhanced code block display
- [ ] File context management UI
- [ ] Model selection indicators
- [ ] Ralex branding and theming

---

## 📋 **Phase 3: Tailscale Deployment (2-3 hours)**

### Task 3.1: Production Configuration (1 hour)
**Goal**: Configure both Ralex backend and Open WebUI for production

**File Changes:**
- `docker-compose.yml` (NEW) - Multi-service deployment
- `nginx/ralex.conf` (NEW) - Nginx configuration
- `systemd/ralex-web.service` (NEW) - Service configuration

**Implementation Details:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  ralex-backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - RALEX_ENV=production
    volumes:
      - ./config:/app/config
      - ./data:/app/data
  
  ralex-webui:
    build: ./ralex-webui
    ports:
      - "3000:8080"
    environment:
      - OPENAI_API_BASE_URL=http://ralex-backend:8000/v1
      - WEBUI_SECRET_KEY=${WEBUI_SECRET_KEY}
    depends_on:
      - ralex-backend
  
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx/ralex.conf:/etc/nginx/conf.d/default.conf
      - /var/lib/tailscale/certs:/etc/nginx/certs
    depends_on:
      - ralex-webui
      - ralex-backend
```

```nginx
# nginx/ralex.conf
server {
    listen 443 ssl http2;
    server_name rpi3.your-tailnet.ts.net;
    
    ssl_certificate /etc/nginx/certs/rpi3.your-tailnet.ts.net.crt;
    ssl_certificate_key /etc/nginx/certs/rpi3.your-tailnet.ts.net.key;
    
    # Frontend (Open WebUI)
    location / {
        proxy_pass http://ralex-webui:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://ralex-backend:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # WebSocket for real-time updates
    location /ws/ {
        proxy_pass http://ralex-backend:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

**Deliverables:**
- [ ] Docker Compose configuration
- [ ] Nginx reverse proxy setup
- [ ] SSL certificate configuration
- [ ] Environment variable management

### Task 3.2: Tailscale HTTPS Setup (30 minutes)
**Goal**: Enable Tailscale HTTPS certificates

**Steps:**
```bash
# Enable Tailscale HTTPS
sudo tailscale cert $(tailscale status --json | jq -r '.Self.DNSName')

# Verify certificates
ls -la /var/lib/tailscale/certs/

# Update nginx permissions
sudo chown -R nginx:nginx /var/lib/tailscale/certs/
```

**Deliverables:**
- [ ] Tailscale HTTPS certificates
- [ ] Nginx certificate configuration
- [ ] Certificate renewal setup

### Task 3.3: Service Deployment (1 hour)
**Goal**: Deploy as systemd services for reliability

**Implementation:**
```ini
# systemd/ralex-web.service
[Unit]
Description=Ralex V3 Web Services
After=network.target docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/ralex
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target  
```

**Deployment Steps:**
```bash
# Copy service file
sudo cp systemd/ralex-web.service /etc/systemd/system/

# Enable and start
sudo systemctl enable ralex-web.service
sudo systemctl start ralex-web.service

# Check status
sudo systemctl status ralex-web.service
```

**Deliverables:**
- [ ] Systemd service configuration
- [ ] Automatic startup on boot
- [ ] Service monitoring and restart policies
- [ ] Health check endpoints

---

## 📋 **Phase 4: Testing and Optimization (3-4 hours)**

### Task 4.1: Integration Testing (2 hours)
**Goal**: Comprehensive testing of all components

**Test Scenarios:**
```javascript
// Voice Input Tests
- Test voice recognition in Chrome/Safari
- Test auto-submit vs manual submit
- Test voice error handling
- Test microphone permissions

// Budget Management Tests  
- Test budget updates in real-time
- Test budget limits and warnings
- Test budget addition functionality
- Test WebSocket reconnection

// AgentOS Integration Tests
- Test standards application
- Test project context loading
- Test file context management
- Test slash command equivalents

// Backend API Tests
- Test OpenAI compatibility
- Test streaming responses  
- Test error handling
- Test model selection logic
```

**Deliverables:**
- [ ] Automated test suite
- [ ] Manual testing checklist
- [ ] Performance benchmarks
- [ ] Error scenario testing

### Task 4.2: Mobile Optimization (1-2 hours) 
**Goal**: Ensure perfect mobile experience

**Mobile Features:**
- Touch-friendly voice button (large, accessible)
- Responsive budget widget
- Mobile-optimized chat interface
- Landscape/portrait mode support
- Keyboard handling improvements

**Deliverables:**
- [ ] Mobile-responsive design
- [ ] Touch interaction optimization
- [ ] Cross-device testing
- [ ] iOS/Android compatibility

---

## 🎯 **Success Criteria & Deliverables**

### **Minimum Viable Product (MVP)**
- [ ] Voice input working in web browser
- [ ] Real-time budget tracking and display
- [ ] AgentOS standards automatically applied
- [ ] Tailscale HTTPS deployment
- [ ] Mobile-friendly interface

### **Full Feature Set**
- [ ] All existing Ralex V2 functionality preserved
- [ ] Open WebUI chat interface fully functional
- [ ] WebSocket real-time updates
- [ ] Session management and persistence
- [ ] Production-ready deployment

### **Performance Targets**
- Voice input latency: < 2 seconds
- Budget updates: < 500ms
- Chat response streaming: < 1 second first token
- Mobile load time: < 3 seconds
- Uptime: 99%+ with systemd auto-restart

---

## 📅 **Implementation Timeline**

**Weekend 1 (12-16 hours):**
- Phase 1: Backend API transformation
- Phase 2.1-2.2: Open WebUI setup and voice integration

**Weekend 2 (8-10 hours):** 
- Phase 2.3-2.4: Budget display and UI customization
- Phase 3: Tailscale deployment
- Phase 4: Testing and optimization

**Total Time Estimate: 20-26 hours over 2-3 weekends**

---

## 🚀 **Post-Implementation Enhancements**

**Future Features to Consider:**
- Text-to-speech for AI responses
- File upload via drag-and-drop
- Advanced voice commands ("Ralex, refactor this function")
- Multi-session management
- Team collaboration features
- Advanced budget analytics
- Voice shortcuts for common commands

This plan provides a comprehensive roadmap for transforming Ralex V2 into a world-class voice-driven coding assistant with professional web interface and AgentOS workflow integration.