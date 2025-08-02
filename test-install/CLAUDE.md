# Claude Code Configuration - Khamel83 Edition

## Project Overview
This project uses Agent-OS for intelligent cost optimization and development workflow management.

## Cost Optimization Strategy
**Goal: Achieve $50 worth of results for $1 using smart model routing**

### Model Usage Pattern
1. **Planning Phase**: Use expensive models (Claude 3.5 Sonnet) for:
   - Architecture decisions
   - High-level problem solving
   - Complex reasoning tasks

2. **Implementation Phase**: Use cheap models (Llama 3.1 8B) for:
   - Code generation from detailed specs
   - Repetitive tasks
   - Simple modifications

3. **Review Phase**: Use medium models (Claude Haiku) for:
   - Code review and debugging
   - Integration testing
   - Performance optimization

### Task Breakdown Approach
- Break complex requests into micro-tasks
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
1. **Analyze task complexity** - determine if planning phase needed
2. **Break down into micro-tasks** - use cost optimization templates
3. **Route to appropriate models** - let LiteLLM handle routing
4. **Cache successful patterns** - for future reuse
5. **Track cost savings** - measure efficiency gains

Remember: The goal is maximum value with minimum cost through intelligent task decomposition and model routing.
