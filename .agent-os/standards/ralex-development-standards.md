# Ralex Development Standards - Agent-OS Enhanced

## Overview
These standards define development practices for the Ralex OpenCode.ai wrapper transformation project, utilizing Agent-OS cost optimization methodology.

## Cost Optimization Standards

### Model Usage Strategy
```yaml
Planning Phase:
  model: "openrouter/anthropic/claude-3.5-sonnet"
  usage: "Architecture decisions, complex reasoning"
  budget_allocation: "30-40% of total budget"
  max_cost_per_session: "$2.00"

Implementation Phase:
  model: "openrouter/meta-llama/llama-3.1-8b-instruct"
  usage: "Code generation from detailed specs"
  budget_allocation: "40-50% of total budget"
  max_cost_per_task: "$0.20"

Review Phase:
  model: "openrouter/anthropic/claude-3-haiku"
  usage: "Testing, debugging, optimization"
  budget_allocation: "10-20% of total budget"
  max_cost_per_review: "$0.50"
```

### Task Breakdown Requirements
- **Maximum task complexity**: Single focused objective
- **Maximum task cost**: $0.20 per micro-task
- **Target task cost**: $0.05-0.15 per micro-task
- **Task independence**: Each task executable standalone
- **Clear acceptance criteria**: Testable and measurable outcomes

### Pattern Caching Standards
```python
# Cache successful implementations
def cache_pattern(pattern_type: str, implementation: dict, success_metrics: dict):
    """
    Cache patterns for reuse across similar tasks
    Location: .khamel83/cache/
    Format: JSON with metadata
    """
```

## Code Quality Standards

### File Structure
```
ralex/
├── ralex/                    # Main package
│   ├── cli/                  # Command line interface
│   ├── core/                 # Core wrapper logic
│   ├── intelligence/         # Agent-OS intelligence layer
│   ├── integrations/         # OpenCode.ai, LiteLLM integrations
│   └── utils/               # Utilities and helpers
├── .agent-os/               # Agent-OS configuration
├── .khamel83/               # Cost optimization enhancements
├── tests/                   # Comprehensive test suite
└── docs/                    # Documentation
```

### Naming Conventions
- **Functions**: `snake_case` with descriptive names
- **Classes**: `PascalCase` with clear purpose
- **Constants**: `UPPER_SNAKE_CASE`
- **Files**: `snake_case.py`
- **Modules**: Short, descriptive names

### Documentation Requirements
```python
def example_function(param: str) -> dict:
    """
    Brief description of function purpose.
    
    Args:
        param: Description of parameter and expected format
        
    Returns:
        Dictionary containing result and metadata
        
    Raises:
        SpecificError: When specific condition occurs
        
    Cost: $0.05 (estimated)
    Dependencies: ["module1", "module2"]
    
    Example:
        >>> result = example_function("test")
        >>> assert result["success"] == True
    """
```

## Testing Standards

### Test Coverage Requirements
- **Minimum coverage**: 85% for all new code
- **Critical path coverage**: 95% for core functionality
- **Integration test coverage**: 100% for external APIs
- **Performance test coverage**: All time-critical operations

### Test Categories
```python
# Unit Tests - Test individual components
class TestTaskClassifier(unittest.TestCase):
    def test_simple_task_classification(self):
        """Test classification of simple tasks."""
        
    def test_complex_task_classification(self):
        """Test classification of complex tasks."""

# Integration Tests - Test component interactions  
class TestOpenCodeIntegration(unittest.TestCase):
    def test_opencode_wrapper_execution(self):
        """Test OpenCode.ai wrapper functionality."""

# End-to-End Tests - Test complete workflows
class TestCompleteWorkflow(unittest.TestCase):
    def test_simple_task_workflow(self):
        """Test complete simple task execution."""
```

### Performance Testing
```python
# Performance benchmarks for each task type
def benchmark_task_execution():
    """
    Benchmark requirements:
    - Simple tasks: <2 seconds response time
    - Complex tasks: <30 seconds total time
    - Cost tracking: <5% overhead
    - Memory usage: <100MB additional
    """
```

## Integration Standards

### OpenCode.ai Integration
```python
class OpenCodeWrapper:
    """
    Standards for OpenCode.ai integration:
    - Robust error handling for all failure modes
    - Timeout management (default: 60 seconds)
    - Credential validation before execution
    - Output parsing and validation
    - Security checks for dangerous operations
    """
```

### LiteLLM Integration
```python
class LiteLLMRouter:
    """
    Standards for LiteLLM integration:
    - Configuration validation on startup
    - Model availability checking
    - Cost tracking per request
    - Fallback routing for failures
    - Performance monitoring
    """
```

### Universal Logger Integration
```python
# Required logging for all operations
def execute_task(task_id: str, task_data: dict):
    """
    All operations must log:
    - Unique operation ID
    - Start/end timestamps  
    - Cost information
    - Performance metrics
    - Success/failure status
    - Error details if applicable
    """
```

## Security Standards

### Credential Management
```python
# Secure credential handling
class CredentialManager:
    """
    Security requirements:
    - Never log credentials in plain text
    - Use environment variables or secure storage
    - Validate credentials before use
    - Support credential rotation
    - Audit credential access
    """
```

### Input Validation
```python
def validate_user_input(input_data: str) -> bool:
    """
    Input validation requirements:
    - Sanitize all user inputs
    - Validate against known dangerous patterns
    - Limit input length and complexity
    - Log security validation decisions
    """
```

### Safe Execution
```python
def safe_execute(command: str) -> dict:
    """
    Safe execution requirements:
    - Validate commands before execution
    - Use sandboxed execution when possible
    - Implement rollback mechanisms
    - Audit all executed operations
    """
```

## Mobile Integration Standards

### iOS Compatibility
```python
class MobileAPIHandler:
    """
    Mobile integration requirements:
    - Maintain existing API endpoint compatibility
    - Preserve response format for mobile apps
    - Support OpenCat and other iOS clients
    - Handle mobile-specific optimizations
    - Test on actual mobile devices
    """
```

### API Response Format
```json
{
    "id": "operation-id",
    "success": true,
    "result": "operation result",
    "model_used": "model-identifier", 
    "cost": 0.05,
    "duration": 1.23,
    "mobile_optimized": true
}
```

## Version Control Standards

### Commit Standards
```bash
# Commit message format
[TASK_ID] Brief description of change

Detailed description:
- What was changed
- Why it was changed  
- Cost impact
- Testing performed

Cost: $0.05
Tests: All passing
```

### Branch Strategy
```
main                 # Production-ready code
├── phase-2         # Current development phase
├── phase-3         # Next phase preparation
└── task-A1         # Individual task branches
```

### Pull Request Requirements
- **All tests passing**: Unit, integration, and performance
- **Cost tracking**: Document cost impact of changes
- **Documentation updated**: All affected docs updated
- **Security review**: Security implications assessed
- **Mobile compatibility**: Mobile integration tested

## Performance Standards

### Response Time Requirements
```python
# Performance targets
SIMPLE_TASK_MAX_TIME = 2.0      # seconds
COMPLEX_TASK_MAX_TIME = 30.0    # seconds
SYSTEM_STARTUP_TIME = 5.0       # seconds
MOBILE_API_RESPONSE = 1.0       # seconds
```

### Resource Usage Limits
```python
# Resource constraints
MAX_MEMORY_USAGE = 100          # MB additional memory
MAX_CPU_USAGE = 50              # % CPU during execution
MAX_DISK_USAGE = 10             # MB for logs and cache
MAX_NETWORK_CALLS = 5           # Per user operation
```

### Monitoring Requirements
```python
def monitor_performance():
    """
    Required monitoring:
    - Response time per operation type
    - Resource usage trends
    - Error rates and types
    - Cost accumulation
    - User satisfaction metrics
    """
```

## Data Standards

### Universal Logging Format
```json
{
    "operation_id": "unique-identifier",
    "timestamp": "ISO-8601-format",
    "operation_type": "task-category",
    "model_used": "model-identifier",
    "cost": 0.05,
    "duration": 1.23,
    "success": true,
    "metadata": {
        "task_complexity": "simple",
        "routing_decision": "opencode",
        "user_context": "mobile"
    }
}
```

### Cost Tracking Schema
```json
{
    "cost_entry_id": "unique-identifier",
    "operation_id": "linked-operation",
    "model": "model-used",
    "tokens": {"input": 100, "output": 50},
    "cost": {"estimated": 0.05, "actual": 0.047},
    "savings": {"traditional": 0.50, "optimized": 0.047},
    "optimization_method": "agent-os-routing"
}
```

## Error Handling Standards

### Error Categories
```python
class RalexError(Exception):
    """Base exception for Ralex operations."""

class OpenCodeError(RalexError):
    """OpenCode.ai integration errors."""

class LiteLLMError(RalexError):
    """LiteLLM routing errors."""

class CostLimitError(RalexError):
    """Cost budget exceeded errors."""

class MobileCompatibilityError(RalexError):
    """Mobile integration errors."""
```

### Error Response Format
```json
{
    "success": false,
    "error": {
        "type": "OpenCodeError",
        "message": "Human-readable error message",
        "code": "OPENCODE_AUTH_FAILED",
        "details": "Technical details for debugging",
        "suggestions": ["Try refreshing credentials", "Check network connection"]
    },
    "operation_id": "for-tracking",
    "cost": 0.00
}
```

## Deployment Standards

### Environment Configuration
```yaml
# Development environment
RALEX_ENV: "development"
LOG_LEVEL: "DEBUG"
COST_LIMITS: "relaxed"
SAFETY_CHECKS: "enhanced"

# Production environment  
RALEX_ENV: "production"
LOG_LEVEL: "INFO"
COST_LIMITS: "strict"
SAFETY_CHECKS: "maximum"
```

### Health Check Requirements
```python
def health_check() -> dict:
    """
    Health check must validate:
    - OpenCode.ai connectivity and credentials
    - LiteLLM model availability
    - Universal logger functionality
    - Cost tracking accuracy
    - Mobile API endpoint availability
    """
```

These standards ensure consistent, high-quality development while maintaining the cost optimization benefits of the Agent-OS methodology.