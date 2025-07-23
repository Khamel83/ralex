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

## Architecture

### Core Components
- `ralex_core/launcher.py` - Main entry point
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

---
*Last updated: 2025-07-23*
*Prepared for: LLM handover and team collaboration*