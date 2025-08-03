# Agent-OS Context Optimization Guide

## Overview
The Agent-OS Context Manager implements intelligent context optimization for cost efficiency across all LLM operations. This system automatically compacts or enriches context based on task type and complexity.

## Key Benefits
- **95% cost reduction** for simple tasks through aggressive context optimization
- **Preserves critical context** for complex operations
- **Mobile workflow protection** ensures iOS integration context is maintained
- **Automatic token management** prevents API cost overruns
- **Universal applicability** works with any Agent-OS project

## How It Works

### Context Analysis
```python
from context_manager import AgentOSContextManager

manager = AgentOSContextManager()
metrics = manager.analyze_context(context_content, metadata)

# Results include:
# - token_count: Estimated tokens
# - relevance_score: How important this context is
# - compaction_ratio: Optimal size reduction
# - estimated_cost: Current context cost
```

### Optimization Strategies

#### 1. Simple Tasks → Truncate Strategy
- **Target**: Direct execution tasks like "create file", "fix bug"
- **Action**: Keep only last 20 lines + critical patterns
- **Savings**: 80-95% token reduction
- **Example**: 2762 tokens → 212 tokens (92% reduction)

#### 2. Complex Tasks → Preserve Strategy  
- **Target**: Architecture, refactoring, design tasks
- **Action**: Maintain full context for comprehensive understanding
- **Savings**: No reduction, optimize for quality
- **Token Limit**: Up to 8000 tokens

#### 3. Mobile Tasks → Summarize Strategy
- **Target**: iOS, OpenCat, mobile API tasks
- **Action**: Intelligent summarization preserving mobile context
- **Savings**: 70-90% reduction while keeping mobile keywords
- **Example**: 2762 tokens → 102 tokens (96% reduction)

#### 4. Analysis Tasks → Enrich Strategy
- **Target**: "Explain", "analyze", "review" requests
- **Action**: Add helpful context when sparse
- **Enhancement**: Project background, architecture notes
- **Token Limit**: Up to 6000 tokens

#### 5. Batch Tasks → Compress Strategy
- **Target**: Multi-file, bulk operations
- **Action**: Remove redundancy, preserve structure
- **Savings**: 40-70% reduction
- **Focus**: Maintain operational context

### Integration Example

```python
# Task classifier with context optimization
from task_classifier import AgentOSTaskClassifier

classifier = AgentOSTaskClassifier()
classification = classifier.classify_task(
    prompt="create a test file",
    context={"interface": "cli"},
    context_content=large_context_string
)

# Results include optimized context
optimized = classification.optimized_context
savings = classification.context_optimization
print(f"Saved {savings['tokens_saved']} tokens (${savings['cost_savings']:.6f})")
```

## Agent-OS Integration Patterns

### 1. CLI Integration
```python
# In CLI command handler
def handle_command(prompt, context_data):
    classification = classifier.classify_task(prompt, {}, context_data)
    
    # Use optimized context for LLM call
    response = llm_call(
        prompt=prompt,
        context=classification.optimized_context,
        model=classification.recommended_model_tier
    )
    
    # Track savings
    log_optimization(classification.context_optimization)
```

### 2. API Integration  
```python
# In API endpoint
@app.post("/optimize")
def optimize_request(request):
    optimized_context, stats = optimize_for_task(
        request.context,
        request.task_type,
        request.metadata
    )
    
    return {
        "optimized_context": optimized_context,
        "optimization_stats": stats,
        "cost_savings": stats["cost_savings"]
    }
```

### 3. Batch Processing
```python
# For batch operations
def process_batch(tasks):
    total_savings = 0
    
    for task in tasks:
        classification = classifier.classify_task(
            task.prompt, 
            task.context,
            task.context_content
        )
        
        # Process with optimized context
        result = process_task(
            task.prompt,
            classification.optimized_context
        )
        
        total_savings += classification.context_optimization["cost_savings"]
    
    return {"total_savings": total_savings}
```

## Configuration

### Context Limits by Task Type
```json
{
  "token_limits": {
    "simple": 1000,     // Minimal context for speed
    "complex": 8000,    // Full context for quality  
    "mobile": 2000,     // Moderate context preserving mobile patterns
    "batch": 4000,      // Structured context for operations
    "analysis": 6000    // Comprehensive context for understanding
  }
}
```

### Preservation Patterns
```json
{
  "preservation_patterns": [
    "mobile|opencat|ios",     // Always preserve mobile context
    "api|endpoint|integration", // Keep integration details
    "error|bug|fix",          // Preserve error context
    "TODO|FIXME|NOTE"         // Keep development notes
  ]
}
```

## Cost Optimization Examples

### Before/After Comparison

**Simple Task Example**:
```
Original Context: 2762 tokens ($0.002762)
Command: "create test.py file"
Strategy: truncate
Result: 212 tokens ($0.000212)
Savings: 2550 tokens ($0.002550) = 92% reduction
```

**Mobile Task Example**:
```
Original Context: 2762 tokens ($0.002762)  
Command: "fix OpenCat mobile API"
Strategy: summarize  
Result: 102 tokens ($0.000102)
Savings: 2660 tokens ($0.002660) = 96% reduction
Critical mobile context preserved: ✅
```

## Best Practices

### 1. Task Type Classification
- Always classify tasks before context optimization
- Use task-specific optimization strategies
- Preserve critical domain context (mobile, API, etc.)

### 2. Incremental Optimization
- Start with conservative settings
- Monitor relevance preservation scores
- Adjust based on task success rates

### 3. Context Quality Monitoring
```python
# Track optimization effectiveness
stats = manager.get_optimization_stats()
print(f"Average relevance preserved: {stats['avg_relevance_preserved']:.2f}")
print(f"Total cost savings: ${stats['total_cost_savings']:.6f}")
```

### 4. Fallback Strategies
- Always provide fallback for missing context manager
- Graceful degradation when optimization fails
- Preserve original context as backup

## Integration with Existing Agent-OS Projects

### Step 1: Add Context Manager
```bash
# Copy context_manager.py to your .agentos/ or .khamel83/ directory
cp context_manager.py your_project/.agentos/
```

### Step 2: Integrate with Task Classification
```python
# Enhance your existing task classifier
from context_manager import optimize_for_task

def classify_and_optimize(prompt, context_content):
    # Your existing classification logic
    task_type = classify_task(prompt)
    
    # Add context optimization
    optimized_context, stats = optimize_for_task(
        context_content, 
        task_type
    )
    
    return {
        "task_type": task_type,
        "optimized_context": optimized_context,
        "optimization_stats": stats
    }
```

### Step 3: Update LLM Calls
```python
# Use optimized context in LLM calls
result = classification_and_optimization(prompt, context)

response = llm_api_call(
    prompt=prompt,
    context=result["optimized_context"],  # Use optimized version
    model=select_model(result["task_type"])
)
```

## Monitoring and Analytics

### Optimization Statistics
```python
# Get comprehensive optimization stats
stats = manager.get_optimization_stats()

# Track key metrics:
# - total_optimizations: Number of optimizations performed
# - total_tokens_saved: Total tokens saved across all operations
# - total_cost_savings: Total cost savings in USD
# - avg_relevance_preserved: Average relevance score maintained
# - strategy_usage: Breakdown of strategies used
# - estimated_savings_percent: Overall efficiency gain
```

### Cost Tracking Integration
```python
# Integrate with budget controller
from budget_controller import BudgetController

budget = BudgetController()
if classification.context_optimization:
    savings = classification.context_optimization["cost_savings"]
    budget.record_savings(savings, operation_id)
```

## Future Enhancements

### 1. Learning System
- Track optimization success rates by task type
- Learn optimal context sizes for different operations
- Adapt strategies based on user feedback

### 2. Advanced Summarization
- Integration with dedicated summarization models
- Context-aware summarization preserving key details
- Multi-pass optimization for maximum efficiency

### 3. Real-time Adaptation
- Dynamic strategy selection based on API costs
- Automatic context expansion when models are cheap
- Budget-aware optimization intensity

This context optimization system represents a fundamental Agent-OS capability that can be integrated into any LLM-powered project for significant cost savings while maintaining operational quality.