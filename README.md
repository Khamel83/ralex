# Ralex V4: Voice-Driven AI Orchestration Platform

**🎙️ The world's most advanced voice-driven development environment - orchestrating OpenCode + LiteLLM + AgentOS + Context7 through natural speech.**

> **🚀 New to Ralex V4?** → Read [SETUP.md](SETUP.md) for 5-minute setup  
> **📱 Voice Interface** → See [USAGE.md](USAGE.md) for voice command patterns  
> **🏗️ Architecture** → Check [docs/V4_ARCHITECTURE.md](docs/V4_ARCHITECTURE.md)  
> **🗺️ Implementation Plan** → See [RALEX_V4_ROADMAP.md](RALEX_V4_ROADMAP.md)

## ✨ What Makes Ralex V4 Revolutionary

### 🎙️ **Complete Voice-Driven Development**
- **File operations** via OpenCode.ai integration - read, write, refactor any file
- **Shell commands** - git, testing, deployment through voice commands
- **Project-wide search** - intelligent code discovery and analysis
- **Automated workflows** - "Deploy this feature" executes entire pipelines

### 🔧 **Seamless Tool Orchestration**
| Component | Purpose | Integration |
|-----------|---------|-------------|
| **OpenCode.ai** | File operations, shell commands | CLI integration with safety controls |
| **LiteLLM** | Smart model routing, cost optimization | Multi-provider with budget management |
| **AgentOS** | Code standards, prompt enhancement | Context-aware standards application |
| **Context7** | Dynamic documentation, examples | MCP server for real-time docs |

### 🧠 **Persistent Context Intelligence**
- **Cross-session memory** stored in MD files, synced via GitHub
- **Project understanding** that grows with each interaction
- **Pattern learning** from your coding style and preferences  
- **Context compression** using AI to summarize old conversations

### 🌐 **Advanced Web Interface**
- **Voice-driven workflows** with automated multi-step processes
- **Mobile coding excellence** - full development from phone/tablet
- **Real-time collaboration** with shared context across devices
- **Intelligent automation** - predict and execute likely next steps

## 🚀 Quick Start

### 1. **Setup** (5 minutes)
```bash
# Get OpenRouter API key (free): https://openrouter.ai/
export OPENROUTER_API_KEY="your-key-here"

# Clone and install
git clone https://github.com/Khamel83/ralex.git
cd ralex
python3 -m pip install -r requirements.txt
npm install --prefix ralex-frontend
```

### 2. **Launch Ralex V3**
```bash
# Start both backend and web interface
./ralex-v3-launch.sh

# Access web interface at: http://localhost:3000
# API available at: http://localhost:8000
```

### 3. **Voice Orchestration Examples**
```
🎙️ "Fix the authentication bug in user_auth.py, execute"
🎙️ "Refactor the entire payment system, send it"
🎙️ "Deploy this feature to staging, go ahead"
🎙️ "Create user management with tests and documentation, do it"
```

## 💡 **How Ralex V4 Works**

### **Voice-to-Execution Orchestration**
1. **🎙️ Voice Input** → Open WebUI captures natural speech commands
2. **🧠 Context Loading** → Intelligent context from MD files + GitHub sync
3. **📋 AgentOS Enhancement** → Standards + documentation via Context7
4. **🎯 LiteLLM Routing** → Optimal model selection based on complexity  
5. **🔧 OpenCode Execution** → Actual file operations and shell commands
6. **📊 Context Update** → Learning and persistent memory storage
7. **🔄 Real-time Sync** → Cross-device updates via WebSocket + GitHub

### **V4 Orchestration Architecture**
```
🎙️ Voice → 📱 WebUI → 🧠 Orchestrator → 📝 Context → 📋 AgentOS → 🎯 LiteLLM → 🔧 OpenCode
     ↓         ↓          ↓              ↓          ↓           ↓           ↓
Speech API → WebSocket → Command Parser → MD Files → Context7 → Models → File Ops
```

## 📊 **Real Usage Costs**

- **Voice coding session**: $0.25-0.75/hour
- **Complex refactoring**: $1-2/day (well under budget)
- **Emergency fixes**: ~$0.01/task (instant response)
- **Daily development**: $0.50-1.50/day (10x cost reduction)

## 🎯 **Perfect For**

- **Mobile developers** who code on phones/tablets
- **Accessibility needs** requiring hands-free coding
- **Remote teams** needing real-time collaboration
- **Cost-conscious developers** wanting AI with budget control
- **Quality-focused teams** requiring consistent standards

## 🌟 **V3 Features**

### **Web Interface**
- 🎙️ **Voice input** with visual recording indicators
- 💰 **Real-time budget** tracking and management
- 📱 **Mobile responsive** design for coding anywhere
- 🔄 **WebSocket updates** for live collaboration
- 🎨 **Dark theme** optimized for coding

### **Smart Backend**
- 🧠 **Enhanced AgentOS** integration with web context
- 📡 **OpenAI-compatible API** for broad tool integration
- 💰 **Session budget** management with transaction history
- 🔍 **Intelligent routing** based on request complexity
- 📁 **File context** tracking across sessions

### **Developer Experience**
- 🚀 **One-command launch** for full stack
- 📊 **Real-time monitoring** of costs and usage
- 🔧 **Health checks** and system diagnostics
- 📝 **Comprehensive logging** for debugging
- 🎯 **Production ready** with Tailscale deployment

## 📚 **V4 Documentation**

- **[RALEX_V4_SPECIFICATION.md](RALEX_V4_SPECIFICATION.md)** - Complete V4 specification
- **[RALEX_V4_ROADMAP.md](RALEX_V4_ROADMAP.md)** - Phase-by-phase implementation plan
- **[docs/V4_ARCHITECTURE.md](docs/V4_ARCHITECTURE.md)** - Technical architecture details
- **[SETUP.md](SETUP.md)** - Installation and configuration guide
- **[USAGE.md](USAGE.md)** - Voice command patterns and workflows
- **[archive/](archive/)** - Historical V1-V3 files and documentation

## 🏆 **V4 Status: Specification Complete, Ready for Implementation**

- 📋 **Complete specification** with detailed architecture
- 🗺️ **Implementation roadmap** with 32-40 hour timeline
- 🧪 **Comprehensive testing strategy** for all components
- 🏗️ **Modular architecture** enabling incremental development
- 🔧 **Production deployment** plan with Tailscale + Docker
- 📚 **Complete documentation** for users and developers

**Next Step**: Begin Phase 1 implementation (Core Orchestration - 8-10 hours)

## 🎮 **Try It Now**

```bash
# Launch Ralex V3 in 30 seconds
git clone https://github.com/Khamel83/ralex.git
cd ralex
export OPENROUTER_API_KEY="your-key"
./ralex-v3-launch.sh

# Open http://localhost:3000 and start voice coding!
```

## 🌍 **The V4 Vision**

**Ralex V4** represents the ultimate evolution of AI-assisted development:
- **Complete voice-driven development** - from concept to deployment
- **Intelligent tool orchestration** - seamless integration of best-in-class tools
- **Persistent project intelligence** - context that grows with your codebase
- **Cross-device collaboration** - code anywhere, sync everywhere
- **Automated workflows** - voice commands that execute entire pipelines

## 🚀 **Ready to Build V4?**

1. **Review the specification** - [RALEX_V4_SPECIFICATION.md](RALEX_V4_SPECIFICATION.md)
2. **Check the roadmap** - [RALEX_V4_ROADMAP.md](RALEX_V4_ROADMAP.md)  
3. **Understand the architecture** - [docs/V4_ARCHITECTURE.md](docs/V4_ARCHITECTURE.md)
4. **Start Phase 1** - Core Orchestration (8-10 hours)

---

**The future of voice-driven development starts here. Let's build Ralex V4! 🎙️🚀**