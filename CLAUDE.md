# Ralex Project Documentation - Agent-OS Optimized

## Project Overview
Ralex is a terminal-native AI coding assistant that uses semantic routing to intelligently dispatch requests to appropriate LLM models via OpenRouter. It provides cost-effective, privacy-focused coding assistance with dynamic model selection.

**Enhanced with Agent-OS**: This project now uses Agent-OS for intelligent cost optimization and development workflow management, achieving **$50 worth of results for $1** using smart model routing.

## 💰 Cost Optimization Strategy (Agent-OS Enhanced)
**Goal: Achieve $50 worth of results for $1 using smart model routing**

### Model Usage Pattern
1. **Planning Phase**: Use expensive models (Claude 3.5 Sonnet) for:
   - Architecture decisions
   - High-level problem solving
   - Complex reasoning tasks
   - Ralex component design

2. **Implementation Phase**: Use cheap models (Llama 3.1 8B) for:
   - Code generation from detailed specs
   - Repetitive tasks
   - Simple modifications
   - Ralex feature implementation

3. **Review Phase**: Use medium models (Claude Haiku) for:
   - Code review and debugging
   - Integration testing
   - Performance optimization
   - Ralex system validation

### Task Breakdown Approach
- Break complex Ralex development into micro-tasks
- Use cached solutions when possible
- Leverage Agent-OS templates and patterns
- Minimize expensive model usage

## Agent-OS Integration
- **Standards**: Follow `.agent-os/standards/` for coding practices
- **Workflows**: Use `.agent-os/workflows/` for development processes
- **Cost Templates**: Reference `.khamel83/cost-optimization/` for efficient task breakdown

## LiteLLM Routing
This project uses LiteLLM for intelligent model routing. Configuration in `.khamel83/model-routing/litellm-config.yaml`.

## Context Management
- Relevant files are in `.agent-os/` and `.khamel83/`
- Cache successful patterns in `.khamel83/cache/`
- Document cost savings in session logs

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

### Current Development Status (2025-08-03)
*   **B05: Codebase Refactoring Initiative:** **✅ COMPLETED.** Successfully removed all V4 references from codebase. All core modules import correctly, 39 tests passing, and JSON configuration files fixed. The systematic approach resolved the complex string replacement issues that were previously blocking this refactoring.

### Previously Fixed Issues
- CI/CD Configuration Problems (FIXED)
- Virtual Environment Setup (FIXED)
- Missing development dependencies (FIXED)
- Ralex V4 Startup Issues (FIXED - 2025-07-27)
- B05 Codebase Refactoring Initiative (FIXED - 2025-08-03)

## Recent Updates
- **2025-08-03**: Enhanced with Agent-OS cost optimization strategies
- **2025-07-27**: Fixed Ralex V4 startup script to properly run OpenWebUI from backend directory
- **2025-07-27**: Updated documentation to reflect current V4 architecture vs legacy components

---
*Last updated: 2025-08-03*
*Enhanced with Agent-OS cost optimization - Achieving $50 worth of results for $1*
*Prepared for: Cost-optimized LLM development and team collaboration*

Remember: The goal is maximum value with minimum cost through intelligent task decomposition and model routing.
