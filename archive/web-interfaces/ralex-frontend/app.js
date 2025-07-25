/**
 * Ralex V3 Frontend - Voice-driven AI Coding Assistant
 * Features: Voice input, real-time budget tracking, WebSocket updates
 */

class RalexApp {
    constructor() {
        this.apiBase = 'http://localhost:8000';
        this.sessionId = null;
        this.websocket = null;
        this.isRecording = false;
        this.recognition = null;
        this.messageCount = 0;
        this.currentBudget = { remaining: 4.00, total: 5.00 };
        
        this.initializeApp();
    }
    
    async initializeApp() {
        await this.createSession();
        this.setupWebSocket();
        this.setupEventListeners();
        this.setupVoiceRecognition();
        this.loadChatHistory();
    }
    
    async createSession() {
        try {
            // Session will be created automatically by the API
            this.sessionId = `session_${Date.now()}`;
            document.getElementById('sessionId').textContent = this.sessionId.slice(-8);
            document.getElementById('sessionStart').textContent = new Date().toLocaleTimeString();
        } catch (error) {
            console.error('Failed to create session:', error);
            this.showMessage('system', 'Failed to connect to Ralex API. Please check if the server is running.');
        }
    }
    
    setupWebSocket() {
        try {
            this.websocket = new WebSocket(`ws://localhost:8000/ws/${this.sessionId}`);
            
            this.websocket.onopen = () => {
                console.log('WebSocket connected');
                document.getElementById('status').textContent = 'Connected';
                document.getElementById('status').style.background = '#1a4d3a';
                document.getElementById('status').style.color = '#00ff88';
            };
            
            this.websocket.onmessage = (event) => {
                const message = JSON.parse(event.data);
                this.handleWebSocketMessage(message);
            };
            
            this.websocket.onclose = () => {
                console.log('WebSocket disconnected');
                document.getElementById('status').textContent = 'Disconnected';
                document.getElementById('status').style.background = '#4d1a1a';
                document.getElementById('status').style.color = '#ff4444';
                
                // Attempt to reconnect after 3 seconds
                setTimeout(() => this.setupWebSocket(), 3000);
            };
            
            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        } catch (error) {
            console.error('Failed to setup WebSocket:', error);
        }
    }
    
    handleWebSocketMessage(message) {
        switch (message.type) {
            case 'budget_update':
                this.updateBudgetDisplay(message.data);
                break;
            case 'typing_indicator':
                this.showTypingIndicator(message.data.is_typing, message.data.model);
                break;
            case 'model_selection':
                this.updateModelInfo(message.data);
                break;
            case 'system_notification':
                this.showMessage('system', message.data.message);
                break;
            case 'session_info':
                this.updateSessionInfo(message.data);
                break;
            default:
                console.log('Unknown WebSocket message:', message);
        }
    }
    
    setupEventListeners() {
        const chatInput = document.getElementById('chatInput');
        const sendBtn = document.getElementById('sendBtn');
        
        // Send message on Ctrl+Enter
        chatInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
        
        // Send button click
        sendBtn.addEventListener('click', () => this.sendMessage());
    }
    
    setupVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                document.getElementById('chatInput').value = transcript;
                this.stopVoiceInput();
                
                // Auto-send if the transcript ends with specific phrases
                const autoSendPhrases = ['send it', 'execute', 'run it', 'go ahead'];
                if (autoSendPhrases.some(phrase => transcript.toLowerCase().includes(phrase))) {
                    setTimeout(() => this.sendMessage(), 500);
                }
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.stopVoiceInput();
                this.showMessage('system', `Voice recognition error: ${event.error}`);
            };
            
            this.recognition.onend = () => {
                this.stopVoiceInput();
            };
        } else {
            console.warn('Speech recognition not supported');
            document.getElementById('voiceBtn').style.opacity = '0.5';
            document.getElementById('voiceBtn').onclick = () => {
                this.showMessage('system', 'Voice recognition is not supported in this browser');
            };
        }
    }
    
    toggleVoiceInput() {
        if (!this.recognition) return;
        
        if (this.isRecording) {
            this.stopVoiceInput();
        } else {
            this.startVoiceInput();
        }
    }
    
    startVoiceInput() {
        if (!this.recognition) return;
        
        this.isRecording = true;
        const voiceBtn = document.getElementById('voiceBtn');
        voiceBtn.classList.add('recording');
        voiceBtn.textContent = '🛑';
        
        try {
            this.recognition.start();
            this.showMessage('system', 'Listening... (Click the button again to stop)');
        } catch (error) {
            console.error('Failed to start voice recognition:', error);
            this.stopVoiceInput();
        }
    }
    
    stopVoiceInput() {
        if (!this.recognition) return;
        
        this.isRecording = false;
        const voiceBtn = document.getElementById('voiceBtn');
        voiceBtn.classList.remove('recording');
        voiceBtn.textContent = '🎙️';
        
        try {
            this.recognition.stop();
        } catch (error) {
            console.error('Error stopping voice recognition:', error);
        }
    }
    
    async sendMessage() {
        const chatInput = document.getElementById('chatInput');
        const message = chatInput.value.trim();
        
        if (!message) return;
        
        // Clear input and disable send button
        chatInput.value = '';
        chatInput.style.height = 'auto';
        document.getElementById('sendBtn').disabled = true;
        
        // Show user message
        this.showMessage('user', message);
        this.messageCount++;
        document.getElementById('messageCount').textContent = this.messageCount;
        
        try {
            // Send to Ralex API
            const response = await fetch(`${this.apiBase}/v1/chat/completions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ralex-api-key'
                },
                body: JSON.stringify({
                    model: 'ralex-smart',
                    messages: [
                        { role: 'user', content: message }
                    ],
                    stream: false,
                    user: this.sessionId
                })
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }
            
            const data = await response.json();
            const assistantMessage = data.choices[0].message.content;
            
            // Show assistant response
            this.showMessage('assistant', assistantMessage);
            this.messageCount++;
            document.getElementById('messageCount').textContent = this.messageCount;
            
            // Update usage info
            if (data.usage) {
                const cost = data.usage.total_tokens * 0.000002; // Rough estimate
                document.getElementById('lastCost').textContent = `$${cost.toFixed(6)}`;
            }
            
        } catch (error) {
            console.error('Failed to send message:', error);
            this.showMessage('system', `Error: ${error.message}`);
        } finally {
            document.getElementById('sendBtn').disabled = false;
        }
    }
    
    showMessage(role, content) {
        const chatContainer = document.getElementById('chatContainer');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        
        if (role === 'assistant') {
            // Simple markdown-like formatting
            content = content
                .replace(/```([\\s\\S]*?)```/g, '<pre><code>$1</code></pre>')
                .replace(/`([^`]+)`/g, '<code>$1</code>')
                .replace(/\\*\\*([^*]+)\\*\\*/g, '<strong>$1</strong>')
                .replace(/\\*([^*]+)\\*/g, '<em>$1</em>');
        }
        
        messageDiv.innerHTML = content;
        chatContainer.appendChild(messageDiv);
        
        // Auto-scroll to bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    showTypingIndicator(isTyping, model = '') {
        const indicator = document.getElementById('typingIndicator');
        if (isTyping) {
            indicator.style.display = 'flex';
            if (model) {
                indicator.querySelector('span').textContent = `${model} is thinking`;
            }
        } else {
            indicator.style.display = 'none';
        }
    }
    
    updateBudgetDisplay(budgetData) {
        if (budgetData.remaining !== undefined) {
            this.currentBudget.remaining = budgetData.remaining;
            document.getElementById('budgetRemaining').textContent = budgetData.remaining.toFixed(2);
        }
        if (budgetData.limit !== undefined) {
            this.currentBudget.total = budgetData.limit;
            document.getElementById('budgetTotal').textContent = budgetData.limit.toFixed(2);
        }
        
        // Update progress bar
        const percentage = (this.currentBudget.remaining / this.currentBudget.total) * 100;
        const progressBar = document.getElementById('budgetProgress');
        progressBar.style.width = `${Math.max(0, percentage)}%`;
        
        // Change color based on remaining budget
        if (percentage < 20) {
            progressBar.style.background = '#ff4444';
        } else if (percentage < 50) {
            progressBar.style.background = '#ffaa00';
        } else {
            progressBar.style.background = '#00ff88';
        }
    }
    
    updateModelInfo(modelData) {
        if (modelData.model) {
            document.getElementById('currentModel').textContent = modelData.model;
        }
        if (modelData.reasoning) {
            // Show model selection reasoning as a system message
            this.showMessage('system', `🧠 Selected ${modelData.model}: ${modelData.reasoning}`);
        }
    }
    
    updateSessionInfo(sessionData) {
        if (sessionData.files_in_context !== undefined) {
            document.getElementById('fileCount').textContent = sessionData.files_in_context;
        }
        if (sessionData.conversation_length !== undefined) {
            this.messageCount = sessionData.conversation_length;
            document.getElementById('messageCount').textContent = this.messageCount;
        }
    }
    
    async addBudget() {
        try {
            const response = await fetch(`${this.apiBase}/api/sessions/${this.sessionId}/budget/add`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(1.00) // Add $1.00
            });
            
            if (response.ok) {
                const result = await response.json();
                this.showMessage('system', `💰 Added $1.00 to budget. New total: $${result.new_limit.toFixed(2)}`);
            }
        } catch (error) {
            console.error('Failed to add budget:', error);
            this.showMessage('system', 'Failed to add budget. Please try again.');
        }
    }
    
    async loadChatHistory() {
        // In a real implementation, this would load previous conversation
        // For now, just show the welcome message
        setTimeout(() => {
            this.showMessage('system', '🚀 Ralex V3 is ready! Try saying "Create a Python function to calculate fibonacci numbers" or use the microphone button.');
        }, 1000);
    }
}

// Global functions for HTML event handlers
window.toggleVoiceInput = () => app.toggleVoiceInput();
window.sendMessage = () => app.sendMessage();
window.addBudget = () => app.addBudget();

// Initialize the app when the page loads
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new RalexApp();
});

// Handle page visibility changes to manage WebSocket connections
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Page is hidden, could pause some activities
    } else {
        // Page is visible, ensure WebSocket is connected
        if (app && (!app.websocket || app.websocket.readyState !== WebSocket.OPEN)) {
            app.setupWebSocket();
        }
    }
});