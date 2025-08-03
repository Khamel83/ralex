#!/usr/bin/env python3
"""
LiteLLM Router for Agent-OS Cost Optimization
Implements intelligent model routing based on task classification and budget constraints.
"""

import json
import os
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import time
import random

class ModelTier(Enum):
    BUDGET = "budget"
    STANDARD = "standard"
    PREMIUM = "premium"

class RoutingStrategy(Enum):
    COST_OPTIMIZED = "cost_optimized"
    PERFORMANCE_OPTIMIZED = "performance_optimized"
    BALANCED = "balanced"
    FALLBACK = "fallback"

@dataclass
class ModelConfig:
    name: str
    provider: str
    tier: ModelTier
    cost_per_token: float
    max_tokens: int
    strengths: List[str]
    best_for_tasks: List[str]
    availability: bool = True
    response_time_avg: float = 1.0

@dataclass
class RoutingDecision:
    selected_model: str
    provider: str
    tier: ModelTier
    strategy_used: RoutingStrategy
    estimated_cost: float
    reasoning: str
    fallback_models: List[str]
    optimization_applied: Dict[str, Any]

class LiteLLMRouter:
    """
    Agent-OS optimized LiteLLM router implementing cost-efficient model selection.
    
    Key Features:
    - Task-aware model routing (simple→budget, complex→standard/premium)
    - Cost optimization with budget constraints
    - Fallback routing for model availability
    - Performance tracking and learning
    - Integration with Agent-OS task classification
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or Path(__file__).parent / "litellm-config.json"
        self.model_configs = self._load_model_configs()
        self.routing_rules = self._load_routing_rules()
        self.performance_cache = {}
        self.routing_history = []
        
    def _load_model_configs(self) -> Dict[str, ModelConfig]:
        """Load model configurations for routing decisions."""
        default_models = {
            # Budget Tier - Optimized for cost efficiency
            "openrouter/anthropic/claude-3-haiku": ModelConfig(
                name="claude-3-haiku",
                provider="anthropic", 
                tier=ModelTier.BUDGET,
                cost_per_token=0.00000025,  # $0.25/1M tokens
                max_tokens=200000,
                strengths=["speed", "cost", "simple_tasks"],
                best_for_tasks=["simple", "analysis", "mobile"]
            ),
            "openrouter/meta-llama/llama-3.1-8b-instruct": ModelConfig(
                name="llama-3.1-8b",
                provider="meta",
                tier=ModelTier.BUDGET,
                cost_per_token=0.0000001,  # $0.10/1M tokens  
                max_tokens=128000,
                strengths=["ultra_low_cost", "speed"],
                best_for_tasks=["simple", "batch"]
            ),
            
            # Standard Tier - Balanced performance and cost
            "openrouter/anthropic/claude-3-sonnet": ModelConfig(
                name="claude-3-sonnet",
                provider="anthropic",
                tier=ModelTier.STANDARD,
                cost_per_token=0.000003,  # $3/1M tokens
                max_tokens=200000,
                strengths=["reasoning", "code", "complex_tasks"],
                best_for_tasks=["complex", "batch", "analysis"]
            ),
            "openrouter/openai/gpt-4o-mini": ModelConfig(
                name="gpt-4o-mini", 
                provider="openai",
                tier=ModelTier.STANDARD,
                cost_per_token=0.00000015,  # $0.15/1M tokens
                max_tokens=128000,
                strengths=["general_purpose", "fast"],
                best_for_tasks=["complex", "mobile", "analysis"]
            ),
            
            # Premium Tier - Maximum capability
            "openrouter/anthropic/claude-3-opus": ModelConfig(
                name="claude-3-opus",
                provider="anthropic", 
                tier=ModelTier.PREMIUM,
                cost_per_token=0.000015,  # $15/1M tokens
                max_tokens=200000,
                strengths=["advanced_reasoning", "complex_code", "architecture"],
                best_for_tasks=["complex"]
            ),
            "openrouter/openai/gpt-4": ModelConfig(
                name="gpt-4",
                provider="openai",
                tier=ModelTier.PREMIUM, 
                cost_per_token=0.00003,  # $30/1M tokens
                max_tokens=128000,
                strengths=["advanced_reasoning", "complex_analysis"],
                best_for_tasks=["complex", "analysis"]
            )
        }
        
        # Load from config file if exists
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    config_data = json.load(f)
                    loaded_models = {}
                    
                    for model_id, model_data in config_data.get("models", {}).items():
                        loaded_models[model_id] = ModelConfig(
                            name=model_data["name"],
                            provider=model_data["provider"],
                            tier=ModelTier(model_data["tier"]),
                            cost_per_token=model_data["cost_per_token"],
                            max_tokens=model_data["max_tokens"],
                            strengths=model_data["strengths"],
                            best_for_tasks=model_data["best_for_tasks"],
                            availability=model_data.get("availability", True),
                            response_time_avg=model_data.get("response_time_avg", 1.0)
                        )
                    
                    return {**default_models, **loaded_models}
            except Exception as e:
                print(f"Warning: Could not load model config: {e}")
        
        return default_models
    
    def _load_routing_rules(self) -> Dict:
        """Load routing rules for different scenarios."""
        return {
            "task_preferences": {
                "simple": ["budget"],
                "complex": ["standard", "premium"], 
                "mobile": ["budget", "standard"],
                "batch": ["budget", "standard"],
                "analysis": ["budget", "standard"],
                "think_harder": ["premium"]
            },
            "cost_thresholds": {
                "budget": 0.001,    # Max $0.001 per operation
                "standard": 0.01,   # Max $0.01 per operation
                "premium": 0.1      # Max $0.10 per operation
            },
            "fallback_order": ["budget", "standard", "premium"],
            "availability_timeout": 5.0,  # Seconds to wait for model
            "retry_attempts": 3
        }
    
    def route_request(self, task_classification, budget_limit: Optional[float] = None,
                     strategy: RoutingStrategy = RoutingStrategy.COST_OPTIMIZED, think_harder: bool = False) -> RoutingDecision:
        """
        Main routing function implementing Agent-OS cost optimization.
        
        Args:
            task_classification: TaskClassification from task classifier
            budget_limit: Maximum budget for this operation (USD)
            strategy: Routing strategy to use
            
        Returns:
            RoutingDecision with selected model and routing metadata
        """
        
        task_type = task_classification.task_type.value
        if think_harder:
            task_type = "think_harder"
        complexity = task_classification.complexity.value
        estimated_tokens = self._estimate_tokens(task_classification)
        
        # Get preferred model tiers for this task
        preferred_tiers = self.routing_rules["task_preferences"].get(task_type, ["budget"])
        
        # Filter models by preference and availability
        candidate_models = self._get_candidate_models(preferred_tiers, estimated_tokens)
        
        # Apply routing strategy
        if strategy == RoutingStrategy.COST_OPTIMIZED:
            selected_model = self._select_cost_optimized(candidate_models, estimated_tokens, budget_limit)
        elif strategy == RoutingStrategy.PERFORMANCE_OPTIMIZED:
            selected_model = self._select_performance_optimized(candidate_models, task_type)
        elif strategy == RoutingStrategy.BALANCED:
            selected_model = self._select_balanced(candidate_models, estimated_tokens, task_type)
        else:  # FALLBACK
            selected_model = self._select_fallback(candidate_models)
        
        if not selected_model:
            # Emergency fallback
            selected_model = self._emergency_fallback()
        
        # Calculate final routing decision
        model_config = self.model_configs[selected_model]
        estimated_cost = estimated_tokens * model_config.cost_per_token
        
        # Generate reasoning
        reasoning = self._generate_routing_reasoning(
            selected_model, task_type, complexity, strategy, estimated_cost
        )
        
        # Prepare fallback options
        fallback_models = [m for m in candidate_models if m != selected_model][:3]
        
        # Track optimization applied
        optimization_applied = {
            "context_optimization": task_classification.context_optimization,
            "model_tier_optimization": model_config.tier.value,
            "cost_vs_baseline": self._calculate_cost_vs_baseline(estimated_cost, task_type)
        }
        
        decision = RoutingDecision(
            selected_model=selected_model,
            provider=model_config.provider,
            tier=model_config.tier,
            strategy_used=strategy,
            estimated_cost=estimated_cost,
            reasoning=reasoning,
            fallback_models=fallback_models,
            optimization_applied=optimization_applied
        )
        
        # Track routing for learning
        self.routing_history.append(decision)
        
        return decision
    
    def _estimate_tokens(self, task_classification) -> int:
        """Estimate token usage for routing decisions."""
        base_tokens = 100  # Minimum for any request
        
        # Add tokens based on complexity
        complexity_multipliers = {"low": 1.0, "medium": 2.5, "high": 5.0}
        complexity_factor = complexity_multipliers.get(task_classification.complexity.value, 1.0)
        
        # Add tokens based on task type
        task_base_tokens = {
            "simple": 200,
            "complex": 1000,
            "mobile": 300,
            "batch": 800,
            "analysis": 500
        }
        
        task_tokens = task_base_tokens.get(task_classification.task_type.value, 200)
        
        # Consider context optimization
        context_tokens = 0
        if task_classification.context_optimization:
            context_tokens = task_classification.context_optimization.get("optimized_tokens", 0)
        
        total_estimated = int(base_tokens + (task_tokens * complexity_factor) + context_tokens)
        
        return total_estimated
    
    def _get_candidate_models(self, preferred_tiers: List[str], estimated_tokens: int) -> List[str]:
        """Get candidate models filtered by preferences and constraints."""
        candidates = []
        
        for model_id, config in self.model_configs.items():
            # Check tier preference
            if config.tier.value not in preferred_tiers:
                continue
                
            # Check availability
            if not config.availability:
                continue
                
            # Check token limit
            if estimated_tokens > config.max_tokens:
                continue
                
            candidates.append(model_id)
        
        return candidates
    
    def _select_cost_optimized(self, candidates: List[str], estimated_tokens: int, 
                             budget_limit: Optional[float]) -> Optional[str]:
        """Select model optimized for minimum cost."""
        if not candidates:
            return None
            
        # Calculate cost for each candidate
        costs = []
        for model_id in candidates:
            config = self.model_configs[model_id]
            cost = estimated_tokens * config.cost_per_token
            
            # Skip if over budget
            if budget_limit and cost > budget_limit:
                continue
                
            costs.append((cost, model_id))
        
        if not costs:
            return None
            
        # Return cheapest option
        costs.sort()
        return costs[0][1]
    
    def _select_performance_optimized(self, candidates: List[str], task_type: str) -> Optional[str]:
        """Select model optimized for best performance."""
        if not candidates:
            return None
            
        # Score models based on task suitability
        scores = []
        for model_id in candidates:
            config = self.model_configs[model_id]
            
            # Base score from tier (higher tier = better performance)
            tier_scores = {ModelTier.BUDGET: 1, ModelTier.STANDARD: 2, ModelTier.PREMIUM: 3}
            score = tier_scores[config.tier]
            
            # Bonus for task specialization
            if task_type in config.best_for_tasks:
                score += 2
                
            # Bonus for relevant strengths
            task_strengths = {
                "simple": ["speed", "cost"],
                "complex": ["reasoning", "code", "advanced_reasoning"],
                "mobile": ["speed", "general_purpose"],
                "batch": ["speed", "ultra_low_cost"],
                "analysis": ["reasoning", "advanced_reasoning"]
            }
            
            relevant_strengths = task_strengths.get(task_type, [])
            for strength in config.strengths:
                if strength in relevant_strengths:
                    score += 1
                    
            scores.append((score, model_id))
        
        # Return highest scoring model
        scores.sort(reverse=True)
        return scores[0][1]
    
    def _select_balanced(self, candidates: List[str], estimated_tokens: int, task_type: str) -> Optional[str]:
        """Select model with best cost/performance balance."""
        if not candidates:
            return None
            
        # Calculate cost-performance score
        scores = []
        for model_id in candidates:
            config = self.model_configs[model_id]
            cost = estimated_tokens * config.cost_per_token
            
            # Performance score (reuse from performance_optimized)
            tier_scores = {ModelTier.BUDGET: 1, ModelTier.STANDARD: 2, ModelTier.PREMIUM: 3}
            perf_score = tier_scores[config.tier]
            
            if task_type in config.best_for_tasks:
                perf_score += 1
                
            # Cost efficiency score (inverse of cost, normalized)
            max_cost = max(estimated_tokens * c.cost_per_token for c in self.model_configs.values())
            cost_efficiency = 1.0 - (cost / max_cost) if max_cost > 0 else 1.0
            
            # Balanced score (weight performance and cost equally)
            balanced_score = (perf_score / 5.0) * 0.5 + cost_efficiency * 0.5
            
            scores.append((balanced_score, model_id))
        
        # Return best balanced option
        scores.sort(reverse=True) 
        return scores[0][1]
    
    def _select_fallback(self, candidates: List[str]) -> Optional[str]:
        """Select fallback model (typically cheapest available)."""
        if not candidates:
            return None
        return candidates[0]  # Return first available
    
    def _emergency_fallback(self) -> str:
        """Emergency fallback when no candidates available."""
        # Return cheapest available model
        available_models = [
            model_id for model_id, config in self.model_configs.items() 
            if config.availability
        ]
        
        if available_models:
            costs = [
                (self.model_configs[m].cost_per_token, m) 
                for m in available_models
            ]
            costs.sort()
            return costs[0][1]
        
        # Ultimate fallback
        return "openrouter/meta-llama/llama-3.1-8b-instruct"
    
    def _generate_routing_reasoning(self, selected_model: str, task_type: str, 
                                  complexity: str, strategy: RoutingStrategy, 
                                  estimated_cost: float) -> str:
        """Generate human-readable reasoning for routing decision."""
        config = self.model_configs[selected_model]
        
        reasoning = f"Selected {config.name} ({config.tier.value} tier) for {task_type} task. "
        
        if strategy == RoutingStrategy.COST_OPTIMIZED:
            reasoning += f"Cost-optimized routing: ${estimated_cost:.6f} estimated. "
        elif strategy == RoutingStrategy.PERFORMANCE_OPTIMIZED:
            reasoning += "Performance-optimized for best results. "
        elif strategy == RoutingStrategy.BALANCED:
            reasoning += "Balanced cost/performance selection. "
        
        if task_type in config.best_for_tasks:
            reasoning += f"Model specialized for {task_type} tasks. "
            
        if complexity == "low" and config.tier == ModelTier.BUDGET:
            reasoning += "Budget model sufficient for low complexity. "
        elif complexity == "high" and config.tier in [ModelTier.STANDARD, ModelTier.PREMIUM]:
            reasoning += "Higher tier model for complex requirements. "
        
        return reasoning
    
    def _calculate_cost_vs_baseline(self, estimated_cost: float, task_type: str) -> Dict:
        """Calculate cost comparison vs baseline expensive model."""
        # Use most expensive model as baseline
        baseline_model = max(
            self.model_configs.values(),
            key=lambda c: c.cost_per_token
        )
        baseline_cost = estimated_cost / self.model_configs[list(self.model_configs.keys())[0]].cost_per_token * baseline_model.cost_per_token
        
        savings = baseline_cost - estimated_cost
        savings_percent = (savings / baseline_cost * 100) if baseline_cost > 0 else 0
        
        return {
            "baseline_cost": baseline_cost,
            "selected_cost": estimated_cost,
            "savings": savings,
            "savings_percent": savings_percent
        }
    
    def get_routing_stats(self) -> Dict:
        """Get routing performance statistics."""
        if not self.routing_history:
            return {"message": "No routing decisions made yet"}
        
        total_decisions = len(self.routing_history)
        
        # Tier usage
        tier_usage = {}
        strategy_usage = {}
        total_estimated_cost = 0
        
        for decision in self.routing_history:
            tier = decision.tier.value
            tier_usage[tier] = tier_usage.get(tier, 0) + 1
            
            strategy = decision.strategy_used.value
            strategy_usage[strategy] = strategy_usage.get(strategy, 0) + 1
            
            total_estimated_cost += decision.estimated_cost
        
        # Calculate cost savings
        total_cost_savings = sum(
            decision.optimization_applied.get("cost_vs_baseline", {}).get("savings", 0)
            for decision in self.routing_history
        )
        
        return {
            "total_routing_decisions": total_decisions,
            "tier_usage": tier_usage,
            "strategy_usage": strategy_usage,
            "total_estimated_cost": total_estimated_cost,
            "total_cost_savings": total_cost_savings,
            "avg_cost_per_decision": total_estimated_cost / total_decisions,
            "models_used": list(set(d.selected_model for d in self.routing_history))
        }

def quick_route(task_classification, budget_limit: Optional[float] = None) -> RoutingDecision:
    """Quick routing function for CLI integration."""
    router = LiteLLMRouter()
    return router.route_request(task_classification, budget_limit)

if __name__ == "__main__":
    # Test routing with different scenarios
    from types import SimpleNamespace
    
    # Mock task classifications for testing
    simple_task = SimpleNamespace(
        task_type=SimpleNamespace(value="simple"),
        complexity=SimpleNamespace(value="low"),
        context_optimization={"optimized_tokens": 100, "tokens_saved": 50}
    )
    
    complex_task = SimpleNamespace(
        task_type=SimpleNamespace(value="complex"),
        complexity=SimpleNamespace(value="high"),
        context_optimization={"optimized_tokens": 5000, "tokens_saved": 1000}
    )
    
    router = LiteLLMRouter()
    
    print("=== LiteLLM Router Testing ===")
    
    # Test simple task routing
    print("\n--- Simple Task Routing ---")
    decision = router.route_request(simple_task, budget_limit=0.001)
    print(f"Model: {decision.selected_model}")
    print(f"Tier: {decision.tier.value}")
    print(f"Cost: ${decision.estimated_cost:.6f}")
    print(f"Reasoning: {decision.reasoning}")
    
    # Test complex task routing  
    print("\n--- Complex Task Routing ---")
    decision = router.route_request(complex_task, budget_limit=0.01)
    print(f"Model: {decision.selected_model}")
    print(f"Tier: {decision.tier.value}")
    print(f"Cost: ${decision.estimated_cost:.6f}")
    print(f"Reasoning: {decision.reasoning}")
    
    # Show routing stats
    print("\n--- Routing Statistics ---")
    stats = router.get_routing_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")