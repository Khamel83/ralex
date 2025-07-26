# Ralex V4 - Voice-Controlled AI Coding Assistant

**🎯 Talk to code. Ralex V4 orchestrates 5 AI tools to turn your voice into working software.**

## What Is This?

Ralex V4 is a voice-controlled coding assistant that connects multiple AI tools to create a seamless development experience. Instead of switching between different AI tools, Ralex orchestrates them all together.

### The Magic: 5 Tools Working as One

1. **OpenWebUI** - Voice interface (speak your commands)
2. **AgentOS** - Strategic thinking (prevents bad decisions)  
3. **LiteLLM** - Model selection (picks cheapest appropriate AI)
4. **OpenRouter** - AI access (connects to 100+ models)
5. **OpenCode** - Code execution (actually writes/edits files)

## Why Ralex V4?

### Before Ralex (The Old Way)
- Switch between ChatGPT, Claude, and coding tools
- Copy/paste code between applications
- Lose context between sessions
- Pay premium prices for simple tasks
- Type everything manually

### With Ralex V4 (The New Way)
- Say: "Create a web scraper for news articles"
- Ralex thinks strategically about the request
- Selects the right AI model for the task
- Writes the actual code files
- Saves the entire conversation
- Costs 10x less than premium subscriptions

## 5-Minute Setup

### Get Your Free API Key
1. Go to [OpenRouter.ai](https://openrouter.ai) 
2. Sign up (free tier included)
3. Copy your API key

### Install Ralex
```bash
git clone https://github.com/Khamel83/ralex.git
cd ralex
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENROUTER_API_KEY="your-key-here"
```

### Test It
```bash
python ralex_bridge.py "create a hello world script"
```

### Use Voice Interface
```bash
python start_ralex_v4.py
# Open http://localhost:3000
# Click microphone, say your command
```

## Example Commands

### File Creation
- "Create a Python calculator with add, subtract, multiply, divide"
- "Make a web scraper that gets headlines from news sites"  
- "Build a simple Flask web app with a home page"

### Code Editing
- "Add error handling to my calculator script"
- "Refactor this function to be more readable"
- "Add unit tests for my main.py file"

### Project Management
- "Explain what this codebase does"
- "Find all the TODO comments in my project"
- "Create a README file for this project"

## How It Works

```
Your Voice Command
      ↓
AgentOS Strategic Analysis
      ↓  
LiteLLM Model Selection
      ↓
OpenRouter API Call
      ↓
AI Generates Solution
      ↓
OpenCode Executes Code
      ↓
Results Saved to .ralex/
      ↓
Auto-commit to Git
```

### Smart Cost Management
- Simple tasks → Cheap models (llama, mistral)
- Complex coding → Mid-tier models (claude haiku)  
- Critical work → Premium models (claude sonnet)
- Most users spend <$5/month vs $20+ for ChatGPT Plus

### Session Memory
Every interaction is saved to `.ralex/session_TIMESTAMP.md`:
- Your original request
- How AgentOS analyzed it
- Which model was selected
- The complete AI response
- What files were created/modified

Access your coding history from any device via git sync.

## What Makes This Different

### vs ChatGPT/Claude Web Interfaces
- ✅ Actually creates files (no copy/paste)
- ✅ Voice control built-in
- ✅ 10x cheaper for most tasks
- ✅ Persistent session history
- ✅ Strategic thinking before acting

### vs GitHub Copilot
- ✅ Complete project understanding
- ✅ Voice commands
- ✅ Multiple AI models
- ✅ Full file operations
- ✅ Cross-session memory

### vs Cursor/Windsurf
- ✅ Open source
- ✅ Voice-first design  
- ✅ Strategic decision making
- ✅ Cost optimization
- ✅ Mobile-friendly

## Architecture Philosophy

### "Orchestrate, Don't Build"
Instead of rebuilding AI tools, Ralex connects existing best-in-class tools:

- **AgentOS**: Forces strategic thinking
- **LiteLLM**: Handles model complexity  
- **OpenRouter**: Provides AI access
- **OpenCode**: Manages code execution
- **OpenWebUI**: Delivers voice interface

### Thin Integration Layer
The entire Ralex V4 codebase is ~300 lines of orchestration code. We don't reinvent wheels, we connect them.

## Getting Started

1. **Read the [QUICKSTART.md](QUICKSTART.md)** - Complete beginner guide
2. **Try simple commands** - Start with file creation
3. **Use voice interface** - Experience hands-free coding
4. **Explore session logs** - Learn from your coding history
5. **Customize models** - Adjust cost/quality preferences

## Support

- **Quick Help**: Check [QUICKSTART.md](QUICKSTART.md)
- **Setup Issues**: See [RALEX_V4_SETUP.md](RALEX_V4_SETUP.md)  
- **Bug Reports**: [GitHub Issues](https://github.com/Khamel83/ralex/issues)
- **Architecture**: [docs/V4_ARCHITECTURE.md](docs/V4_ARCHITECTURE.md)

## The Vision

Voice-controlled development where you describe what you want and AI builds it. No more context switching, copy/pasting, or losing your train of thought. Just natural conversation that produces working code.

**Ready to start voice-coding?**

```bash
python ralex_bridge.py "create something amazing"
```