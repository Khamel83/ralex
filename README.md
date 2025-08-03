# Ralex

Terminal-native AI coding assistant with semantic routing and cost-optimized model selection via OpenRouter.

**Current Version:** 1.3.0  
**Development Standards:** Agent-OS enhanced (see `agent_os/standards/`)  
**Primary Interface:** OpenCat iOS app (mobile) + OpenWebUI (web) + terminal (CLI)

## 💰 Cost Optimization

**Goal: $50 worth of results for $1 using intelligent model routing**

- 🧠 **Planning**: Expensive models (Claude 3.5 Sonnet) for architecture decisions
- ⚡ **Implementation**: Cheap models (Llama 3.1 8B) for code generation  
- 🔍 **Review**: Medium models (Claude Haiku) for debugging/QA
- 💾 **Caching**: Reuse successful patterns

## 🚀 Quick Start

### Prerequisites
- Python 3.10-3.12
- OpenRouter API key (free at https://openrouter.ai/)

### Installation
```bash
git clone https://github.com/Khamel83/ralex.git
cd ralex
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### Running Ralex V4 (Full Stack)
```bash
export OPENROUTER_API_KEY="your-key-here"
python start_ralex.py
```

**Access Points:**
- **API Server**: http://localhost:8000
- **Web Interface**: http://localhost:3000
- **Health Check**: http://localhost:8000/health

### Legacy CLI Mode
```bash
python -m ralex_core.launcher
```

## 📱 Mobile Interface (Recommended for RPi)

For Raspberry Pi deployments, iOS apps provide better performance than the web interface:

### 1. OpenCat (Best for Development)
- **Download**: [App Store - OpenCat](https://apps.apple.com/us/app/opencat-chat-with-ai-bot/id6445999201)
- **Setup**:
  - Base URL: `http://[your-rpi-ip]:8000/v1`
  - API Key: `ralex-key` (any value)
  - Model: `ralex-bridge`

### 2. ChatBox AI (Team Collaboration)
- **Download**: [chatboxai.app](https://chatboxai.app/en) → iOS version
- **Setup**:
  - Endpoint: `http://[your-rpi-ip]:8000`
  - API Key: `ralex-key`

### 3. Pal Chat (Simple & Clean)
- **Download**: [App Store - Pal Chat](https://apps.apple.com/us/app/pal-chat-ai-chat-client/id6447545085)
- **Setup**:
  - Base URL: `http://[your-rpi-ip]:8000`
  - API Key: any value

*Note: Replace `[your-rpi-ip]` with your device's actual IP address*

## 🏗️ Architecture

### Core Components
- **`start_ralex.py`** - Main V4 startup orchestrator
- **`ralex_bridge.py`** - Core orchestrator (AgentOS + LiteLLM + OpenRouter)
- **`ralex_api.py`** - OpenAI-compatible API server
- **`ralex_core/`** - Core Python package with all modules
- **`agent_os/`** - Development standards and workflow instructions

### Component Stack
```
┌─────────────────────────────────────────┐
│              User Interfaces           │
│  OpenCat (iOS) | OpenWebUI | Terminal  │
├─────────────────────────────────────────┤
│             API Layer                   │
│        RalexBridge (Port 8000)         │
├─────────────────────────────────────────┤
│           Core Services                 │
│ AgentOS | LiteLLM | OpenRouter | OpenCode │
├─────────────────────────────────────────┤
│         Model Providers                 │
│   OpenAI | Anthropic | Google | Local   │
└─────────────────────────────────────────┘
```

## 🧪 Testing

```bash
# Run test suite (39 passing tests)
pytest tests/ -v

# Run specific test categories
pytest tests/unit/ -v           # Unit tests
pytest tests/integration/ -v    # Integration tests (currently disabled)

# Code quality checks
ruff check .                   # Linting
black .                       # Formatting
```

## ⚙️ Configuration

### Environment Variables
```bash
export OPENROUTER_API_KEY="sk-or-..."  # Required
export RALEX_ANALYTICS=false           # Optional: Disable analytics  
export RALEX_BUDGET_LIMIT=5           # Optional: Daily budget in USD
export RALEX_DEBUG=true               # Optional: Enable debug logging
```

### Configuration Files
- `config/model_tiers.json` - Model pricing and routing tiers
- `config/intent_routes.json` - Intent → model mapping
- `config/settings.json` - System settings
- `agent_os/standards/` - Coding standards (Python, Git)
- `agent_os/instructions/` - Workflow instructions

## 📊 Performance Metrics

### Cost Efficiency
- **Target**: 50:1 cost optimization ratio
- **Typical usage**: $0.50-1.00/day (well under $5 budget)
- **Model distribution**: 70% cheap, 20% medium, 10% premium
- **Daily budget**: $5 limit with real-time monitoring

### System Performance
- **Response time**: <2s for simple queries, 5-10s for complex
- **Memory usage**: ~50MB baseline, scales with context
- **Test coverage**: 39 passing tests covering core functionality
- **System health**: 95% production readiness score

## 🔒 Security

### API Key Management
```bash
# Secure .env file permissions
chmod 600 .env

# Never commit API keys
echo "*.env" >> .gitignore
```

### Budget Security
- Daily spending limits enforced
- Real-time cost monitoring  
- Conservative cost estimates (50% safety buffer)
- Emergency fallback mechanisms

## 📚 Documentation

### User Documentation
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[COMPREHENSIVE_HANDOVER.md](COMPREHENSIVE_HANDOVER.md)** - Complete system overview
- **[USAGE.md](USAGE.md)** - Daily workflow examples

### Technical Documentation  
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical implementation details
- **[FRONTLOADING_EXECUTION_APPROVALS_INVESTIGATION.md](FRONTLOADING_EXECUTION_APPROVALS_INVESTIGATION.md)** - Batch approval implementation plan
- **[LITELLM_AGENTOS_ALTERNATIVES_RESEARCH.md](LITELLM_AGENTOS_ALTERNATIVES_RESEARCH.md)** - Alternative solutions analysis
- **[TEST_CLEANUP_SUMMARY.md](TEST_CLEANUP_SUMMARY.md)** - Test suite status and improvements

### Development Documentation
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guidelines
- **[SECURITY.md](SECURITY.md)** - Security considerations
- **[CLAUDE.md](CLAUDE.md)** - Project instructions for AI assistants

## 🛠️ Development

### Development Setup
```bash
# Full development environment
git clone https://github.com/Khamel83/ralex.git
cd ralex
python -m venv .venv-dev
source .venv-dev/bin/activate
pip install -r requirements.txt
pip install -e .

# Install development tools
pip install pytest black ruff mypy
```

### Code Standards
- **Python**: PEP 8, type hints, docstrings (see `agent_os/standards/python.md`)
- **Git**: Atomic commits, descriptive messages (see `agent_os/standards/git-workflow.md`)
- **Testing**: >80% coverage requirement
- **Documentation**: Comprehensive with examples

## 🚀 Deployment

### Production Checklist
- [ ] Set secure API key permissions (`chmod 600 .env`)
- [ ] Configure firewall for ports 8000 and 3000
- [ ] Set up HTTPS for remote access
- [ ] Enable logging and monitoring
- [ ] Configure automatic backups of context data
- [ ] Test mobile app connectivity
- [ ] Verify budget limits and alerts

### Raspberry Pi Optimization
- Use iOS mobile apps instead of web interface for better performance
- Configure Tailscale VPN for remote access
- Set up automatic startup on boot
- Monitor CPU and memory usage

## ❓ Troubleshooting

### Common Issues

**Connection Failed (Mobile Apps)**
1. Check device IP and port 8000 accessibility
2. Verify same WiFi network
3. Try "ralex-key" as API key

**Budget Exceeded**
1. Check current spending: `curl http://localhost:8000/budget/status`
2. Reset budget: `rm /tmp/ralex_litellm_budget.json`
3. Adjust daily limit in configuration

**Import Errors**
1. Activate virtual environment: `source .venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Install in development mode: `pip install -e .`

### Health Checks
```bash
# System health
curl http://localhost:8000/health

# Run test suite
pytest tests/ -v

# Check system logs
tail -f ralex_startup.log
```

## 📞 Support

- **Issues**: https://github.com/Khamel83/ralex/issues
- **Documentation**: See docs in this repository
- **Health Check**: `python archive/development-tools/validation/health_check.py`

## 📄 License

Apache License 2.0 - see LICENSE file for details.

---

**🚀 Ralex is production-ready and optimized for cost-effective AI development!**

*Last updated: 2025-08-03*