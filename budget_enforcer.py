#!/usr/bin/env python3
"""
Budget Enforcement Engine
Core philosophy implementation: "strict dollar constraints" - never exceed budget
"""

import os
import json
import time
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

class BudgetEnforcer:
    """
    Hard budget constraint enforcement.
    Philosophy: System knows it's impossible and stops rather than exceed budget.
    """
    
    def __init__(self, daily_limit: float = None):
        self.config_path = Path(".ralex/intelligence-config.yaml")
        self.cost_log_path = Path(".ralex/cost_log.txt")
        self.budget_log_path = Path(".ralex/budget_log.json")
        
        self.config = self.load_config()
        self.daily_limit = daily_limit or self.config.get("cost_limits", {}).get("daily_budget", 5.00)
        self.weekly_limit = self.config.get("cost_limits", {}).get("weekly_budget", 25.00)
        
        # Model cost rates (per 1K tokens) - adjusted for realistic costs
        self.model_costs = {
            "openrouter/meta-llama/llama-3.1-8b-instruct": 0.00006,  # $0.06/1M tokens
            "openrouter/anthropic/claude-3-haiku": 0.00025,          # $0.25/1M tokens  
            "gpt-3.5-turbo": 0.0015,                                 # $1.50/1M tokens
            "gpt-4": 0.03,                                           # $30/1M tokens
            "openrouter/anthropic/claude-3.5-sonnet": 0.003,        # $3/1M tokens
            "openrouter/meta-llama/llama-3.1-70b-instruct": 0.0009, # $0.9/1M tokens
            "gpt-4o": 0.005,                                         # $5/1M tokens
            "openrouter/anthropic/claude-3-opus": 0.015,            # $15/1M tokens
            "openrouter/openai/o1-preview": 0.015                   # $15/1M tokens
        }
        
    def load_config(self) -> dict:
        """Load budget configuration"""
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    return yaml.safe_load(f)
            except Exception:
                pass
        return {"cost_limits": {"daily_budget": 5.00, "weekly_budget": 25.00}}
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for cost calculation.
        Conservative estimate: ~1.3 tokens per word for English text.
        """
        words = len(text.split())
        estimated_tokens = int(words * 1.3)
        
        # Add safety margin for response tokens (assume similar length response)
        total_tokens = estimated_tokens * 2
        
        return max(total_tokens, 100)  # Minimum 100 tokens for realistic costs
    
    def estimate_cost(self, query: str, model: str) -> float:
        """
        Estimate query cost before execution.
        Returns cost in dollars with safety margin.
        """
        tokens = self.estimate_tokens(query)
        
        # Get cost per 1K tokens for model
        cost_per_1k = self.model_costs.get(model, 0.003)  # Default to sonnet rate
        
        # Calculate base cost
        base_cost = (tokens / 1000) * cost_per_1k
        
        # Add 20% safety margin for estimation errors
        estimated_cost = base_cost * 1.2
        
        return round(estimated_cost, 4)
    
    def get_daily_spending(self) -> float:
        """Get total spending for current day"""
        today = datetime.now().date()
        
        if not self.cost_log_path.exists():
            return 0.0
            
        total_spent = 0.0
        
        try:
            with open(self.cost_log_path) as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = eval(line.strip())  # Parse dict string
                            
                            # Parse timestamp
                            timestamp_str = entry.get("timestamp", "")
                            if timestamp_str:
                                entry_date = datetime.fromisoformat(timestamp_str).date()
                                
                                if entry_date == today:
                                    # Look for actual cost (if available) or estimate
                                    cost = entry.get("actual_cost", entry.get("estimated_cost", 0.0))
                                    if isinstance(cost, (int, float)):
                                        total_spent += cost
                                        
                        except Exception:
                            continue  # Skip malformed entries
                            
        except Exception:
            return 0.0
            
        return round(total_spent, 4)
    
    def get_weekly_spending(self) -> float:
        """Get total spending for current week"""
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        if not self.cost_log_path.exists():
            return 0.0
            
        total_spent = 0.0
        
        try:
            with open(self.cost_log_path) as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = eval(line.strip())
                            
                            timestamp_str = entry.get("timestamp", "")
                            if timestamp_str:
                                entry_date = datetime.fromisoformat(timestamp_str).date()
                                
                                if entry_date >= week_start:
                                    cost = entry.get("actual_cost", entry.get("estimated_cost", 0.0))
                                    if isinstance(cost, (int, float)):
                                        total_spent += cost
                                        
                        except Exception:
                            continue
                            
        except Exception:
            return 0.0
            
        return round(total_spent, 4)
    
    def check_budget(self, estimated_cost: float) -> Dict[str, any]:
        """
        Hard budget check - returns whether query is allowed.
        Philosophy: Never exceed configured limits.
        """
        current_daily = self.get_daily_spending()
        current_weekly = self.get_weekly_spending()
        
        # Check daily limit
        if current_daily + estimated_cost > self.daily_limit:
            return {
                "allowed": False,
                "reason": "Daily budget limit exceeded",
                "current_daily_spending": current_daily,
                "daily_limit": self.daily_limit,
                "remaining_daily": max(0, self.daily_limit - current_daily),
                "requested_cost": estimated_cost,
                "philosophy": "System knows it's impossible and stops",
                "suggestion": f"Reduce query complexity or increase daily budget to ${self.daily_limit + 1:.2f}"
            }
        
        # Check weekly limit
        if current_weekly + estimated_cost > self.weekly_limit:
            return {
                "allowed": False,
                "reason": "Weekly budget limit exceeded", 
                "current_weekly_spending": current_weekly,
                "weekly_limit": self.weekly_limit,
                "remaining_weekly": max(0, self.weekly_limit - current_weekly),
                "requested_cost": estimated_cost,
                "philosophy": "System knows it's impossible and stops",
                "suggestion": f"Wait for next week or increase weekly budget to ${self.weekly_limit + 5:.2f}"
            }
        
        # Budget check passed
        return {
            "allowed": True,
            "estimated_cost": estimated_cost,
            "remaining_daily": self.daily_limit - current_daily - estimated_cost,
            "remaining_weekly": self.weekly_limit - current_weekly - estimated_cost,
            "current_daily_spending": current_daily,
            "current_weekly_spending": current_weekly,
            "philosophy": "Cost-first decision approved within constraints"
        }
    
    def record_actual_cost(self, estimated_cost: float, actual_cost: float, model: str, query: str) -> None:
        """
        Record actual cost for budget tracking accuracy.
        Updates cost log with actual vs estimated costs.
        """
        self.budget_log_path.parent.mkdir(exist_ok=True)
        
        budget_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "query_length": len(query),
            "estimated_cost": estimated_cost,
            "actual_cost": actual_cost,
            "estimation_accuracy": abs(actual_cost - estimated_cost) / max(estimated_cost, 0.001),
            "daily_spending_after": self.get_daily_spending() + actual_cost
        }
        
        # Append to budget log
        try:
            existing_entries = []
            if self.budget_log_path.exists():
                with open(self.budget_log_path) as f:
                    existing_entries = json.load(f)
                    
            existing_entries.append(budget_entry)
            
            with open(self.budget_log_path, 'w') as f:
                json.dump(existing_entries, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not record budget entry: {e}")
    
    def get_cost_optimization_suggestions(self, query: str, current_model: str) -> Dict[str, any]:
        """
        Suggest cost optimization alternatives when budget is tight.
        Philosophy: Help users work within constraints.
        """
        suggestions = {
            "current_model": current_model,
            "current_estimated_cost": self.estimate_cost(query, current_model),
            "alternatives": []
        }
        
        # Find cheaper model alternatives
        query_lower = query.lower()
        
        # Classify query complexity
        complex_keywords = ["refactor", "debug", "analyze", "optimize", "create", "build"]
        is_complex = any(keyword in query_lower for keyword in complex_keywords)
        
        if is_complex:
            # Suggest medium-tier instead of premium
            cheaper_models = [
                "openrouter/anthropic/claude-3.5-sonnet",
                "gpt-4",
                "openrouter/meta-llama/llama-3.1-70b-instruct"
            ]
        else:
            # Suggest cheap models for simple queries
            cheaper_models = [
                "openrouter/meta-llama/llama-3.1-8b-instruct",
                "openrouter/anthropic/claude-3-haiku"
            ]
        
        for model in cheaper_models:
            if model != current_model:
                alt_cost = self.estimate_cost(query, model)
                if alt_cost < suggestions["current_estimated_cost"]:
                    suggestions["alternatives"].append({
                        "model": model,
                        "estimated_cost": alt_cost,
                        "savings": suggestions["current_estimated_cost"] - alt_cost,
                        "tier": self.get_model_tier(model)
                    })
        
        # Sort by cost (cheapest first)
        suggestions["alternatives"].sort(key=lambda x: x["estimated_cost"])
        
        return suggestions
    
    def get_model_tier(self, model: str) -> str:
        """Get model tier for cost optimization"""
        if model in ["openrouter/meta-llama/llama-3.1-8b-instruct", "openrouter/anthropic/claude-3-haiku"]:
            return "cheap"
        elif model in ["gpt-4", "openrouter/anthropic/claude-3.5-sonnet", "openrouter/meta-llama/llama-3.1-70b-instruct"]:
            return "medium"
        else:
            return "premium"
    
    def generate_budget_report(self) -> Dict[str, any]:
        """Generate budget usage report for monitoring"""
        today = datetime.now().date()
        
        report = {
            "date": today.isoformat(),
            "daily_spending": self.get_daily_spending(),
            "daily_limit": self.daily_limit,
            "daily_utilization": (self.get_daily_spending() / self.daily_limit) * 100,
            "weekly_spending": self.get_weekly_spending(),
            "weekly_limit": self.weekly_limit,
            "weekly_utilization": (self.get_weekly_spending() / self.weekly_limit) * 100,
            "remaining_daily": max(0, self.daily_limit - self.get_daily_spending()),
            "remaining_weekly": max(0, self.weekly_limit - self.get_weekly_spending()),
            "philosophy_compliance": "Hard constraints enforced"
        }
        
        # Add warnings
        if report["daily_utilization"] > 80:
            report["warning"] = "Approaching daily budget limit"
        elif report["weekly_utilization"] > 80:
            report["warning"] = "Approaching weekly budget limit"
        else:
            report["status"] = "Budget usage within safe limits"
            
        return report

def test_budget_enforcer():
    """Test budget enforcement functionality"""
    print("🧪 Testing Budget Enforcer...")
    
    # Test with very low budget
    enforcer = BudgetEnforcer(daily_limit=0.01)
    
    # Test cost estimation
    query = "refactor this complex architecture with multiple microservices"
    expensive_model = "gpt-4"
    
    estimated_cost = enforcer.estimate_cost(query, expensive_model)
    print(f"  Estimated cost for expensive query: ${estimated_cost:.4f}")
    
    # Test budget check (should fail)
    budget_check = enforcer.check_budget(estimated_cost)
    print(f"  Budget check allowed: {budget_check.get('allowed')}")
    
    if not budget_check.get("allowed"):
        print(f"  ✅ Budget enforcement working: {budget_check.get('reason')}")
        print(f"  💡 Suggestion: {budget_check.get('suggestion')}")
    
    # Test with cheap model
    cheap_model = "openrouter/meta-llama/llama-3.1-8b-instruct"
    cheap_cost = enforcer.estimate_cost("what is python", cheap_model)
    cheap_check = enforcer.check_budget(cheap_cost)
    
    print(f"  Cheap query cost: ${cheap_cost:.4f}")
    print(f"  Cheap query allowed: {cheap_check.get('allowed')}")
    
    # Test cost optimization suggestions
    suggestions = enforcer.get_cost_optimization_suggestions(query, expensive_model)
    print(f"  Cost optimization alternatives: {len(suggestions['alternatives'])}")
    
    if suggestions["alternatives"]:
        best_alt = suggestions["alternatives"][0]
        print(f"  Best alternative: {best_alt['model']} (${best_alt['estimated_cost']:.4f})")
    
    print("  ✅ Budget enforcer tests completed")

if __name__ == "__main__":
    test_budget_enforcer()