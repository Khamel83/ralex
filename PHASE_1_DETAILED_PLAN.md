# Ralex V2 Phase 1: Proof of Concept - Detailed Execution Plan

## Overview
**Goal**: Validate that OpenCode.ai + LiteLLM + OpenRouter integration actually works
**Timeline**: 2-3 hours
**Success**: Can send a request through the complete chain and get a response

## Pre-Execution Checklist

### Environment Prerequisites
- [ ] OPENROUTER_API_KEY environment variable set
- [ ] OpenCode.ai installed and accessible
- [ ] Python 3.11+ available
- [ ] Git repository cloned
- [ ] Network connectivity to OpenRouter

### Risk Assessment
**High Risk**: OpenCode.ai may not support custom proxy endpoints
**Mitigation**: Test multiple proxy configuration methods
**Backup Plan**: Use curl/direct API testing if OpenCode.ai integration fails

## Detailed Task Breakdown

### Task 1.1: Component Validation (30 minutes)

#### 1.1.1 OpenCode.ai Functionality Test
```bash
# Verify installation
export PATH=/home/RPI3/.opencode/bin:$PATH
opencode --version

# Test basic functionality
opencode --help | grep -i proxy  # Look for proxy options
opencode --help | grep -i model  # Look for model options

# Test with environment variable method
export OPENAI_API_BASE="http://localhost:4000/v1"
export OPENAI_API_KEY="test"
```

**Expected Output**: Version number, help text, proxy/model options
**Failure Action**: Document exact error, research alternative config methods

#### 1.1.2 LiteLLM Proxy Test
```bash
# Create test environment
python3 -m venv .test-env
source .test-env/bin/activate
pip install 'litellm[proxy]'

# Test basic proxy startup
.test-env/bin/litellm --model openrouter/google/gemini-flash-1.5 --port 4000 &
PROXY_PID=$!

# Wait and test
sleep 5
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 10
  }'

# Cleanup
kill $PROXY_PID
```

**Expected Output**: HTTP 200 response with chat completion
**Failure Action**: Debug proxy startup, check OpenRouter connectivity

#### 1.1.3 OpenRouter Direct Test
```bash
# Test direct OpenRouter connectivity
curl -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "X-Title: Ralex-V2-Test" \
  -d '{
    "model": "google/gemini-flash-1.5",
    "messages": [{"role": "user", "content": "Say hello"}],
    "max_tokens": 10
  }'
```

**Expected Output**: JSON response with completion
**Failure Action**: Check API key, network connectivity

### Task 1.2: Integration Testing (60 minutes)

#### 1.2.1 LiteLLM with OpenRouter Configuration
```bash
# Create minimal test config
cat > test_config.yaml << EOF
model_list:
  - model_name: "test-model"
    litellm_params:
      model: "openrouter/google/gemini-flash-1.5"
      api_base: "https://openrouter.ai/api/v1"
      api_key: "${OPENROUTER_API_KEY}"

litellm_settings:
  set_verbose: true
EOF

# Test with config
.test-env/bin/litellm --config test_config.yaml --port 4000 &
PROXY_PID=$!
sleep 5

# Test proxy endpoint
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer fake-key" \
  -d '{
    "model": "test-model",
    "messages": [{"role": "user", "content": "Test message"}],
    "max_tokens": 20
  }'

kill $PROXY_PID
```

**Expected Output**: Successful proxy → OpenRouter → response flow
**Failure Action**: Debug config, check logs, verify API routing

#### 1.2.2 OpenCode.ai Proxy Integration Test
```bash
# Method 1: Environment variables
export OPENAI_API_BASE="http://localhost:4000/v1"
export OPENAI_API_KEY="fake-key"

# Start proxy
.test-env/bin/litellm --config test_config.yaml --port 4000 &
PROXY_PID=$!
sleep 5

# Test OpenCode.ai with proxy
echo "Test request" | opencode run --model test-model

kill $PROXY_PID
```

**Expected Output**: OpenCode.ai → LiteLLM → OpenRouter → response
**Failure Action**: Try alternative config methods

#### 1.2.3 Alternative Integration Methods
```bash
# Method 2: Direct model specification
opencode run --model "http://localhost:4000/v1/test-model" "Test message"

# Method 3: Configuration file (if supported)
cat > opencode_config.json << EOF
{
  "api_base": "http://localhost:4000/v1",
  "api_key": "fake-key",
  "model": "test-model"
}
EOF

opencode run --config opencode_config.json "Test message"
```

### Task 1.3: Cost Routing Validation (60 minutes)

#### 1.3.1 Multi-Model Configuration
```bash
cat > routing_test_config.yaml << EOF
model_list:
  - model_name: "cheap"
    litellm_params:
      model: "openrouter/google/gemini-flash-1.5"
      api_base: "https://openrouter.ai/api/v1"
      api_key: "${OPENROUTER_API_KEY}"
  
  - model_name: "smart"
    litellm_params:
      model: "openrouter/anthropic/claude-3.5-sonnet"
      api_base: "https://openrouter.ai/api/v1"
      api_key: "${OPENROUTER_API_KEY}"

router_settings:
  routing_strategy: "simple-shuffle"  # Start simple
EOF
```

#### 1.3.2 Manual Routing Test
```bash
# Start multi-model proxy
.test-env/bin/litellm --config routing_test_config.yaml --port 4000 &
PROXY_PID=$!
sleep 5

# Test cheap model
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer fake-key" \
  -d '{
    "model": "cheap",
    "messages": [{"role": "user", "content": "Fix typo: teh → the"}],
    "max_tokens": 10
  }'

# Test smart model  
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer fake-key" \
  -d '{
    "model": "smart", 
    "messages": [{"role": "user", "content": "Analyze this architecture"}],
    "max_tokens": 50
  }'

kill $PROXY_PID
```

#### 1.3.3 Cost Tracking Validation
```bash
# Create simple cost tracker
cat > simple_tracker.py << EOF
import json
import time
from datetime import datetime

def log_request(model, prompt, response_tokens):
    cost_per_token = {
        "cheap": 0.000001,  # Gemini Flash estimate
        "smart": 0.000015   # Claude Sonnet estimate
    }
    
    cost = response_tokens * cost_per_token.get(model, 0.00001)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "prompt_length": len(prompt.split()),
        "response_tokens": response_tokens,
        "estimated_cost": cost
    }
    
    print(f"💰 Request cost: ${cost:.6f} ({model}, {response_tokens} tokens)")
    
    # Log to file
    with open("cost_log.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

if __name__ == "__main__":
    log_request("cheap", "Fix typo", 5)
    log_request("smart", "Analyze architecture", 100)
EOF

python3 simple_tracker.py
```

## Success Criteria Validation

### Phase 1 Success Checklist
- [ ] OpenCode.ai successfully installed and functional
- [ ] LiteLLM proxy starts without errors
- [ ] OpenRouter API responds to direct requests
- [ ] Proxy successfully routes to OpenRouter
- [ ] OpenCode.ai can communicate with proxy
- [ ] Multi-model routing works (cheap vs smart)
- [ ] Basic cost tracking implemented
- [ ] End-to-end flow: OpenCode.ai → LiteLLM → OpenRouter → Response

### Performance Benchmarks
- [ ] Response time < 10 seconds for simple requests
- [ ] Proxy startup time < 5 seconds
- [ ] No memory leaks over 30-minute test period
- [ ] Error rate < 5% over 20 test requests

### Documentation Requirements
- [ ] All working configurations documented
- [ ] Error scenarios and solutions recorded
- [ ] Performance metrics captured
- [ ] Next phase recommendations prepared

## Failure Scenarios & Contingency Plans

### Scenario 1: OpenCode.ai Doesn't Support Custom Proxy
**Detection**: No proxy configuration options found
**Contingency**: Use direct API testing, document limitation
**Impact**: Medium - limits yolo mode integration

### Scenario 2: LiteLLM OpenRouter Integration Fails  
**Detection**: Proxy returns errors when routing to OpenRouter
**Contingency**: Test direct OpenAI compatibility mode
**Impact**: High - breaks core value proposition

### Scenario 3: Cost Routing Doesn't Work
**Detection**: All requests go to same model regardless of pattern
**Contingency**: Manual model selection, simplified routing
**Impact**: Medium - reduces cost optimization

### Scenario 4: Performance Unacceptable
**Detection**: Response times > 10 seconds consistently
**Contingency**: Optimize config, reduce functionality
**Impact**: Low - feature vs performance tradeoff

## Phase 1 Deliverables

### Working Configurations
- `test_config.yaml` - Basic LiteLLM setup
- `routing_test_config.yaml` - Multi-model routing
- `opencode_proxy_setup.sh` - OpenCode.ai integration script

### Test Results
- `integration_test_results.md` - Complete test outcomes
- `performance_metrics.json` - Response times, error rates
- `cost_analysis.md` - Cost routing effectiveness

### Documentation
- `phase1_lessons_learned.md` - Issues encountered and solutions
- `phase2_recommendations.md` - Next steps based on findings
- `troubleshooting_guide.md` - Common issues and fixes

## Transition to Phase 2

### Go/No-Go Decision Criteria
**GO**: All success criteria met, performance acceptable
**NO-GO**: Critical integration points fail, performance unacceptable

### Phase 2 Preparation
- Documented working configurations
- Identified optimization opportunities  
- Risk mitigation strategies for known issues
- Resource requirements for Phase 2

**Phase 1 must prove the concept works before investing in Phase 2 development.**