#!/usr/bin/env python3
"""
Advanced Cost Estimation Engine for Agent-OS Intelligence
Implements predictive cost modeling with task-specific learning and budget optimization.
"""

import json
import math
import statistics
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import time

class CostCategory(Enum):
    MODEL_INFERENCE = "model_inference"      # LLM API costs
    EXECUTION_TIME = "execution_time"        # Compute time costs
    CONTEXT_TOKENS = "context_tokens"        # Input token costs
    OUTPUT_TOKENS = "output_tokens"          # Output token costs
    STORAGE_OPERATIONS = "storage_ops"       # File/data operations
    NETWORK_CALLS = "network_calls"          # API/network costs
    RETRY_OVERHEAD = "retry_overhead"        # Failed execution costs

@dataclass
class CostBreakdown:
    category: CostCategory
    cost: float
    confidence: float
    explanation: str
    optimization_potential: float

@dataclass
class CostEstimate:
    total_cost: float
    cost_breakdown: List[CostBreakdown]
    confidence_level: float
    variance_range: Tuple[float, float]  # (min, max) estimate
    optimization_suggestions: List[str]
    budget_impact: Dict[str, float]

@dataclass
class ExecutionCostRecord:
    prompt: str
    task_type: str
    complexity: float
    estimated_cost: float
    actual_cost: float
    execution_time: float
    tokens_input: int
    tokens_output: int
    model_used: str
    success: bool
    timestamp: float
    cost_breakdown: Dict[str, float]

class CostEstimationEngine:
    """
    Agent-OS Intelligence: Advanced cost estimation with predictive modeling.
    
    Features:
    - Task-specific cost modeling with historical learning
    - Multi-dimensional cost breakdown (model, time, tokens, storage, network)
    - Predictive cost variance and confidence intervals
    - Budget impact analysis and optimization recommendations
    - Real-time cost tracking and model refinement
    - Cost-aware task routing recommendations
    """
    
    def __init__(self, cost_history_file: Optional[str] = None):
        self.cost_history_file = cost_history_file or Path(__file__).parent / "cost-history.json"
        self.cost_records: List[ExecutionCostRecord] = self._load_cost_history()
        self.cost_models = self._initialize_cost_models()
        self.pricing_data = self._load_pricing_data()
        
    def _load_cost_history(self) -> List[ExecutionCostRecord]:
        """Load historical cost data for learning."""
        if not self.cost_history_file.exists():
            return []
        
        try:
            with open(self.cost_history_file) as f:
                data = json.load(f)
                return [
                    ExecutionCostRecord(**record) for record in data.get("cost_records", [])
                ]
        except:
            return []
    
    def _save_cost_history(self):
        """Save cost history for persistence."""
        self.cost_history_file.parent.mkdir(exist_ok=True)
        with open(self.cost_history_file, 'w') as f:
            json.dump({
                "cost_records": [asdict(record) for record in self.cost_records],
                "cost_models": self.cost_models,
                "last_updated": time.time()
            }, f, indent=2)
    
    def _initialize_cost_models(self) -> Dict:
        """Initialize cost models for different task types."""
        return {
            "simple": {
                "base_cost": 0.001,
                "complexity_multiplier": 1.2,
                "time_factor": 0.0001,
                "token_factor": 0.000001,
                "confidence": 0.8
            },
            "complex": {
                "base_cost": 0.01,
                "complexity_multiplier": 2.5,
                "time_factor": 0.0005,
                "token_factor": 0.000003,
                "confidence": 0.6
            },
            "mobile": {
                "base_cost": 0.002,
                "complexity_multiplier": 1.5,
                "time_factor": 0.0002,
                "token_factor": 0.000001,
                "confidence": 0.7
            },
            "batch": {
                "base_cost": 0.005,
                "complexity_multiplier": 3.0,
                "time_factor": 0.0008,
                "token_factor": 0.000002,
                "confidence": 0.5
            },
            "analysis": {
                "base_cost": 0.003,
                "complexity_multiplier": 1.8,
                "time_factor": 0.0003,
                "token_factor": 0.000002,
                "confidence": 0.7
            }
        }
    
    def _load_pricing_data(self) -> Dict:
        """Load current model pricing data."""
        return {
            "models": {
                "openrouter/meta-llama/llama-3.1-8b-instruct": {
                    "input_cost_per_token": 0.0000001,  # $0.10/1M tokens
                    "output_cost_per_token": 0.0000001,
                    "tier": "budget"
                },
                "openrouter/anthropic/claude-3-haiku": {
                    "input_cost_per_token": 0.00000025,  # $0.25/1M tokens
                    "output_cost_per_token": 0.00000125,  # $1.25/1M tokens
                    "tier": "budget"
                },
                "openrouter/openai/gpt-4o-mini": {
                    "input_cost_per_token": 0.00000015,  # $0.15/1M tokens
                    "output_cost_per_token": 0.0000006,   # $0.60/1M tokens
                    "tier": "standard"
                },
                "openrouter/anthropic/claude-3-sonnet": {
                    "input_cost_per_token": 0.000003,     # $3/1M tokens
                    "output_cost_per_token": 0.000015,    # $15/1M tokens
                    "tier": "standard"
                },
                "openrouter/openai/gpt-4": {
                    "input_cost_per_token": 0.00003,      # $30/1M tokens
                    "output_cost_per_token": 0.00006,     # $60/1M tokens
                    "tier": "premium"
                }
            },
            "execution_costs": {
                "opencode_base": 0.0001,  # Base execution cost per second
                "safety_checks": 0.00001,  # Cost per safety check
                "file_operations": 0.000001,  # Cost per file operation
                "network_calls": 0.00001   # Cost per network call
            }
        }
    
    def estimate_cost(self, task_type: str, complexity: float, context: Optional[Dict] = None,
                     routing_decision: Optional[Dict] = None) -> CostEstimate:
        """
        Generate comprehensive cost estimate with breakdown and optimization suggestions.
        
        Args:
            task_type: Type of task (simple, complex, mobile, batch, analysis)
            complexity: Complexity score (0.0-1.0)
            context: Additional context (file_count, session_data, etc.)
            routing_decision: LiteLLM routing decision with model selection
            
        Returns:
            CostEstimate with detailed breakdown and recommendations
        """
        context = context or {}
        
        # Get base cost model for task type
        base_model = self.cost_models.get(task_type, self.cost_models["simple"])
        
        # Calculate cost breakdown by category
        cost_breakdown = []
        
        # 1. Model Inference Costs
        model_cost = self._estimate_model_cost(routing_decision, complexity, context)
        cost_breakdown.append(model_cost)
        
        # 2. Execution Time Costs
        execution_cost = self._estimate_execution_cost(task_type, complexity, context)
        cost_breakdown.append(execution_cost)
        
        # 3. Context Token Costs
        context_cost = self._estimate_context_cost(context, routing_decision)
        cost_breakdown.append(context_cost)
        
        # 4. Output Token Costs
        output_cost = self._estimate_output_cost(task_type, complexity, routing_decision)
        cost_breakdown.append(output_cost)
        
        # 5. Storage Operation Costs
        storage_cost = self._estimate_storage_cost(task_type, context)
        cost_breakdown.append(storage_cost)
        
        # 6. Network Call Costs
        network_cost = self._estimate_network_cost(task_type, context)
        cost_breakdown.append(network_cost)
        
        # 7. Retry Overhead Costs
        retry_cost = self._estimate_retry_cost(complexity, task_type)
        cost_breakdown.append(retry_cost)
        
        # Calculate total cost
        total_cost = sum(cb.cost for cb in cost_breakdown)
        
        # Apply historical learning adjustment
        adjusted_cost, confidence = self._apply_historical_learning(
            task_type, complexity, total_cost, context
        )
        
        # Calculate variance range
        variance = self._calculate_cost_variance(task_type, complexity)
        variance_range = (adjusted_cost * (1 - variance), adjusted_cost * (1 + variance))
        
        # Generate optimization suggestions
        optimization_suggestions = self._generate_optimization_suggestions(
            cost_breakdown, task_type, complexity, context
        )
        
        # Calculate budget impact
        budget_impact = self._calculate_budget_impact(adjusted_cost, context)
        
        return CostEstimate(
            total_cost=adjusted_cost,
            cost_breakdown=cost_breakdown,
            confidence_level=confidence,
            variance_range=variance_range,
            optimization_suggestions=optimization_suggestions,
            budget_impact=budget_impact
        )
    
    def _estimate_model_cost(self, routing_decision: Optional[Dict], complexity: float, 
                           context: Dict) -> CostBreakdown:
        """Estimate model inference costs."""
        if not routing_decision:
            base_cost = 0.001 * (1 + complexity)
            return CostBreakdown(
                category=CostCategory.MODEL_INFERENCE,
                cost=base_cost,
                confidence=0.5,
                explanation="No routing decision - using default estimate",
                optimization_potential=0.3
            )
        
        model_name = routing_decision.get("selected_model", "")
        pricing = self.pricing_data["models"].get(model_name, {})
        
        if not pricing:
            base_cost = 0.001 * (1 + complexity)
            return CostBreakdown(
                category=CostCategory.MODEL_INFERENCE,
                cost=base_cost,
                confidence=0.4,
                explanation=f"Unknown model pricing: {model_name}",
                optimization_potential=0.5
            )
        
        # Estimate token usage based on complexity and context
        estimated_input_tokens = self._estimate_input_tokens(complexity, context)
        estimated_output_tokens = self._estimate_output_tokens(complexity, context)
        
        input_cost = estimated_input_tokens * pricing["input_cost_per_token"]
        output_cost = estimated_output_tokens * pricing["output_cost_per_token"]
        total_model_cost = input_cost + output_cost
        
        # Optimization potential based on model tier
        tier = pricing.get("tier", "standard")
        optimization_potential = {
            "budget": 0.1,
            "standard": 0.3,
            "premium": 0.7
        }.get(tier, 0.3)
        
        return CostBreakdown(
            category=CostCategory.MODEL_INFERENCE,
            cost=total_model_cost,
            confidence=0.8,
            explanation=f"Model: {model_name}, Tokens: {estimated_input_tokens}+{estimated_output_tokens}",
            optimization_potential=optimization_potential
        )
    
    def _estimate_execution_cost(self, task_type: str, complexity: float, context: Dict) -> CostBreakdown:
        """Estimate execution time-based costs."""
        base_time = {
            "simple": 5.0,
            "complex": 30.0,
            "mobile": 10.0,
            "batch": 60.0,
            "analysis": 15.0
        }.get(task_type, 10.0)
        
        complexity_multiplier = 1 + (complexity * 2)
        estimated_time = base_time * complexity_multiplier
        
        execution_cost = estimated_time * self.pricing_data["execution_costs"]["opencode_base"]
        
        optimization_potential = 0.4 if complexity > 0.6 else 0.2
        
        return CostBreakdown(
            category=CostCategory.EXECUTION_TIME,
            cost=execution_cost,
            confidence=0.7,
            explanation=f"Estimated execution time: {estimated_time:.1f}s",
            optimization_potential=optimization_potential
        )
    
    def _estimate_context_cost(self, context: Dict, routing_decision: Optional[Dict]) -> CostBreakdown:
        """Estimate context token costs."""
        context_tokens = context.get("context_tokens", 500)  # Default estimate
        
        if routing_decision and "selected_model" in routing_decision:
            model_name = routing_decision["selected_model"]
            pricing = self.pricing_data["models"].get(model_name, {})
            token_cost = pricing.get("input_cost_per_token", 0.000001)
        else:
            token_cost = 0.000001  # Default
        
        cost = context_tokens * token_cost
        
        # Optimization potential based on context size
        optimization_potential = min(0.8, context_tokens / 1000)  # Higher for larger contexts
        
        return CostBreakdown(
            category=CostCategory.CONTEXT_TOKENS,
            cost=cost,
            confidence=0.9,
            explanation=f"Context tokens: {context_tokens}",
            optimization_potential=optimization_potential
        )
    
    def _estimate_output_cost(self, task_type: str, complexity: float, 
                            routing_decision: Optional[Dict]) -> CostBreakdown:
        """Estimate output token costs."""
        base_output_tokens = {
            "simple": 50,
            "complex": 300,
            "mobile": 100,
            "batch": 200,
            "analysis": 400
        }.get(task_type, 100)
        
        estimated_output = base_output_tokens * (1 + complexity)
        
        if routing_decision and "selected_model" in routing_decision:
            model_name = routing_decision["selected_model"]
            pricing = self.pricing_data["models"].get(model_name, {})
            token_cost = pricing.get("output_cost_per_token", 0.000002)
        else:
            token_cost = 0.000002  # Default
        
        cost = estimated_output * token_cost
        
        return CostBreakdown(
            category=CostCategory.OUTPUT_TOKENS,
            cost=cost,
            confidence=0.8,
            explanation=f"Estimated output tokens: {int(estimated_output)}",
            optimization_potential=0.2
        )
    
    def _estimate_storage_cost(self, task_type: str, context: Dict) -> CostBreakdown:
        """Estimate storage operation costs."""
        file_count = context.get("file_count", 1)
        operations_per_file = {
            "simple": 2,    # Read, write
            "complex": 5,   # Multiple operations
            "mobile": 3,    # Read, modify, write
            "batch": 8,     # Bulk operations
            "analysis": 3   # Read, analyze, report
        }.get(task_type, 3)
        
        total_operations = file_count * operations_per_file
        cost = total_operations * self.pricing_data["execution_costs"]["file_operations"]
        
        optimization_potential = 0.3 if file_count > 5 else 0.1
        
        return CostBreakdown(
            category=CostCategory.STORAGE_OPERATIONS,
            cost=cost,
            confidence=0.9,
            explanation=f"File operations: {total_operations} ({file_count} files)",
            optimization_potential=optimization_potential
        )
    
    def _estimate_network_cost(self, task_type: str, context: Dict) -> CostBreakdown:
        """Estimate network call costs."""
        api_calls = {
            "simple": 1,
            "complex": 3,
            "mobile": 2,    # May involve API calls
            "batch": 5,
            "analysis": 2
        }.get(task_type, 2)
        
        cost = api_calls * self.pricing_data["execution_costs"]["network_calls"]
        
        return CostBreakdown(
            category=CostCategory.NETWORK_CALLS,
            cost=cost,
            confidence=0.8,
            explanation=f"Estimated API calls: {api_calls}",
            optimization_potential=0.2
        )
    
    def _estimate_retry_cost(self, complexity: float, task_type: str) -> CostBreakdown:
        """Estimate retry overhead costs."""
        # Higher complexity = higher chance of retries
        retry_probability = complexity * 0.3  # Max 30% chance
        retry_cost_multiplier = 1.5  # Retries cost 1.5x original
        
        base_cost = 0.001  # Base retry cost
        expected_retry_cost = base_cost * retry_probability * retry_cost_multiplier
        
        optimization_potential = retry_probability  # Can optimize by reducing failures
        
        return CostBreakdown(
            category=CostCategory.RETRY_OVERHEAD,
            cost=expected_retry_cost,
            confidence=0.6,
            explanation=f"Retry probability: {retry_probability:.1%}",
            optimization_potential=optimization_potential
        )
    
    def _estimate_input_tokens(self, complexity: float, context: Dict) -> int:
        """Estimate input token count."""
        base_tokens = 200
        complexity_tokens = int(complexity * 500)
        context_tokens = context.get("context_tokens", 300)
        return base_tokens + complexity_tokens + context_tokens
    
    def _estimate_output_tokens(self, complexity: float, context: Dict) -> int:
        """Estimate output token count."""
        base_tokens = 100
        complexity_tokens = int(complexity * 300)
        return base_tokens + complexity_tokens
    
    def _apply_historical_learning(self, task_type: str, complexity: float, 
                                 estimated_cost: float, context: Dict) -> Tuple[float, float]:
        """Apply historical learning to adjust cost estimate."""
        if not self.cost_records:
            return estimated_cost, 0.5
        
        # Find similar historical executions
        similar_records = []
        for record in self.cost_records:
            if (record.task_type == task_type and 
                abs(record.complexity - complexity) < 0.2):
                similar_records.append(record)
        
        if not similar_records:
            return estimated_cost, 0.5
        
        # Calculate accuracy of previous estimates
        accuracies = []
        adjustments = []
        
        for record in similar_records:
            if record.estimated_cost > 0:
                accuracy = 1 - abs(record.actual_cost - record.estimated_cost) / record.estimated_cost
                accuracies.append(max(0, accuracy))
                
                if record.estimated_cost > 0:
                    adjustment = record.actual_cost / record.estimated_cost
                    adjustments.append(adjustment)
        
        if adjustments:
            # Apply median adjustment to avoid outliers
            median_adjustment = statistics.median(adjustments)
            adjusted_cost = estimated_cost * median_adjustment
            
            # Confidence based on historical accuracy
            confidence = statistics.mean(accuracies) if accuracies else 0.5
            
            return adjusted_cost, confidence
        
        return estimated_cost, 0.5
    
    def _calculate_cost_variance(self, task_type: str, complexity: float) -> float:
        """Calculate expected cost variance for uncertainty range."""
        base_variance = {
            "simple": 0.2,      # ±20%
            "complex": 0.4,     # ±40%
            "mobile": 0.3,      # ±30%
            "batch": 0.5,       # ±50%
            "analysis": 0.3     # ±30%
        }.get(task_type, 0.3)
        
        # Higher complexity = higher variance
        complexity_variance = complexity * 0.2
        
        return base_variance + complexity_variance
    
    def _generate_optimization_suggestions(self, cost_breakdown: List[CostBreakdown],
                                         task_type: str, complexity: float, 
                                         context: Dict) -> List[str]:
        """Generate cost optimization suggestions."""
        suggestions = []
        
        # Find highest cost categories
        sorted_costs = sorted(cost_breakdown, key=lambda x: x.cost, reverse=True)
        top_cost_categories = sorted_costs[:3]
        
        for breakdown in top_cost_categories:
            if breakdown.optimization_potential > 0.3:
                if breakdown.category == CostCategory.MODEL_INFERENCE:
                    suggestions.append("Consider using a budget-tier model for this task type")
                elif breakdown.category == CostCategory.CONTEXT_TOKENS:
                    suggestions.append("Enable context optimization to reduce input tokens")
                elif breakdown.category == CostCategory.EXECUTION_TIME:
                    suggestions.append("Break complex tasks into simpler subtasks")
                elif breakdown.category == CostCategory.RETRY_OVERHEAD:
                    suggestions.append("Improve task reliability to reduce retry costs")
                elif breakdown.category == CostCategory.STORAGE_OPERATIONS:
                    suggestions.append("Optimize file operations and reduce I/O")
        
        # Task-specific suggestions
        if task_type == "batch" and complexity > 0.6:
            suggestions.append("Consider parallel processing to reduce execution time")
        elif task_type == "complex" and context.get("file_count", 0) > 10:
            suggestions.append("Use incremental processing for large file sets")
        
        return suggestions[:5]  # Limit to top 5 suggestions
    
    def _calculate_budget_impact(self, estimated_cost: float, context: Dict) -> Dict[str, float]:
        """Calculate impact on daily/hourly budgets."""
        daily_budget = context.get("daily_budget", 5.0)
        hourly_budget = context.get("hourly_budget", 1.25)
        
        return {
            "daily_budget_percentage": (estimated_cost / daily_budget) * 100,
            "hourly_budget_percentage": (estimated_cost / hourly_budget) * 100,
            "budget_efficiency": min(100, (1 / max(estimated_cost, 0.001)) * 10),  # Efficiency score
            "cost_per_operation": estimated_cost
        }
    
    def record_actual_cost(self, prompt: str, task_type: str, complexity: float,
                          estimated_cost: float, actual_cost: float, execution_time: float,
                          tokens_input: int, tokens_output: int, model_used: str,
                          success: bool, cost_breakdown: Dict[str, float] = None):
        """Record actual execution costs for learning."""
        record = ExecutionCostRecord(
            prompt=prompt,
            task_type=task_type,
            complexity=complexity,
            estimated_cost=estimated_cost,
            actual_cost=actual_cost,
            execution_time=execution_time,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            model_used=model_used,
            success=success,
            timestamp=time.time(),
            cost_breakdown=cost_breakdown or {}
        )
        
        self.cost_records.append(record)
        
        # Keep only recent records (last 2000)
        if len(self.cost_records) > 2000:
            self.cost_records = self.cost_records[-2000:]
        
        # Update cost models based on performance
        self._update_cost_models(record)
        
        # Save updated records
        self._save_cost_history()
    
    def _update_cost_models(self, record: ExecutionCostRecord):
        """Update cost models based on actual performance."""
        task_model = self.cost_models.get(record.task_type)
        if not task_model:
            return
        
        # Calculate prediction accuracy
        if record.estimated_cost > 0:
            accuracy = 1 - abs(record.actual_cost - record.estimated_cost) / record.estimated_cost
            
            # Adjust model parameters based on accuracy
            if accuracy < 0.7:  # Poor accuracy
                # Slightly increase base cost if we're underestimating
                if record.actual_cost > record.estimated_cost:
                    task_model["base_cost"] *= 1.02
                else:
                    task_model["base_cost"] *= 0.98
                
                # Reduce confidence
                task_model["confidence"] *= 0.99
            elif accuracy > 0.9:  # Good accuracy
                # Increase confidence
                task_model["confidence"] = min(0.95, task_model["confidence"] * 1.01)
    
    def get_cost_analytics(self) -> Dict:
        """Get cost analysis and prediction performance statistics."""
        if not self.cost_records:
            return {"message": "No cost records available"}
        
        total_records = len(self.cost_records)
        
        # Calculate prediction accuracy
        accurate_predictions = 0
        total_estimated = 0
        total_actual = 0
        
        for record in self.cost_records:
            if record.estimated_cost > 0:
                accuracy = 1 - abs(record.actual_cost - record.estimated_cost) / record.estimated_cost
                if accuracy > 0.8:  # Within 20% accuracy
                    accurate_predictions += 1
                
                total_estimated += record.estimated_cost
                total_actual += record.actual_cost
        
        prediction_accuracy = accurate_predictions / total_records if total_records > 0 else 0
        
        # Task type breakdown
        task_breakdown = defaultdict(list)
        for record in self.cost_records:
            task_breakdown[record.task_type].append(record.actual_cost)
        
        avg_costs_by_task = {
            task: statistics.mean(costs) for task, costs in task_breakdown.items()
        }
        
        # Model performance
        model_performance = defaultdict(list)
        for record in self.cost_records:
            if record.estimated_cost > 0:
                accuracy = 1 - abs(record.actual_cost - record.estimated_cost) / record.estimated_cost
                model_performance[record.model_used].append(accuracy)
        
        avg_model_accuracy = {
            model: statistics.mean(accuracies) for model, accuracies in model_performance.items()
        }
        
        return {
            "total_cost_records": total_records,
            "prediction_accuracy": prediction_accuracy,
            "total_estimated_cost": total_estimated,
            "total_actual_cost": total_actual,
            "cost_efficiency": total_estimated / max(total_actual, 0.001),
            "avg_costs_by_task": avg_costs_by_task,
            "model_accuracy": avg_model_accuracy,
            "cost_models_confidence": {task: model["confidence"] for task, model in self.cost_models.items()}
        }
    
    def optimize_budget_allocation(self, daily_budget: float, task_distribution: Dict[str, int]) -> Dict:
        """Optimize budget allocation across different task types."""
        total_tasks = sum(task_distribution.values())
        if total_tasks == 0:
            return {"error": "No tasks provided"}
        
        # Estimate costs for each task type
        task_costs = {}
        total_estimated_cost = 0
        
        for task_type, count in task_distribution.items():
            avg_complexity = 0.5  # Assume medium complexity
            estimate = self.estimate_cost(task_type, avg_complexity)
            task_cost = estimate.total_cost * count
            task_costs[task_type] = task_cost
            total_estimated_cost += task_cost
        
        # Calculate budget allocation
        if total_estimated_cost <= daily_budget:
            # Budget sufficient
            allocation = {
                task_type: (cost / total_estimated_cost) * daily_budget 
                for task_type, cost in task_costs.items()
            }
            optimization_status = "optimal"
        else:
            # Budget insufficient - prioritize tasks
            task_priorities = {
                "simple": 1.0,
                "mobile": 0.9,
                "analysis": 0.8,
                "complex": 0.7,
                "batch": 0.6
            }
            
            # Allocate budget based on priority
            remaining_budget = daily_budget
            allocation = {}
            
            sorted_tasks = sorted(task_costs.items(), 
                                key=lambda x: task_priorities.get(x[0], 0.5), 
                                reverse=True)
            
            for task_type, cost in sorted_tasks:
                if remaining_budget >= cost:
                    allocation[task_type] = cost
                    remaining_budget -= cost
                else:
                    allocation[task_type] = remaining_budget
                    remaining_budget = 0
                    
            optimization_status = "budget_constrained"
        
        return {
            "optimization_status": optimization_status,
            "budget_allocation": allocation,
            "estimated_costs": task_costs,
            "total_estimated_cost": total_estimated_cost,
            "budget_utilization": min(100, (total_estimated_cost / daily_budget) * 100),
            "recommendations": self._generate_budget_recommendations(
                task_distribution, task_costs, daily_budget
            )
        }
    
    def _generate_budget_recommendations(self, task_distribution: Dict[str, int],
                                       task_costs: Dict[str, float], 
                                       daily_budget: float) -> List[str]:
        """Generate budget optimization recommendations."""
        recommendations = []
        
        total_cost = sum(task_costs.values())
        
        if total_cost > daily_budget * 1.2:
            recommendations.append("Consider reducing complex task volume or breaking into simpler tasks")
        
        # Find most expensive task types
        if task_costs:
            most_expensive = max(task_costs.items(), key=lambda x: x[1])
            if most_expensive[1] > daily_budget * 0.5:
                recommendations.append(f"Task type '{most_expensive[0]}' consumes >50% of budget - consider optimization")
        
        # Efficiency recommendations
        simple_tasks = task_distribution.get("simple", 0)
        complex_tasks = task_distribution.get("complex", 0)
        
        if complex_tasks > simple_tasks:
            recommendations.append("High complex-to-simple task ratio - consider task simplification")
        
        return recommendations

def quick_estimate_cost(task_type: str, complexity: float, context: Optional[Dict] = None,
                       routing_decision: Optional[Dict] = None) -> CostEstimate:
    """Quick cost estimation function for CLI integration."""
    engine = CostEstimationEngine()
    return engine.estimate_cost(task_type, complexity, context, routing_decision)

if __name__ == "__main__":
    # Test cost estimation engine
    engine = CostEstimationEngine()
    
    test_scenarios = [
        {
            "task_type": "simple",
            "complexity": 0.2,
            "context": {"file_count": 1, "context_tokens": 300},
            "routing": {"selected_model": "openrouter/meta-llama/llama-3.1-8b-instruct"}
        },
        {
            "task_type": "complex",
            "complexity": 0.8,
            "context": {"file_count": 5, "context_tokens": 2000},
            "routing": {"selected_model": "openrouter/anthropic/claude-3-sonnet"}
        },
        {
            "task_type": "mobile",
            "complexity": 0.4,
            "context": {"file_count": 2, "context_tokens": 800},
            "routing": {"selected_model": "openrouter/openai/gpt-4o-mini"}
        }
    ]
    
    print("=== Cost Estimation Engine Testing ===")
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n--- Scenario {i}: {scenario['task_type'].title()} Task ---")
        
        estimate = engine.estimate_cost(
            scenario["task_type"],
            scenario["complexity"],
            scenario["context"],
            scenario["routing"]
        )
        
        print(f"Total Estimated Cost: ${estimate.total_cost:.6f}")
        print(f"Confidence Level: {estimate.confidence_level:.2f}")
        print(f"Variance Range: ${estimate.variance_range[0]:.6f} - ${estimate.variance_range[1]:.6f}")
        
        print("Cost Breakdown:")
        for breakdown in estimate.cost_breakdown:
            print(f"  {breakdown.category.value}: ${breakdown.cost:.6f} - {breakdown.explanation}")
        
        if estimate.optimization_suggestions:
            print("Optimization Suggestions:")
            for suggestion in estimate.optimization_suggestions:
                print(f"  • {suggestion}")
        
        print(f"Budget Impact: {estimate.budget_impact['daily_budget_percentage']:.1f}% of daily budget")
    
    # Test budget optimization
    print(f"\n--- Budget Optimization ---")
    task_distribution = {"simple": 10, "complex": 3, "mobile": 5, "analysis": 2}
    optimization = engine.optimize_budget_allocation(5.0, task_distribution)
    
    print(f"Optimization Status: {optimization['optimization_status']}")
    print(f"Budget Utilization: {optimization['budget_utilization']:.1f}%")
    print("Budget Allocation:")
    for task_type, allocation in optimization['budget_allocation'].items():
        print(f"  {task_type}: ${allocation:.4f}")
    
    print("Recommendations:")
    for rec in optimization['recommendations']:
        print(f"  • {rec}")