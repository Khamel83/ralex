# Ralex

Terminal-native AI coding assistant with semantic routing and cost-optimized model selection via OpenRouter.

**Current Version:** 1.3.0  
**Development Standards:** Modern continuous deployment (see `.agent-os/standards/`)  
**Primary Interface:** OpenCat iOS app (mobile) + terminal (development)

## Quick Start

### Single Command Setup
```bash
@execute-task ralex-mobile-intelligence-complete
```
*Executes complete OpenCat integration + intelligence optimization (120-150 minutes)*

### Manual Setup
```bash
git clone https://github.com/Khamel83/ralex.git
cd ralex
export OPENROUTER_API_KEY="your-key-here"
python start_ralex_v4.py
```

## Architecture

**Current Components:**
- `ralex_api.py` - OpenAI-compatible API server
- `ralex_bridge.py` - Core orchestrator (AgentOS + LiteLLM + OpenRouter)
- `start_ralex_v4.py` - Main startup orchestrator
- `.agent-os/` - Modern development standards and automation

**Endpoints:**
- RalexBridge API: http://localhost:8000
- OpenWebUI Interface: http://localhost:3000 (RPi: use iOS app instead)

## Mobile Interface (Primary)

**OpenCat iOS App** - Primary mobile interface for Ralex
- Download: [App Store - OpenCat](https://apps.apple.com/us/app/opencat-chat-with-ai-bot/id6445999201)
- Configuration: Base URL = `http://[your-rpi-ip]:8000/v1`, Model = `ralex-bridge`
- Features: Native iOS interface, cost-optimized routing, development workflows

## Intelligence Optimization

**Cost-First Model Routing:**
- Simple queries → Direct to cheap models
- Complex tasks → Agent-OS workflows with tier optimization
- Context tracking (3-5 tokens)
- Cost logging to `.ralex/cost_log.txt`

**Enable:** `export INTELLIGENCE_ENABLED=true`

## Development Standards

**Modern Workflow:**
- Semantic versioning (1.2.3 format)
- Feature branches merge when ready (1hr-3weeks)
- Main branch always production-ready
- Conventional commits (`feat:`, `fix:`, `docs:`)
- No marketing language - facts and metrics only

**Standards Location:** `.agent-os/standards/modern-development.yaml`

## Files

**Key Configuration:**
- `.ralex/intelligence-config.yaml` - Cost optimization settings
- `CLAUDE.md` - Complete project documentation
- `.agent-os/task-specs/` - Automated workflow specifications

**Legacy Components:**
- `ralex_core/` - V1-V3 components (deprecated)
- `archive/web-interfaces/ralex-webui/` - Web interface (RPi: use iOS instead)

---

**Documentation Standards Reference:** All documentation follows factual, anti-marketing philosophy per `.agent-os/standards/modern-development.yaml`