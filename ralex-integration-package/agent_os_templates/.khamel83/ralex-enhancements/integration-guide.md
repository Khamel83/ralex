# Ralex Integration Guide

This guide explains how to integrate Agent-OS cost optimization with Ralex's intelligent model routing.

## Overview
Agent-OS provides the "intelligence layer" for cost optimization, while Ralex handles the actual model routing and execution via LiteLLM.

## Integration Points

### 1. Task Analysis
Agent-OS analyzes task complexity and determines routing strategy:
```
Complex Task → Planning Phase (Expensive Model)
Simple Task → Direct Implementation (Cheap Model)
Debug Task → Review Phase (Medium Model)
```

### 2. Model Selection
Ralex uses LiteLLM for actual model routing based on Agent-OS recommendations:
- Planning: `openrouter/anthropic/claude-3.5-sonnet`
- Implementation: `openrouter/meta-llama/llama-3.1-8b-instruct`
- Review: `openrouter/anthropic/claude-3-haiku`

### 3. Context Management
Agent-OS standards and patterns inform Ralex's context window optimization:
- Cache successful patterns in `.khamel83/cache/`
- Reuse solutions for similar tasks
- Minimize context size for cheap models

## Workflow Integration

### Phase 1: Planning (Agent-OS + Expensive Model)
1. Agent-OS analyzes task complexity
2. Creates detailed breakdown and specifications
3. Ralex routes to planning model (Claude 3.5 Sonnet)
4. Saves architectural decisions and patterns

### Phase 2: Implementation (Agent-OS + Cheap Models)
1. Agent-OS breaks down into micro-tasks
2. Each micro-task routed to implementation model (Llama 3.1 8B)
3. Ralex executes tasks with minimal context
4. Results cached for future reuse

### Phase 3: Review (Agent-OS + Medium Model)
1. Agent-OS validates implementation against specifications
2. Ralex routes debugging/testing to review model (Claude Haiku)
3. Escalates complex issues back to planning model if needed

## Configuration Files

### Ralex Configuration
Update your `ralex_bridge.py` to read Agent-OS cost optimization settings:

```python
def apply_agentos_thinking(self, prompt: str) -> dict:
    """Enhanced with .khamel83 cost optimization"""
    cost_config = self.load_cost_config()
    
    thinking = {
        "original_prompt": prompt,
        "complexity": self.analyze_complexity(prompt, cost_config),
        "cost_strategy": self.determine_strategy(prompt, cost_config),
        "cached_solution": self.check_cache(prompt)
    }
    return thinking

def load_cost_config(self):
    """Load .khamel83 cost optimization settings"""
    config_path = Path(".khamel83/model-routing/litellm-config.yaml")
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {}
```

### LiteLLM Configuration
Place the Agent-OS LiteLLM config as your project's main routing configuration:

```bash
cp .khamel83/model-routing/litellm-config.yaml ./litellm_config.yaml
```

## Cost Tracking Integration

### Ralex Session Logs
Enhanced session logs with cost tracking:

```markdown
# Ralex Session with Agent-OS Cost Optimization

## Original Task
[User request]

## Agent-OS Analysis
- Complexity: [high/medium/low]
- Strategy: [planning/implementation/review]
- Estimated Traditional Cost: $[amount]

## Execution Log
- Planning Phase: $[amount] ([model])
- Implementation Tasks: $[amount] ([model])
- Review Phase: $[amount] ([model])

## Results
- Total Cost: $[amount]
- Estimated Savings: $[amount] ([percentage]%)
- Patterns Cached: [list]
```

## Performance Optimization

### Context Window Management
- **Planning Phase**: Full context, detailed specifications
- **Implementation Phase**: Minimal context, specific task focus
- **Review Phase**: Targeted context, error-specific information

### Pattern Caching
Successful solutions automatically cached in `.khamel83/cache/`:
- Common code patterns
- Architectural decisions
- Debugging solutions
- Configuration templates

### Batch Processing
Group similar micro-tasks for efficient processing:
- Multiple file creations
- Repetitive code modifications
- Similar API endpoints
- Database operations

## Monitoring and Analytics

### Cost Dashboard
Track your savings over time:
- Daily/weekly/monthly cost summaries
- Savings percentage trends
- Most effective optimization strategies
- Pattern reuse frequency

### Performance Metrics
- Average task completion time
- Model accuracy by phase
- Context efficiency ratios
- Cache hit rates

This integration transforms Ralex from a simple model router into an intelligent cost optimization system powered by Agent-OS methodology.