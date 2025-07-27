# Minimal Viable Architecture Design
**Generated**: 2025-07-27 by Phase 17 Comprehensive Refactor Planning

## Executive Summary
Design for the absolute minimum architecture that completely embodies our cost-first agentic thinking philosophy. This is the target architecture after comprehensive rationalization.

**Philosophy**: "Cheap LLMs do agentic thinking within strict dollar constraints. Always solve within budget OR know it's impossible and stop."

---

## CORE ARCHITECTURAL PRINCIPLES

### 🎯 **Single Responsibility Components**
Each component has ONE job aligned with philosophy:
1. **Budget Enforcer**: Ensures dollar constraints never violated
2. **Intelligence Router**: Cost-first query classification and routing  
3. **Template Executor**: Applies agentic methodology to complex queries
4. **API Gateway**: Clean interface for mobile app integration
5. **Cost Tracker**: Real-time spending monitoring

### 🔄 **Zero Redundancy Rule**
- One way to do each thing
- No duplicate functionality
- No overlapping concerns
- No "just in case" features

### 📦 **Minimal Dependencies**
- LiteLLM (essential for multi-provider routing)
- PyYAML (essential for configuration)
- FastAPI (essential for mobile interface)
- **Total**: 3 external dependencies

---

## TARGET ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│                    RALEX MINIMAL STACK                     │
├─────────────────────────────────────────────────────────────┤
│  Mobile App (OpenCat) ──→ FastAPI Gateway ──→ Core Engine  │
└─────────────────────────────────────────────────────────────┘

Core Engine Flow:
1. Query → Budget Check → Cost Estimation → Route Decision
2. Simple → Cheap Model Direct
3. Complex → Template Selection → Agentic Execution
4. All → Cost Tracking → Response
```

### 🏗️ **Component Architecture**

```
ralex/
├── ralex_core.py           # 200 lines - Main orchestrator
├── budget_enforcer.py      # 80 lines - Hard budget constraints  
├── intelligence_router.py  # 120 lines - Cost-first routing
├── template_executor.py    # 100 lines - Agentic methodology
├── api_server.py          # 150 lines - FastAPI mobile interface
├── config.yaml            # 50 lines - Single configuration
└── templates/             # Agent-OS methodology templates
    ├── debug.yaml
    ├── refactor.yaml  
    └── test.yaml
```

**Total Core Implementation**: ~700 lines
**Current Bloated Implementation**: ~127,000 lines
**Reduction Achievement**: 99.45%

---

## COMPONENT SPECIFICATIONS

### 1. **Budget Enforcer** (`budget_enforcer.py`)

**Responsibility**: Absolute cost constraint enforcement
**Philosophy Embodiment**: "Within strict dollar constraints"

```python
class BudgetEnforcer:
    def __init__(self, daily_limit: float):
        self.daily_limit = daily_limit
        self.cost_tracker = CostTracker()
    
    def check_budget(self, estimated_cost: float) -> dict:
        """Hard stop if budget would be exceeded"""
        current_spent = self.cost_tracker.get_daily_spending()
        
        if current_spent + estimated_cost > self.daily_limit:
            return {
                "allowed": False,
                "reason": "Budget exceeded",
                "remaining": self.daily_limit - current_spent,
                "requested": estimated_cost
            }
        
        return {"allowed": True, "remaining": self.daily_limit - current_spent - estimated_cost}
    
    def estimate_cost(self, query: str, model: str) -> float:
        """Predict query cost before execution"""
        # Model-specific cost estimation
        token_count = len(query.split()) * 1.3  # Rough token estimation
        
        cost_per_token = {
            "openrouter/meta-llama/llama-3.1-8b-instruct": 0.00000006,
            "gpt-4": 0.00003,
            "openrouter/anthropic/claude-3.5-sonnet": 0.000015
        }
        
        return token_count * cost_per_token.get(model, 0.00001)
```

**Key Features**:
- Hard budget stops (core philosophy requirement)
- Pre-execution cost estimation
- Real-time budget tracking
- Graceful failure with budget information

### 2. **Intelligence Router** (Enhanced `intelligence_router.py`)

**Responsibility**: Cost-first query classification and model selection
**Philosophy Embodiment**: "Cheap LLMs do thinking"

```python
class IntelligenceRouter:
    def __init__(self):
        self.config = self.load_config()
        self.budget_enforcer = BudgetEnforcer(self.config['daily_budget'])
    
    def route_query(self, query: str) -> dict:
        """Cost-first routing with budget enforcement"""
        # Step 1: Classify intent (cheap operation)
        intent = self.classify_intent(query)
        
        # Step 2: Select model tier based on intent
        model_tier = "cheap" if intent == "simple" else "medium"
        model = self.get_model_for_tier(model_tier)
        
        # Step 3: Budget enforcement (CRITICAL)
        estimated_cost = self.budget_enforcer.estimate_cost(query, model)
        budget_check = self.budget_enforcer.check_budget(estimated_cost)
        
        if not budget_check["allowed"]:
            return {
                "error": "Budget constraint violated",
                "budget_status": budget_check,
                "philosophy": "System stops rather than exceed budget"
            }
        
        # Step 4: Route decision
        return {
            "model": model,
            "model_tier": model_tier,
            "route": "template" if intent == "complex" else "direct",
            "estimated_cost": estimated_cost,
            "budget_remaining": budget_check["remaining"]
        }
```

**Key Features**:
- Integrated budget enforcement
- Cost estimation before routing
- Hard stops when budget would be exceeded
- Simple, fast classification

### 3. **Template Executor** (`template_executor.py`)

**Responsibility**: Apply agentic methodology to complex queries
**Philosophy Embodiment**: "Agentic thinking"

```python
class TemplateExecutor:
    def __init__(self):
        self.templates = self.load_templates()
    
    def execute_with_template(self, query: str, template_type: str) -> dict:
        """Apply systematic methodology from templates"""
        template = self.templates.get(template_type, {})
        workflow = template.get('workflow', {})
        
        # Apply template workflow to query
        enhanced_query = self.apply_workflow(query, workflow)
        
        return {
            "original_query": query,
            "enhanced_query": enhanced_query,
            "template_applied": template_type,
            "methodology": workflow,
            "agentic": True
        }
    
    def apply_workflow(self, query: str, workflow: dict) -> str:
        """Apply systematic thinking to query"""
        # Add template-specific context and methodology
        methodology_prompt = f"""
        Apply systematic {workflow.get('category', 'development')} methodology:
        
        Original Request: {query}
        
        Systematic Approach:
        {self.format_workflow_steps(workflow)}
        
        Cost Constraints: Use minimal resources while ensuring quality.
        Time Budget: Complete within template time limits.
        """
        
        return methodology_prompt
```

**Key Features**:
- Systematic methodology application
- Template-driven thinking enhancement
- Cost-conscious prompt engineering
- Measurable agentic vs ad-hoc behavior

### 4. **API Server** (`api_server.py`)

**Responsibility**: Clean OpenAI-compatible interface for mobile apps
**Philosophy Embodiment**: Minimal, efficient mobile integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Ralex API", version="2.0.0")

class ChatRequest(BaseModel):
    model: str = "ralex-bridge"
    messages: list
    max_tokens: int = 150

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """OpenAI-compatible chat completions endpoint"""
    core = RalexCore()
    
    # Extract latest message
    user_message = request.messages[-1]["content"]
    
    # Process through core engine
    result = await core.process_query(user_message)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # Return OpenAI-compatible response
    return {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": result["response"]
            }
        }],
        "model": result["model_used"],
        "usage": {
            "total_tokens": result["token_count"],
            "prompt_tokens": result["input_tokens"],
            "completion_tokens": result["output_tokens"]
        }
    }

@app.get("/v1/models")
async def list_models():
    """List available models"""
    return {
        "data": [
            {"id": "ralex-bridge", "object": "model"},
            {"id": "ralex-cheap", "object": "model"},
            {"id": "ralex-medium", "object": "model"}
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "philosophy": "cost-first agentic thinking"}
```

**Key Features**:
- OpenAI-compatible interface
- Mobile app integration ready
- Health monitoring
- Minimal, focused endpoints

### 5. **Core Orchestrator** (`ralex_core.py`)

**Responsibility**: Coordinate all components
**Philosophy Embodiment**: Single decision point

```python
class RalexCore:
    def __init__(self):
        self.router = IntelligenceRouter()
        self.executor = TemplateExecutor()
        self.budget_enforcer = BudgetEnforcer(5.00)  # $5 daily limit
        
    async def process_query(self, query: str) -> dict:
        """Main processing pipeline with budget enforcement"""
        
        # Step 1: Intelligence routing with budget check
        routing = self.router.route_query(query)
        
        if "error" in routing:
            return routing  # Budget exceeded - hard stop
        
        # Step 2: Execute based on route
        if routing["route"] == "template":
            # Complex query - use agentic methodology
            template_type = self.detect_template_type(query)
            execution = self.executor.execute_with_template(query, template_type)
            enhanced_query = execution["enhanced_query"]
        else:
            # Simple query - direct execution
            enhanced_query = query
            execution = {"agentic": False, "template_applied": None}
        
        # Step 3: LiteLLM call with cost tracking
        response = await self.call_model(enhanced_query, routing["model"])
        
        # Step 4: Cost tracking
        actual_cost = self.calculate_actual_cost(response)
        self.budget_enforcer.record_cost(actual_cost)
        
        return {
            "response": response["content"],
            "model_used": routing["model"],
            "estimated_cost": routing["estimated_cost"],
            "actual_cost": actual_cost,
            "budget_remaining": routing["budget_remaining"] - actual_cost,
            "agentic": execution.get("agentic", False),
            "template_used": execution.get("template_applied"),
            "philosophy_embodied": True
        }
```

**Key Features**:
- Centralized decision making
- Budget enforcement at every step
- Cost tracking and reporting
- Clear agentic vs direct execution paths

---

## CONFIGURATION CONSOLIDATION

### 📄 **Single Configuration File** (`config.yaml`)

```yaml
# Ralex Minimal Configuration
# Philosophy: Cost-first agentic thinking within strict dollar constraints

# Budget constraints (core philosophy)
budget:
  daily_limit: 5.00
  weekly_limit: 25.00
  cost_per_query_max: 0.10
  
# Model tiers (cost-optimized)
models:
  cheap:
    - "openrouter/meta-llama/llama-3.1-8b-instruct"
    - "openrouter/anthropic/claude-3-haiku"
  medium:
    - "gpt-4"
    - "openrouter/anthropic/claude-3.5-sonnet"
  premium:  # Only for emergency escalation
    - "gpt-4o"
    
# Intelligence routing
intelligence:
  enabled: true
  routing_timeout: 1.0  # seconds
  classification_method: "keyword"
  
# API configuration
api:
  host: "0.0.0.0"
  port: 8000
  cors_enabled: true
  rate_limit: "100/minute"
  
# Cost tracking
tracking:
  enabled: true
  log_file: ".ralex/cost_log.json"
  real_time: true
  
# Template system
templates:
  enabled: true
  directory: "./templates"
  default_timeout: "30min"
```

**Total Configuration**: 50 lines
**Current Scattered Config**: 200+ lines across multiple files
**Consolidation**: Single source of truth

---

## DEPENDENCY MINIMIZATION

### 📦 **Essential Dependencies Only**

```requirements.txt
# Ralex Minimal Dependencies
# Philosophy: Don't reinvent the wheel, but minimize complexity

# Core functionality
litellm>=1.0.0          # Multi-provider LLM routing
pyyaml>=6.0             # Configuration management  
fastapi>=0.100.0        # API server
uvicorn>=0.20.0         # ASGI server

# Optional: Development only
pytest>=7.0.0           # Testing (dev only)
ruff>=0.1.0             # Linting (dev only)
```

**Production Dependencies**: 4 packages
**Current Bloated Dependencies**: 100+ packages
**Size Reduction**: 95% smaller dependency tree

### 🚫 **Eliminated Dependencies**

- **OpenWebUI**: 40MB+ of web interface complexity
- **Streamlit**: Legacy web interface 
- **Multiple config parsers**: JSON, TOML, INI handlers
- **Legacy routing**: Custom model selection logic
- **Development cruft**: Unused testing frameworks

---

## DATA FLOW ARCHITECTURE

### 🔄 **Request Processing Pipeline**

```
Mobile Request → FastAPI → Core Orchestrator
                             ↓
                        Budget Check ←→ Cost Tracker
                             ↓
                        Intelligence Router
                             ↓
                    Simple Query ←→ Complex Query
                         ↓              ↓
                    Direct Model → Template Executor
                         ↓              ↓
                    LiteLLM Call ←← Enhanced Query
                         ↓
                    Response + Cost Tracking
                         ↓
                    Mobile App Response
```

**Pipeline Characteristics**:
- **Budget check first** - No execution without budget approval
- **Cost tracking at every step** - Real-time spending monitoring
- **Clear decision points** - Simple vs complex routing
- **Graceful failures** - Budget exceeded = clean stop

### 💾 **State Management**

**Minimal State Requirements**:
- Daily spending total (in-memory + persistent)
- Query classification cache (optional, in-memory only)
- Template selection history (for optimization)

**Eliminated State**:
- Session files (markdown context)
- Complex configuration hierarchies  
- Legacy routing state
- OpenWebUI database

---

## PERFORMANCE CHARACTERISTICS

### ⚡ **Target Performance Metrics**

| Metric | Current | Target | Improvement |
|--------|---------|---------|-------------|
| Startup Time | 30s | 3s | 10x faster |
| Memory Usage | 300MB | 30MB | 10x smaller |
| Query Response | Variable | <2s | Consistent |
| Budget Check | N/A | <10ms | New feature |
| LOC Complexity | 127k | 700 | 99.5% reduction |

### 🎯 **Philosophy Embodiment Metrics**

| Philosophy Aspect | Implementation | Measurement |
|------------------|----------------|-------------|
| "Cheap LLMs do thinking" | ✅ Intelligence router | 80%+ queries use cheap models |
| "Strict dollar constraints" | ✅ Budget enforcer | Zero budget overruns |
| "Always solve within budget" | ✅ Cost estimation | 100% pre-execution checks |
| "Know impossible and stop" | ✅ Graceful failure | Clear budget exceeded messages |
| "Agentic thinking" | ✅ Template execution | Complex queries use methodology |

---

## MIGRATION STRATEGY

### 📋 **Implementation Phases**

**Phase 1**: Core Component Implementation
- Build budget_enforcer.py (critical missing piece)
- Enhance intelligence_router.py with budget integration
- Create template_executor.py for agentic execution

**Phase 2**: API Server Implementation  
- Build minimal FastAPI server
- Implement OpenAI-compatible endpoints
- Mobile app integration testing

**Phase 3**: Integration and Testing
- Connect all components through ralex_core.py
- End-to-end philosophy validation
- Performance optimization

**Phase 4**: Bloat Elimination
- Remove OpenWebUI dependencies
- Delete dead code (model_router.py, etc.)
- Consolidate configuration

### ⚠️ **Risk Mitigation**

**Backwards Compatibility**:
- Keep mobile app interface identical
- Maintain cost logging format
- Preserve agent-os template structure

**Rollback Plan**:
- Feature flags for new components
- Parallel implementation during transition
- Git branch strategy for safe migration

---

## SUCCESS CRITERIA

### 🎯 **Architecture Success Metrics**

**Quantitative Goals**:
- LOC reduction: 99%+ (127k → 700 lines)
- Dependency reduction: 95%+ (100+ → 4 packages)
- Memory usage: 90%+ reduction (300MB → 30MB)
- Startup time: 90%+ improvement (30s → 3s)

**Qualitative Goals**:
- Philosophy embodiment: 95%+ score
- Code clarity: New developer understanding <30min
- Maintenance burden: 85%+ reduction
- Feature completeness: 100% core functionality retained

### ✅ **Philosophy Validation Criteria**

1. **Budget constraints are hard limits** - System never exceeds configured budget
2. **Cheap models handle majority** - 80%+ of queries use cost-optimized routing
3. **Agentic methodology applied** - Complex queries demonstrably use templates
4. **Graceful failure modes** - Clear budget exceeded messages with remaining budget
5. **Cost-first decision making** - Every choice optimizes for minimum cost

---

*Next Phase: Detailed refactor execution plan with step-by-step implementation*