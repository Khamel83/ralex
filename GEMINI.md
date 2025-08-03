# Gemini CLI Configuration - Khamel83 Edition

## Project Overview
This project uses Agent-OS for intelligent cost optimization and development workflow management.

## Gemini CLI Integration
Use Gemini CLI for "vibe coding" and quick iterations alongside the cost-optimized Ralex system.

### Usage Patterns
- **Quick Exploration**: Use Gemini for rapid codebase exploration
- **Multimodal Tasks**: Leverage Gemini's image/document understanding
- **Iterative Development**: Fast feedback loops for development

### Agent-OS Integration
- **Standards**: Follow `.agent-os/standards/` for coding practices
- **Workflows**: Use `.agent-os/workflows/` for development processes
- **Context**: Reference project structure in `.agent-os/` and `.khamel83/`

### Cost Optimization
While Gemini CLI is used for exploration, refer to the main Ralex system (via Claude Code/Cursor) for cost-optimized production work:

1. **Explore with Gemini** - understand problems and possibilities
2. **Plan with Ralex** - create cost-effective implementation strategy  
3. **Implement efficiently** - use Agent-OS breakdown templates
4. **Review and iterate** - combine both tools as needed

### Workflow Integration
- Use Gemini CLI for initial exploration and understanding
- Switch to Ralex/LiteLLM routing for cost-effective implementation
- Return to Gemini for complex multimodal tasks when needed

### Context Files
- **Agent-OS Structure**: `.agent-os/` directory
- **Cost Optimization**: `.khamel83/cost-optimization/`
- **Cached Patterns**: `.khamel83/cache/`
- **Model Routing**: `.khamel83/model-routing/`

The goal is to use each tool for its strengths while maintaining cost efficiency through Agent-OS structure.

---

## Current Development Status (2025-08-03)

**Comprehensive Planning Complete:**
The entire project roadmap has been broken down into detailed, atomic workflow plans (B01-B07) located in `.agent-os/workflows/`.

**Progress on Implementation:**
*   **B01: Deprecate V5 MCP Documents:** **Completed.** Old V5 documents have been archived.
*   **B02: Hybrid Claude Code Router Integration:** **Completed.** `CCRManager` implemented, integrated into orchestrator, and CLI command added.
*   **B03: Agent-OS Ethos and Standards Implementation:** **Completed.** Dynamic port allocation, GitHub CLI dependency check, and flexible permissions model implemented.
*   **B05: Codebase Refactoring Initiative:** **In Progress / Paused.** File renames and most class name updates are complete. However, persistent issues with updating `ralex_core/launcher.py` due to complex string replacements have led to a decision to pause this specific refactoring for now. This will be revisited with a more robust strategy.

**Next Steps:**
The immediate next step is to commit all current changes and push them to GitHub. Further code modifications are paused until a new strategy for the `ralex_core/launcher.py` refactoring is determined.