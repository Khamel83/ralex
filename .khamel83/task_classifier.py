#!/usr/bin/env python3
"""
Agent-OS Task Classifier for Ralex
Analyzes prompts and classifies tasks for optimal routing decisions.
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

# Import context manager and LiteLLM router for optimization
try:
    from context_manager import AgentOSContextManager, optimize_for_task
    from litellm_router import LiteLLMRouter, RoutingStrategy
except ImportError:
    # Fallback if modules not available
    def optimize_for_task(context, task_type, metadata=None):
        return context, {"strategy": "no_optimization", "tokens_saved": 0}
    
    class LiteLLMRouter:
        def route_request(self, task_classification, budget_limit=None):
            from types import SimpleNamespace
            return SimpleNamespace(
                selected_model="fallback_model",
                tier=SimpleNamespace(value="budget"),
                estimated_cost=0.001,
                reasoning="Fallback routing - LiteLLM router not available"
            )

class TaskType(Enum):
    SIMPLE = "simple"
    COMPLEX = "complex"
    MOBILE = "mobile"
    BATCH = "batch"
    ANALYSIS = "analysis"

class ComplexityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class TaskClassification:
    task_type: TaskType
    complexity: ComplexityLevel
    confidence: float
    reasoning: str
    estimated_cost: float
    recommended_model_tier: str
    execution_strategy: str
    context_optimization: Optional[Dict] = None
    optimized_context: Optional[str] = None
    routing_decision: Optional[Dict] = None

class AgentOSTaskClassifier:
    """
    Implements Agent-OS cost optimization through intelligent task classification.
    
    Classification Logic:
    - simple: Direct to OpenCode.ai (fast, cheap)
    - complex: Use cost optimization (planning + implementation)
    - mobile: Preserve iOS workflow compatibility
    - batch: Group similar operations for efficiency
    - analysis: Read-only operations requiring explanation
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or Path(__file__).parent / "classifier-config.json"
        self.patterns = self._load_patterns()
        self.cost_estimates = self._load_cost_estimates()
        
    def _load_patterns(self) -> Dict:
        """Load classification patterns from config."""
        default_patterns = {
            "simple_keywords": [
                "create file", "write function", "fix bug", "add comment",
                "rename variable", "format code", "simple test", "basic function"
            ],
            "complex_keywords": [
                "refactor", "architecture", "design pattern", "optimize",
                "integrate", "migrate", "transform", "comprehensive"
            ],
            "mobile_keywords": [
                "opencat", "ios", "mobile", "app", "ralex api", "endpoint"
            ],
            "batch_keywords": [
                "multiple files", "all tests", "entire codebase", "batch process"
            ],
            "analysis_keywords": [
                "explain", "analyze", "review", "understand", "how does",
                "what is", "why", "describe", "documentation"
            ]
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    config = json.load(f)
                    return config.get("patterns", default_patterns)
            except:
                pass
        
        return default_patterns
    
    def _load_cost_estimates(self) -> Dict:
        """Load cost estimation data."""
        return {
            TaskType.SIMPLE: {"base_cost": 0.01, "model_tier": "budget"},
            TaskType.COMPLEX: {"base_cost": 0.15, "model_tier": "standard"},
            TaskType.MOBILE: {"base_cost": 0.05, "model_tier": "budget"},
            TaskType.BATCH: {"base_cost": 0.25, "model_tier": "standard"},
            TaskType.ANALYSIS: {"base_cost": 0.02, "model_tier": "budget"}
        }
    
    def classify_task(self, prompt: str, context: Optional[Dict] = None, 
                     context_content: Optional[str] = None, 
                     budget_limit: Optional[float] = None) -> TaskClassification:
        """
        Main classification function implementing Agent-OS optimization logic.
        
        Args:
            prompt: User input to classify
            context: Additional context (file paths, session data, etc.)
            context_content: Raw context content for optimization
            budget_limit: Budget limit for LiteLLM routing
            
        Returns:
            TaskClassification with routing recommendations, optimized context, and model selection
        """
        context = context or {}
        prompt_lower = prompt.lower()
        
        # Calculate scores for each task type
        scores = self._calculate_scores(prompt_lower, context)
        
        # Determine primary task type
        task_type = max(scores, key=scores.get)
        confidence = scores[task_type]
        
        # Determine complexity
        complexity = self._analyze_complexity(prompt_lower, context)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(prompt, task_type, complexity, scores)
        
        # Estimate cost and recommend strategy
        cost_estimate = self._estimate_cost(task_type, complexity, context)
        model_tier = self.cost_estimates[task_type]["model_tier"]
        execution_strategy = self._recommend_execution_strategy(task_type, complexity)
        
        # Optimize context if provided
        context_optimization = None
        optimized_context = None
        
        if context_content:
            optimization_metadata = {
                **context,
                "task_type": task_type.value,
                "complexity": complexity.value,
                "prompt": prompt
            }
            
            optimized_context, context_optimization = optimize_for_task(
                context_content, 
                task_type.value, 
                optimization_metadata
            )
            
            # Update cost estimate with context optimization savings
            if context_optimization.get("cost_savings", 0) > 0:
                cost_estimate -= context_optimization["cost_savings"]
                reasoning += f" Context optimized: {context_optimization['tokens_saved']} tokens saved."
        
        # Create preliminary classification for routing
        preliminary_classification = TaskClassification(
            task_type=task_type,
            complexity=complexity,
            confidence=confidence,
            reasoning=reasoning,
            estimated_cost=cost_estimate,
            recommended_model_tier=model_tier,
            execution_strategy=execution_strategy,
            context_optimization=context_optimization,
            optimized_context=optimized_context,
            routing_decision=None
        )
        
        # Get LiteLLM routing decision
        routing_decision = None
        try:
            router = LiteLLMRouter()
            routing_result = router.route_request(preliminary_classification, budget_limit)
            
            routing_decision = {
                "selected_model": routing_result.selected_model,
                "provider": routing_result.provider,
                "tier": routing_result.tier.value,
                "strategy_used": routing_result.strategy_used.value,
                "estimated_cost": routing_result.estimated_cost,
                "reasoning": routing_result.reasoning,
                "fallback_models": routing_result.fallback_models,
                "optimization_applied": routing_result.optimization_applied
            }
            
            # Update final cost estimate with routing decision
            cost_estimate = routing_result.estimated_cost
            reasoning += f" Model routing: {routing_result.reasoning}"
            
        except Exception as e:
            # Fallback if routing fails
            routing_decision = {
                "selected_model": "fallback_model",
                "tier": "budget",
                "estimated_cost": cost_estimate,
                "reasoning": f"Routing failed: {e}",
                "error": str(e)
            }
        
        return TaskClassification(
            task_type=task_type,
            complexity=complexity,
            confidence=confidence,
            reasoning=reasoning,
            estimated_cost=cost_estimate,
            recommended_model_tier=model_tier,
            execution_strategy=execution_strategy,
            context_optimization=context_optimization,
            optimized_context=optimized_context,
            routing_decision=routing_decision
        )
    
    def _calculate_scores(self, prompt: str, context: Dict) -> Dict[TaskType, float]:
        """Calculate classification scores for each task type."""
        scores = {task_type: 0.0 for task_type in TaskType}
        
        # Keyword-based scoring
        for task_type in TaskType:
            pattern_key = f"{task_type.value}_keywords"
            if pattern_key in self.patterns:
                for keyword in self.patterns[pattern_key]:
                    if keyword in prompt:
                        scores[task_type] += 0.2
        
        # Context-based adjustments
        if context.get("file_count", 0) > 5:
            scores[TaskType.BATCH] += 0.3
            scores[TaskType.COMPLEX] += 0.2
        
        if context.get("interface") == "mobile":
            scores[TaskType.MOBILE] += 0.5
        
        # Pattern-based detection
        if re.search(r'\b(explain|analyze|review|understand)\b', prompt):
            scores[TaskType.ANALYSIS] += 0.4
        
        if re.search(r'\b(create|write|implement|build)\b', prompt):
            scores[TaskType.SIMPLE] += 0.3
        
        if re.search(r'\b(refactor|optimize|transform|migrate)\b', prompt):
            scores[TaskType.COMPLEX] += 0.4
        
        # Normalize scores
        max_score = max(scores.values()) if max(scores.values()) > 0 else 1.0
        return {k: min(v / max_score, 1.0) for k, v in scores.items()}
    
    def _analyze_complexity(self, prompt: str, context: Dict) -> ComplexityLevel:
        """Analyze task complexity for cost optimization."""
        complexity_score = 0
        
        # Word count influence
        word_count = len(prompt.split())
        if word_count > 50:
            complexity_score += 2
        elif word_count > 20:
            complexity_score += 1
        
        # File count influence
        file_count = context.get("file_count", 0)
        if file_count > 10:
            complexity_score += 3
        elif file_count > 3:
            complexity_score += 2
        elif file_count > 1:
            complexity_score += 1
        
        # Complexity keywords
        high_complexity_patterns = [
            r'\b(architecture|design pattern|refactor|migrate)\b',
            r'\b(optimize|performance|scale)\b',
            r'\b(integrate|connect|sync)\b'
        ]
        
        for pattern in high_complexity_patterns:
            if re.search(pattern, prompt):
                complexity_score += 2
        
        # Multiple operations
        operation_words = ["and", "then", "also", "additionally", "furthermore"]
        complexity_score += sum(1 for word in operation_words if word in prompt.lower())
        
        # Classify complexity
        if complexity_score >= 6:
            return ComplexityLevel.HIGH
        elif complexity_score >= 3:
            return ComplexityLevel.MEDIUM
        else:
            return ComplexityLevel.LOW
    
    def _generate_reasoning(self, prompt: str, task_type: TaskType, 
                          complexity: ComplexityLevel, scores: Dict) -> str:
        """Generate human-readable reasoning for classification."""
        top_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:2]
        
        reasoning = f"Classified as {task_type.value} task with {complexity.value} complexity. "
        
        if task_type == TaskType.SIMPLE:
            reasoning += "Direct OpenCode.ai execution recommended for efficiency."
        elif task_type == TaskType.COMPLEX:
            reasoning += "Agent-OS cost optimization recommended (planning + implementation phases)."
        elif task_type == TaskType.MOBILE:
            reasoning += "Mobile workflow optimization to preserve iOS integration."
        elif task_type == TaskType.BATCH:
            reasoning += "Batch processing recommended for multiple operations."
        elif task_type == TaskType.ANALYSIS:
            reasoning += "Analysis-focused task, minimal execution required."
        
        if len(top_scores) > 1 and top_scores[1][1] > 0.3:
            reasoning += f" Secondary classification: {top_scores[1][0].value} ({top_scores[1][1]:.2f})."
        
        return reasoning
    
    def _estimate_cost(self, task_type: TaskType, complexity: ComplexityLevel, 
                      context: Dict) -> float:
        """Estimate cost based on Agent-OS optimization principles."""
        base_cost = self.cost_estimates[task_type]["base_cost"]
        
        # Complexity multiplier
        complexity_multipliers = {
            ComplexityLevel.LOW: 1.0,
            ComplexityLevel.MEDIUM: 2.5,
            ComplexityLevel.HIGH: 5.0
        }
        
        complexity_multiplier = complexity_multipliers[complexity]
        
        # Context adjustments
        file_count = context.get("file_count", 1)
        file_multiplier = min(1 + (file_count - 1) * 0.2, 3.0)  # Cap at 3x
        
        estimated_cost = base_cost * complexity_multiplier * file_multiplier
        
        # Agent-OS optimization: Cap costs to prevent runaway
        return min(estimated_cost, 1.0)  # Max $1 per task
    
    def _recommend_execution_strategy(self, task_type: TaskType, 
                                    complexity: ComplexityLevel) -> str:
        """Recommend execution strategy based on Agent-OS principles."""
        if task_type == TaskType.SIMPLE and complexity == ComplexityLevel.LOW:
            return "direct_opencode"
        elif task_type == TaskType.COMPLEX or complexity == ComplexityLevel.HIGH:
            return "agentos_optimized"
        elif task_type == TaskType.MOBILE:
            return "mobile_preserved"
        elif task_type == TaskType.BATCH:
            return "batch_processed"
        elif task_type == TaskType.ANALYSIS:
            return "analysis_mode"
        else:
            return "standard_litellm"
    
    def get_routing_recommendation(self, classification: TaskClassification) -> Dict:
        """Get specific routing recommendations for LiteLLM."""
        strategy_map = {
            "direct_opencode": {
                "route": "opencode.yolo",
                "model": "fast",
                "timeout": 30,
                "retries": 1
            },
            "agentos_optimized": {
                "route": "agentos.cost_optimized",
                "model": "planning_then_implementation",
                "timeout": 300,
                "retries": 2
            },
            "mobile_preserved": {
                "route": "ralex.mobile",
                "model": "mobile_optimized",
                "timeout": 60,
                "retries": 2
            },
            "batch_processed": {
                "route": "litellm.batch",
                "model": "efficient",
                "timeout": 600,
                "retries": 1
            },
            "analysis_mode": {
                "route": "litellm.analysis",
                "model": "budget",
                "timeout": 60,
                "retries": 1
            },
            "standard_litellm": {
                "route": "litellm.standard",
                "model": "balanced",
                "timeout": 120,
                "retries": 2
            }
        }
        
        return strategy_map.get(classification.execution_strategy, 
                              strategy_map["standard_litellm"])

def quick_classify(prompt: str, context: Optional[Dict] = None) -> TaskClassification:
    """Quick classification function for CLI usage."""
    classifier = AgentOSTaskClassifier()
    return classifier.classify_task(prompt, context)

if __name__ == "__main__":
    # Test classification
    test_prompts = [
        "create a simple test.py file",
        "refactor the entire codebase architecture using design patterns",
        "fix the mobile API endpoint for OpenCat integration",
        "explain how the routing system works"
    ]
    
    classifier = AgentOSTaskClassifier()
    
    for prompt in test_prompts:
        result = classifier.classify_task(prompt)
        print(f"\nPrompt: {prompt}")
        print(f"Type: {result.task_type.value}")
        print(f"Complexity: {result.complexity.value}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Cost: ${result.estimated_cost:.3f}")
        print(f"Strategy: {result.execution_strategy}")
        print(f"Reasoning: {result.reasoning}")