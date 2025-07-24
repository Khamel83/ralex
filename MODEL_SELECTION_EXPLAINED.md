# Model Selection & Budget Logic Explained

## Who Decides Which Model to Use?

### 1. LiteLLM Router (Primary Decision Maker)
**Location**: `litellm_budget_config.yaml` - routing_rules section

```yaml
routing_rules:
  # Simple tasks → cheap model
  - pattern: "fix|typo|simple|quick|small|format"
    model: "cheap"  # Gemini Flash
    max_cost_per_request: 0.001
    
  # Complex tasks → smart model  
  - pattern: "refactor|analyze|complex|architecture|design|review"
    model: "smart"  # Claude Sonnet
    max_cost_per_request: 0.01
    
  # Yolo mode → ultra-fast cheap
  - pattern: "yolo|urgent|fast|now|quick"
    model: "yolo"   # Gemini Flash (limited tokens)
    max_cost_per_request: 0.0005
```

**How it works:**
1. User types: `"fix this typo"`
2. LiteLLM sees "fix" and "typo" in the request
3. Matches pattern → routes to "cheap" model (Gemini Flash)
4. Cost: ~$0.0001 per request

### 2. Budget-Based Override
**Location**: `litellm_budget_config.yaml` - budget_based_routing section

```yaml
budget_based_routing:
  # High budget: Use both cheap and smart models
  - budget_remaining: "> 2.00"
    preferred_models: ["cheap", "smart"]
    
  # Medium budget: Prefer cheap models
  - budget_remaining: "> 0.50"  
    preferred_models: ["cheap", "yolo"]
    
  # Low budget: Emergency mode (cheap only)
  - budget_remaining: "< 0.50"
    preferred_models: ["yolo"]
    max_tokens: 200
```

**Example Logic:**
- Budget remaining: $3.50 → "refactor this code" uses Claude Sonnet ($0.01)
- Budget remaining: $1.20 → "refactor this code" uses Gemini Flash ($0.001) 
- Budget remaining: $0.30 → "refactor this code" uses Gemini Flash (200 tokens max)

### 3. User Override (Optional)
**Location**: Command line arguments

```bash
# Force specific model
./yolo-budget-code.sh --model smart "simple task"   # Forces Claude Sonnet
./yolo-budget-code.sh --model cheap "complex task"  # Forces Gemini Flash
```

## Where Did These Budgets Come From?

### Current Budget Structure:
- **Daily Limit**: $5.00
- **Alert Thresholds**: 50% ($2.50), 80% ($4.00), 96% ($4.80)
- **Model Costs**: 
  - Gemini Flash: ~$0.000001/token
  - Claude Sonnet: ~$0.000015/token

### Budget Reasoning (Conservative Estimate):

#### Scenario 1: Full Day AI Coding (8 hours)
```
Assumptions:
- 50 requests per day 
- Mix: 70% simple (cheap) + 30% complex (smart)
- Average tokens per request: 1,000

Cost Breakdown:
- 35 simple requests × 1,000 tokens × $0.000001 = $0.035
- 15 complex requests × 1,000 tokens × $0.000015 = $0.225
- Total: $0.26/day

Current $5 budget = 19x safety margin
```

#### Scenario 2: High Intensity Programming (3-5 hours)
```
Assumptions:
- 100 requests in 4 hours
- Mix: 40% simple + 60% complex (more refactoring)
- Average tokens: 1,500 per request

Cost Breakdown:
- 40 simple × 1,500 × $0.000001 = $0.06
- 60 complex × 1,500 × $0.000015 = $1.35
- Total: $1.41/day

Current $5 budget = 3.5x safety margin
```

### **The Budget is VERY Conservative!**

You're absolutely right - we could easily do:
- **Full day coding**: ~$0.50-1.00/day realistic cost
- **High intensity**: ~$2.00-3.00/day realistic cost
- **Current $5 limit**: Allows for 5-10x safety margin

## AgentOS Integration & Smart Prompting

### How AgentOS Should Structure Prompts:

#### Small Requests (→ Cheap Model):
```bash
# AgentOS breaks down into atomic tasks
"fix syntax error on line 23"
"add docstring to function get_user()"  
"format this code block"
"add error handling to file.read()"
```

#### Big Requests (→ Smart Model):
```bash
# AgentOS sends complex architectural requests
"analyze the entire codebase and suggest performance improvements"
"refactor user authentication system for better security"
"design database schema for multi-tenant application"
"review code quality and suggest architectural changes"
```

### AgentOS Integration Points:

#### 1. Task Decomposition
**Location**: `~/.agent-os/instructions/execute-tasks.md`

AgentOS should break down:
```
User: "Improve this application"
↓
AgentOS breaks into:
1. "fix obvious bugs" (cheap)
2. "add unit tests" (cheap) 
3. "optimize performance bottlenecks" (smart)
4. "improve error handling" (cheap)
5. "refactor architecture" (smart)
```

#### 2. Smart Prompt Routing  
**Location**: Custom AgentOS standards

```markdown
# ~/.agent-os/standards/prompt-optimization.md

## Cheap Model Tasks (< 1000 tokens):
- Bug fixes
- Code formatting  
- Adding comments/docstrings
- Simple refactoring
- Syntax corrections

## Smart Model Tasks (> 1000 tokens):
- Architecture design
- Complex debugging
- Performance analysis
- Security reviews
- System design
```

## Virtual Environment Setup Check

### Current Status:
```bash
# Check if venv setup is working
ls -la | grep venv
# Should show: .venv-v2/ (or similar)

# Check if LiteLLM is properly installed
.venv-v2/bin/python -c "import litellm; print('OK')"

# Check if OpenCode.ai is accessible
export PATH="/home/RPI3/.opencode/bin:$PATH"
opencode --version
```

### Fix Virtual Environment Issues:

#### Option 1: Clean Setup
```bash
# Remove problematic venvs
rm -rf .venv-v2/ .test-env/

# Create fresh environment
python3 -m venv .ralex-env
source .ralex-env/bin/activate
pip install 'litellm[proxy]'
```

#### Option 2: System Installation (if venv issues persist)
```bash
# Install globally (not recommended but works)
pip install --user 'litellm[proxy]'
```

### Updated Setup Script:
```bash
#!/bin/bash
# setup-budget-tracking-fixed.sh

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if (( $(echo "$PYTHON_VERSION < 3.10" | bc -l) )); then
    echo "❌ Python 3.10+ required, found $PYTHON_VERSION"
    exit 1
fi

# Create clean virtual environment
if [ -d ".ralex-env" ]; then
    echo "🧹 Cleaning existing environment..."
    rm -rf .ralex-env
fi

echo "🐍 Creating virtual environment..."
python3 -m venv .ralex-env

echo "📦 Installing dependencies..."
.ralex-env/bin/pip install --upgrade pip
.ralex-env/bin/pip install 'litellm[proxy]'

echo "✅ Virtual environment ready: .ralex-env"
```

## Budget Recommendations

### Realistic Budget Tiers:

#### Conservative User ($2/day):
- Light coding (20-30 requests/day)
- Mostly simple tasks
- Emergency fallback budget

#### Normal User ($5/day - current):
- Full day coding
- Mix of simple and complex tasks  
- Good safety margin

#### Power User ($10/day):
- High intensity programming
- Lots of complex refactoring
- Multiple projects simultaneously

#### Team/Heavy Use ($20+/day):
- Continuous AI assistance
- Large codebase analysis
- Multiple developers

### Suggested Budget Adjustment:
```yaml
# In litellm_budget_config.yaml
general_settings:
  max_budget: 10.00  # Increase from 5.00
  budget_duration: "1d"
  
  budget_alerts:
    - threshold: 5.00   # 50% of $10
    - threshold: 8.00   # 80% of $10  
    - threshold: 9.50   # 95% of $10
```

**Bottom Line**: Current $5 budget is very conservative. You could realistically code all day on $2-3, so $10 daily budget would give you plenty of headroom for intensive programming sessions.