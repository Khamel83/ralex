# RalexOS - Y-Router Edition

## 🎉 Claude Code + 10 OpenRouter Models + 22 MCP Servers = Complete AI Dev Environment

**What you get:** Use Claude Code with 10 different AI models through OpenRouter, plus access to 22 specialized MCP servers, all without needing an Anthropic API key.

**V1 COMPLETE**: Fully working Y-Router + OpenRouter integration with seamless model switching and comprehensive MCP ecosystem.

## Why Y-Router?

Y-Router lets you use Claude Code (the official Anthropic CLI) with **any OpenRouter model** while keeping your existing Claude Code Pro subscription intact. You get:

- **10 AI models** - GPT-5 Nano, Kimi K2, Qwen3 Coder, Gemini Flash, and more
- **Seamless switching** - `/model kimi-k2` switches models mid-conversation  
- **Cost control** - Start cheap with nano, scale up for complex tasks
- **Full tool calling** - All models support Claude Code's tool ecosystem
- **22 MCP servers** - Complete development environment ready to go

## V1 Features ✅

**10-Model OpenRouter Integration:**
- GPT-5 Nano (fast/cheap), Kimi K2 (reasoning), Qwen3 Coder (specialist)
- Gemini 2.5/2.0 Flash, GPT-4o Mini, Claude 3.5 Sonnet, and more
- Seamless model switching: `/model kimi-k2`, `/model qwen3-coder`

**22 MCP Servers Working:**
- filesystem, memory-bank, sequential-thinking, github-integration
- playwright-testing, sentry-monitoring, k83-framework, mcp-orchestrator
- And 14 more specialized servers for complete development ecosystem

**Cost-Effective Workflow:**
- Start with `claude-cheap` (GPT-5 Nano) for basic tasks
- Scale up to specialized models as needed
- Manual control = perfect cost optimization

**Production Ready:**
- Y-router Docker integration
- Secure API key management (.env)
- OpenRouter requests branded as "Ralex"

## 🚀 Quick Start - Get Running in 3 Steps

### 1. Get an OpenRouter API Key (Free)
- Sign up at [OpenRouter.ai](https://openrouter.ai) (free account)
- Get your API key from the dashboard
- Add it to your environment:
```bash
echo "OPENROUTER_API_KEY=your-key-here" > .env
```

### 2. Run the Setup Script
```bash
git clone https://github.com/Khamel83/ralex.git
cd ralex
./setup-y-router.sh
source ~/.bashrc
```

### 3. Start Using Claude Code with 10 Models
```bash
# Entry points - pick your model:
claude-cheap "What's 2+2?"                    # GPT-5 Nano (super fast/cheap)
claude-kimi "Explain quantum computing"       # Kimi K2 (reasoning expert) 
claude-qwen3 "Write a Python function"        # Qwen3 Coder (coding specialist)
claude-flash "Help me debug this code"        # Gemini Flash (fast, good quality)

# Switch models mid-conversation:
/model moonshotai/kimi-k2                      # Switch to reasoning expert
/model qwen/qwen3-coder                        # Switch to coding specialist
/model google/gemini-2.5-flash                # Switch to fast general model
```

### 4. Access 22 MCP Servers (Automatically Available)
All your existing MCP tools work with any model:
- **Filesystem** - File operations and navigation
- **GitHub** - Repository management and workflows  
- **Playwright** - Web automation and testing
- **Memory Bank** - Persistent memory across sessions
- **Sequential Thinking** - Step-by-step problem solving
- And 17 more specialized development tools

## 💡 Why This is Awesome

**For Claude Code Users:**
- Keep your Pro subscription for normal use
- Add 10 specialized models for specific tasks  
- No configuration conflicts - they coexist perfectly

**For Developers:**
- **Cost optimization** - Use nano for simple tasks, scale up as needed
- **Specialization** - Right model for the right job (coding, reasoning, general)
- **Full ecosystem** - All MCP tools work with any model
- **Future-proof** - Easy to add new models as they become available

**For Teams:**
- **Shared setup** - One script works for everyone
- **Consistent environment** - Same tools and models across the team
- **Easy onboarding** - Clone, run script, start coding

## 🎯 Available Models

| Command | Model | Best For | Cost |
|---------|-------|----------|------|
| `claude-cheap` | GPT-5 Nano | Quick tasks, testing | Ultra low |
| `claude-kimi` | Kimi K2 (1T params) | Complex reasoning, agentic work | Low |
| `claude-qwen3` | Qwen3 Coder | Code generation, debugging | Low |
| `claude-flash` | Gemini 2.5 Flash | Fast general tasks | Low |
| `claude-gpt4` | GPT-4o Mini | Reliable, well-tested | Medium |
| `claude-gemini2` | Gemini 2.0 Flash | Latest Google model | Low |
| Plus 4 more... | Various specialists | Specific use cases | Varies |

## 📚 Usage Examples

**Smart Cost Optimization:**
```bash
# Start cheap for planning
claude-cheap "Help me plan a web scraping project"

# Switch to specialist for implementation  
/model qwen/qwen3-coder

# Switch to reasoning expert for complex logic
/model moonshotai/kimi-k2
```

**MCP Integration:**
```bash
# Use filesystem tools with any model
claude-flash "List all Python files and find the main entry point"

# GitHub integration with reasoning model
claude-kimi "Analyze the recent commits and suggest improvements"
```

## 📖 Documentation

- **[V1_COMPLETE.md](V1_COMPLETE.md)** - Complete feature overview and what's working
- **[claude.md](claude.md)** - Technical details and future roadmap (V2/V3/V4 ideas)
- **[CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md)** - Detailed setup guide and troubleshooting

## 🤝 Contributing

This project is actively developed and we welcome contributions! 

**Current Status:** V1 Complete (production ready)  
**Next:** V2-V4 roadmap with 390 atomic tasks ready for execution via Agent-OS integration

## 🎯 V2-V4 Roadmap: Intelligent AI Development Environment

**V2: Smart Model Routing** - Automatic task-to-model optimization with cost control
**V3: Agent-OS Integration** - Project-aware autonomous development with pattern learning  
**V4: Enterprise Features** - Multi-agent orchestration, team collaboration, and advanced security

### Ready to Execute: 390 Atomic Tasks
All implementation tasks have been broken down into atomic, executable components following Agent-OS methodology. See `.agent-os/instructions/execute-tasks.md` for the complete 390-task roadmap from V1 to V4 completion.

## 🛡️ Fixed Issues

**GitHub Actions Errors Resolved** ✅
- Disabled outdated CI/CD workflows that expected Python package structure
- Added appropriate V1 tests for bash/docker setup
- No more failed workflow runs!

## 📊 What Makes This Special

This isn't just another AI wrapper - it's a complete integration that:

1. **Actually works** - Tested and confirmed working setup
2. **Preserves your existing setup** - Keep Claude Code Pro unchanged
3. **Gives you choice** - 10 models for different needs
4. **Scales with you** - Start simple, add complexity as needed
5. **Complete ecosystem** - 22 MCP servers for any development task

## 🚀 Ready to Get Started?

```bash
git clone https://github.com/Khamel83/ralex.git
cd ralex
echo "OPENROUTER_API_KEY=your-key-here" > .env
./setup-y-router.sh
source ~/.bashrc
claude-cheap "Hello world!"
```

**That's it!** You now have Claude Code + 10 models + 22 MCP servers ready to go.

---

**Built for developers who want choice, control, and a complete AI development environment** 🎯
