# Ralex V4 Setup Guide

## What V4 Delivers
Voice-driven coding assistant that orchestrates 5 core components:
- **AgentOS**: Strategic thinking and standards enforcement
- **LiteLLM**: Model selection and cost optimization  
- **OpenRouter**: LLM API access with multiple providers
- **OpenCode**: Autonomous coding execution engine
- **OpenWebUI**: Voice/web frontend interface

## Quick Test (Without Dependencies)
```bash
# Test the bridge directly
python ralex_bridge.py "create a test.py file with print('working!')"

# Check results
ls test.py
cat .ralex/session_*.md
```

## Full Integration Setup

### 1. Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Environment Variables  
```bash
export OPENROUTER_API_KEY="your-openrouter-key"
```

### 3. Start Full Stack
```bash
python start_ralex_v4.py
```

This will:
- Start RalexBridge API on port 8000
- Configure OpenWebUI to use the bridge
- Start OpenWebUI on port 8080
- Enable voice commands → coding actions

## Architecture Flow

```
Voice Input (OpenWebUI) 
    ↓
AgentOS Strategic Filter
    ↓  
LiteLLM Model Selection
    ↓
OpenRouter API Call
    ↓
OpenCode Execution
    ↓
Context Saved (.ralex/*.md)
    ↓
Git Auto-Commit
```

## Files Created
- `ralex_bridge.py`: Core orchestrator (150 lines)
- `ralex_api.py`: FastAPI wrapper for OpenWebUI  
- `start_ralex_v4.py`: Full stack startup script
- Updated `opencode_client.py`: Fixed file writing

## Testing Commands
- "create a hello.py file with print statement"
- "write a simple calculator function"  
- "add error handling to my code"

## Context Persistence
All sessions saved to `.ralex/session_TIMESTAMP.md` with:
- Original prompt
- AgentOS thinking analysis
- Model selected  
- AI response
- Execution results

Sessions auto-committed to git for cross-device sync.

## What's Different from V3
- **Simplified**: No custom routers, just orchestration
- **Integrated**: All 5 components work together seamlessly  
- **Strategic**: AgentOS forces structured thinking before execution
- **Persistent**: Full context history with git sync
- **Voice-enabled**: OpenWebUI provides speech-to-text interface

Total implementation: ~300 lines of orchestration code vs 2000+ lines of custom components.