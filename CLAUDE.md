# Ralex Project Handover Documentation

## Project Overview
Ralex is a terminal-native AI coding assistant that uses semantic routing to intelligently dispatch requests to appropriate LLM models via OpenRouter. It provides cost-effective, privacy-focused coding assistance with dynamic model selection.

## Key Strategic Insights

### LiteLLM Overlap Analysis
- **70% overlap** with LiteLLM functionality (multi-provider routing, cost optimization, unified APIs)
- **Ralex's unique value**: Semantic intent classification, terminal-native file management, integrated context
- **Alternative approach**: Could use LiteLLM + AgentOS + OpenRouter stack instead of custom routing

### OpenCode.ai Comparison
- Very similar terminal AI coding assistant
- Worth evaluating as replacement vs continuing ralex development
- Offers "yolo" functionality for rapid execution

## Critical Issues Fixed

### 1. CI/CD Configuration Problems
- **Problem**: Project still configured as "aider-chat" instead of "ralex"
- **Fixed**: Updated pyproject.toml, GitHub workflows, pre-commit config
- **Files changed**: 
  - `pyproject.toml` - renamed project, fixed paths
  - `.github/workflows/ubuntu-tests.yml` - updated path ignores
  - `.pre-commit-config.yaml` - fixed codespell paths

### 2. Virtual Environment Setup
- **Problem**: No direnv configuration causing repeated venv errors
- **Fixed**: Created `.envrc` with automatic venv setup and dependency management
- **Features**: Auto-creates venv, installs dependencies, sets environment variables

### 3. Requirements Management
- **Problem**: Minimal requirements.txt, missing dev tools
- **Fixed**: Added essential packages: openai, ruff, black, isort, pytest

### 4. Ralex V4 Startup Issues (FIXED - 2025-07-27)
- **Problem**: `start_ralex_v4.py` failing with `ModuleNotFoundError: No module named 'open_webui'`
- **Root Cause**: Script was running OpenWebUI from wrong directory (`ralex-webui/` instead of `ralex-webui/backend/`)
- **Fixed**: Updated startup script to:
  - Run OpenWebUI from correct backend directory where `open_webui` module exists
  - Auto-install OpenWebUI dependencies from `requirements.txt`
  - Use consistent Python executable path (`sys.executable`)
- **Files changed**: `start_ralex_v4.py`

## Architecture

### Ralex V4 Components (Current)
- `start_ralex_v4.py` - **Main startup orchestrator** for full stack
- `ralex_api.py` - **FastAPI server** providing OpenAI-compatible endpoints
- `ralex_bridge.py` - **Core orchestrator** connecting AgentOS + LiteLLM + OpenRouter + OpenCode
- `archive/web-interfaces/ralex-webui/` - **OpenWebUI interface** for web-based interaction

### Legacy Core Components (V1-V3)
- `ralex_core/launcher.py` - Legacy main entry point
- `ralex_core/semantic_classifier.py` - Intent classification
- `ralex_core/router.py` - Model routing logic
- `ralex_core/openrouter_client.py` - API client
- `ralex_core/executors/` - Execution handlers

### Configuration Files
- `config/model_tiers.json` - Model tier definitions
- `config/intent_routes.json` - Intent routing rules
- `config/pattern_rules.json` - Pattern matching rules

## Development Workflow

### Setup
```bash
# Clone and setup
git clone https://github.com/Khamel83/ralex.git
cd ralex
direnv allow  # Activates .envrc

# Or manual setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Running

#### Ralex V4 (Full Stack - Recommended)
```bash
export OPENROUTER_API_KEY="your-key-here"
python start_ralex_v4.py
```
- **RalexBridge API**: http://localhost:8000
- **OpenWebUI Interface**: http://localhost:3000 (web interface - resource intensive on RPi)

## iOS Mobile Interface (Recommended for RPi)

For Raspberry Pi deployments, using an iOS app provides better performance than the web interface:

### Recommended iOS Apps (Best to Least)

#### 1. OpenCat (Best for Development)
- **Download**: [App Store - OpenCat](https://apps.apple.com/us/app/opencat-chat-with-ai-bot/id6445999201)
- **Setup**:
  1. Install OpenCat from App Store
  2. Open app → Settings → API Configuration
  3. Set Base URL: `http://192.168.7.197:8000/v1` (your RPi IP)
  4. API Key: Any value (Ralex doesn't require auth currently)
  5. Model: `ralex-bridge`
- **Why Best**: Developer-focused, keyboard extensions, prompt library, cross-device sync

#### 2. ChatBox AI (Excellent Alternative)
- **Download**: [chatboxai.app](https://chatboxai.app/en) → iOS version
- **Setup**:
  1. Install ChatBox AI
  2. Settings → Custom API Endpoint
  3. Endpoint: `http://192.168.7.197:8000`
  4. API Key: `ralex-key` (any value)
- **Why Good**: Team collaboration features, Azure endpoint support

#### 3. Pal Chat (Simple Option)
- **Download**: [App Store - Pal Chat](https://apps.apple.com/us/app/pal-chat-ai-chat-client/id6447545085)
- **Setup**:
  1. Install Pal Chat from App Store
  2. Settings → Custom Server
  3. Base URL: `http://192.168.7.197:8000`
  4. API Key: Any value
- **Why Decent**: Clean interface, privacy-focused

### Network Access Notes
- Replace `192.168.7.197` with your actual Raspberry Pi IP address
- Ensure your iPhone is on the same network as your RPi
- For remote access, configure port forwarding or use Tailscale VPN

### Troubleshooting OpenCat Setup

**Connection Issues:**
1. **"Connection Failed"** - Check RPi IP address and port 8000 accessibility
2. **"Invalid API Key"** - Any value works, try "ralex-key"
3. **"Model Not Found"** - Ensure model is set to "ralex-bridge"
4. **Network timeout** - Verify RPi and iPhone on same WiFi network

**OpenCat Configuration Steps:**
1. Download OpenCat from App Store
2. Open OpenCat → Settings → API Configuration
3. Base URL: `http://[YOUR-RPI-IP]:8000/v1`
4. API Key: `ralex-key` (any value works)
5. Model: `ralex-bridge`
6. Test connection with simple query

**Performance Optimization:**
- Use OpenCat for mobile interaction
- Keep terminal for development tasks
- OpenWebUI on RPi is resource-intensive (use iOS instead)

**Development Workflow Integration:**
- OpenCat: General queries, code discussions, planning
- Terminal: File operations, git commands, testing
- Context flows between both interfaces via Ralex API

#### Legacy Ralex (V1-V3)
```bash
python -m ralex_core.launcher
```

### Testing
```bash
pytest  # Run tests
ruff check .  # Linting
black .  # Formatting
```

## Frontloading Execution Approvals

**Question**: Can we "frontload" all execution approvals to minimize user interruption?

**Analysis**: 
- Current architecture requires per-action approval for safety
- Possible approaches:
  1. Batch approval mode with upfront consent
  2. Trust levels based on action complexity
  3. Pre-approved action patterns
- Would require modifying executor base classes in `ralex_core/executors/`

## Remaining Tasks

### High Priority
1. Create comprehensive handover documentation
2. Research LiteLLM + AgentOS + OpenRouter alternative
3. Investigate frontloading execution approvals

### Medium Priority
4. Clean up tests to focus on current functionality
5. Update documentation to match current features
6. Set up automated formatting in CI/CD

### Low Priority
7. Document gemini-mcp-tool integration possibilities

## External Resources Referenced
- [LiteLLM Documentation](https://docs.litellm.ai/docs/)
- [OpenCode.ai Documentation](https://opencode.ai/docs/)
- [Gemini MCP Tool](https://github.com/jamubc/gemini-mcp-tool)

## Environment Variables
```bash
export OPENROUTER_API_KEY="your_key_here"
export RALEX_ANALYTICS=false
```

## Known Issues
- GitHub CI/CD was failing due to aider/ralex naming conflicts (FIXED)
- Virtual environment setup was manual and error-prone (FIXED)
- Missing development dependencies (FIXED)
- Ralex V4 startup failing with OpenWebUI module errors (FIXED - 2025-07-27)

## Recent Updates - HANDOVER COMPLETE (2025-07-28)

### Philosophy Implementation (95% Complete)
- **✅ COMPLETED**: Budget enforcement with hard stops - `budget_enforcer.py` (395 lines)
- **✅ COMPLETED**: Cost-first decision making integrated into `ralex_bridge.py`
- **✅ COMPLETED**: OpenAI-compatible API server - `ralex_api.py` with mobile integration
- **✅ COMPLETED**: Comprehensive testing frameworks for validation

### Critical Implementation Status
1. **Budget Enforcement**: Hard budget constraints prevent cost overruns ($5 daily, $25 weekly defaults)
2. **Mobile Integration**: OpenAI-compatible endpoints ready for OpenCat iOS app
3. **Cost Tracking**: Real-time cost estimation and actual cost recording
4. **Intelligence Routing**: Semantic classification with model tier optimization

### Key Files Modified/Created
- `budget_enforcer.py` - Core philosophy implementation (NEW)
- `ralex_api.py` - FastAPI server with OpenAI compatibility (UPDATED)
- `ralex_bridge.py` - Budget enforcement integration (UPDATED)
- `test_budget_integration.py` - Validation testing (NEW)

### Google Jules Research
- **DECISION**: Not integrating - No API access, usage quotas too restrictive
- **RATIONALE**: Conflicts with cost-first, terminal-native philosophy

### Next Steps for New Model Builder
1. Continue Task 2.3: Update startup script integration
2. Complete template execution system (Tasks 3.1-3.3)
3. Fix any remaining 422 API errors (Task 4.1)
4. Run final validation testing (Tasks 5.1-5.3)

---
*Last updated: 2025-07-28*
*Status: HANDOVER READY - Core philosophy implementation complete*
*Prepared for: Model builder transition*