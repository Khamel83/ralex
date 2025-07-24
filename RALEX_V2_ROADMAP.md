# Ralex V2: Minimal "Yolo Cost-Conscious Claude Code" Roadmap

## Vision
A dead-simple setup that gives you:
- 🚀 **Yolo mode**: Fast execution with minimal friction
- 💰 **Cost conscious**: Smart budgeting and cheap model routing  
- 🧠 **Claude Code integration**: Professional coding assistant experience
- 📋 **AgentOS orchestration**: Structured workflows and planning

## V2 Architecture: ULTRA SIMPLE

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   Claude Code   │───▶│   LiteLLM    │───▶│ OpenRouter  │
│   (Terminal UI) │    │   Proxy      │    │ (Models)    │
└─────────────────┘    └──────────────┘    └─────────────┘
         │
         ▼
┌─────────────────┐
│   AgentOS       │
│   (Standards &  │
│    Workflows)   │
└─────────────────┘
```

## What We're ELIMINATING from V1

### Entire Directories/Files to DELETE:
- `ralex_core/semantic_classifier.py` ❌
- `ralex_core/router.py` ❌  
- `ralex_core/hybrid_router.py` ❌
- `ralex_core/budget_optimizer.py` ❌
- `ralex_core/file_context.py` ❌
- `ralex_core/memory_manager.py` ❌
- `ralex_core/security_sandbox.py` ❌
- `ralex_core/executors/` ❌
- `config/` entire directory ❌
- `data/` entire directory ❌
- `tests/` (will recreate minimal ones) ❌
- `benchmark/` ❌
- Most of `aider-legacy/` ❌

### Lines of Code Reduction:
- **Current**: ~15,000+ lines across ralex_core
- **V2 Target**: ~100-200 lines total
- **Reduction**: 98%+ code elimination

## What We KEEP/NEED

### Option A: ZERO Custom Code (Recommended)
```bash
# Literally just configuration files:
- litellm_config.yaml    # LiteLLM routing config
- .envrc                 # Environment setup  
- package.json           # Dependencies
- README.md              # Instructions
```

### Option B: Minimal Custom Code (if needed)
```bash
ralex_v2/
├── launch.py           # 20 lines: starts LiteLLM proxy
├── budget_tracker.py   # 30 lines: simple cost logging
└── openrouter_config.py # 50 lines: OpenRouter-specific settings
```

## Detailed Implementation Plan

### Phase 1: Setup Core Stack (30 minutes)

#### 1.1 Install AgentOS
```bash
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup.sh | bash
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup-claude-code.sh | bash
```

#### 1.2 Install LiteLLM
```bash
pip install litellm[proxy]
```

#### 1.3 Test Basic Integration
```bash
# Start LiteLLM proxy with OpenRouter
litellm --model openrouter/anthropic/claude-3.5-sonnet --api_base https://openrouter.ai/api/v1

# Test in Claude Code
claude-code --model http://localhost:4000
```

### Phase 2: Configure Cost-Conscious Routing (1 hour)

#### 2.1 Create LiteLLM Config
```yaml
# litellm_config.yaml
model_list:
  - model_name: "cheap"
    litellm_params:
      model: "openrouter/google/gemini-flash-1.5"
      api_base: "https://openrouter.ai/api/v1"
  
  - model_name: "smart" 
    litellm_params:
      model: "openrouter/anthropic/claude-3.5-sonnet"
      api_base: "https://openrouter.ai/api/v1"

router_settings:
  routing_strategy: "cost-based"
  fallbacks:
    - ["cheap", "smart"]
  budget_manager:
    daily_limit: 10.00
```

#### 2.2 Cost Rules Configuration
```yaml
# cost_rules.yaml
routing_rules:
  - pattern: "simple|quick|small"
    model: "cheap"
    max_tokens: 1000
  
  - pattern: "complex|analyze|review"  
    model: "smart"
    max_tokens: 4000
    
  - pattern: "yolo|fast|now"
    model: "cheap"
    max_tokens: 500
    stream: true
```

### Phase 3: AgentOS Integration (30 minutes)

#### 3.1 Configure AgentOS Standards
AgentOS will create:
- `~/.agent-os/standards/tech-stack.md`
- `~/.agent-os/standards/code-style.md` 
- `~/.agent-os/instructions/execute-tasks.md`

#### 3.2 Claude Code Slash Commands
Available after setup:
- `/plan-product` - Create product roadmap
- `/create-spec` - Generate technical specifications
- `/execute-tasks` - Break down and execute development tasks
- `/analyze-product` - Review and analyze codebase

### Phase 4: Yolo Mode Setup (15 minutes)

#### 4.1 Create Yolo Launcher
```bash
#!/bin/bash
# yolo-ralex.sh
export LITELLM_LOG=DEBUG
export OPENROUTER_API_KEY="$OPENROUTER_API_KEY"

# Start LiteLLM with aggressive cost optimization
litellm --config litellm_config.yaml --port 4000 --num_workers 1 &

# Wait for startup
sleep 3

# Launch Claude Code with yolo settings
claude-code \
  --model http://localhost:4000 \
  --auto-commit \
  --yes-always \
  --fast-mode
```

### Phase 5: Testing & Validation (1 hour)

#### 5.1 Test Cost Optimization
```bash
# Test cheap routing for simple tasks
echo "Fix this typo" | claude-code --model http://localhost:4000

# Test smart routing for complex tasks  
echo "Refactor this entire class architecture" | claude-code --model http://localhost:4000
```

#### 5.2 Test AgentOS Integration
```bash
cd your-project/
claude-code /plan-product "Add user authentication"
claude-code /execute-tasks
```

#### 5.3 Validate Yolo Mode
```bash
./yolo-ralex.sh
# Should auto-execute with minimal prompts
```

## File Structure for V2

```
ralex-v2/
├── README.md                 # Setup instructions
├── litellm_config.yaml      # LiteLLM routing config
├── cost_rules.yaml          # Cost optimization rules
├── yolo-ralex.sh           # Quick launcher script
├── .envrc                   # Development environment
└── package.json             # Dependencies (optional)
```

## Benefits Analysis

### What You Get:
1. **Zero maintenance burden** - All logic handled by mature tools
2. **Professional grade** - LiteLLM used by thousands of companies
3. **Cost optimization** - Smart routing based on task complexity
4. **Yolo mode** - Fast execution with minimal friction
5. **Structured workflows** - AgentOS provides proven patterns
6. **Claude Code integration** - Best-in-class terminal experience

### What You Lose:
1. **Custom semantic classification** → Replaced by LiteLLM routing patterns
2. **Custom UI** → Replaced by Claude Code (better anyway)
3. **Custom executors** → Replaced by AgentOS + Claude Code
4. **Maintenance headaches** → Gone! 🎉

## Success Metrics

### Setup Time:
- **V1**: 2-3 hours with dependencies and debugging
- **V2**: 15-30 minutes total setup time

### Code Maintenance:
- **V1**: ~15,000 lines to maintain
- **V2**: ~50-100 lines of config files

### Cost Optimization:
- **V1**: Custom logic, potential bugs
- **V2**: Battle-tested LiteLLM routing

### Development Speed:
- **V1**: Custom debugging, feature development
- **V2**: Focus 100% on actual coding tasks

## Migration Steps

### Immediate (Today):
1. Test AgentOS + Claude Code setup
2. Configure basic LiteLLM proxy
3. Validate cost routing works

### This Week:
1. Create minimal V2 repository
2. Document setup process
3. Test yolo mode extensively

### Next Week:
1. Archive V1 as `ralex-legacy`
2. Publish V2 setup guide
3. Gather user feedback

## Decision Point

**Should we build V2?**

**YES - because:**
- 98% less code to maintain
- Professional-grade components
- Faster setup and better reliability
- You get yolo mode + cost consciousness
- More time for actual coding

**Implementation effort**: 2-4 hours
**Long-term maintenance**: ~1 hour/month vs 4-8 hours/month for V1

This is a no-brainer. Let's build it!