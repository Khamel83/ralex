import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

class BudgetOptimizer:
    def __init__(self, usage_log_path="data/ralex_usage_log.jsonl", daily_limit=None, model_tiers=None):
        self.usage_log_path = usage_log_path
        self.daily_limit = daily_limit
        self.model_tiers = model_tiers if model_tiers is not None else {}
        os.makedirs(os.path.dirname(self.usage_log_path), exist_ok=True)

    def record_usage(self, model, tokens_sent, tokens_received, cost):
        """Records usage data to the usage log file."""
        with open(self.usage_log_path, "a") as f:
            record = {
                "timestamp": datetime.now().isoformat(),
                "model": model,
                "tokens_sent": tokens_sent,
                "tokens_received": tokens_received,
                "cost": cost
            }
            f.write(json.dumps(record) + "\n")

    def get_total_spent(self):
        """Reads the usage log and sums the total cost."""
        total_cost = 0.0
        if not os.path.exists(self.usage_log_path):
            return total_cost

        with open(self.usage_log_path, "r") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    total_cost += record.get("cost", 0.0)
                except json.JSONDecodeError:
                    continue
        return total_cost

    def get_spent_today(self):
        """Calculates the total cost spent today."""
        total_cost_today = 0.0
        if not os.path.exists(self.usage_log_path):
            return total_cost_today

        today = datetime.now().date()
        with open(self.usage_log_path, "r") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    record_date = datetime.fromisoformat(record["timestamp"]).date()
                    if record_date == today:
                        total_cost_today += record.get("cost", 0.0)
                except (json.JSONDecodeError, ValueError):
                    continue
        return total_cost_today

    def check_budget_status(self):
        """Compares current spending against the daily limit and returns a status."""
        if self.daily_limit is None:
            return {"status": "no_limit", "spent_today": self.get_spent_today(), "daily_limit": None}

        spent_today = self.get_spent_today()
        percentage_used = (spent_today / self.daily_limit) * 100

        status = "safe"
        if percentage_used >= 100:
            status = "exceeded"
        elif percentage_used >= 80:
            status = "warning"
        
        return {
            "status": status,
            "spent_today": spent_today,
            "daily_limit": self.daily_limit,
            "percentage_used": percentage_used,
            "remaining": self.daily_limit - spent_today if self.daily_limit is not None else float('inf')
        }

    def get_model_cost(self, model_name):
        """Retrieves the cost per token for a given model."""
        for tier_name, models in self.model_tiers.get("tiers", {}).items():
            for model_info in models:
                if model_info["name"] == model_name:
                    return model_info["cost_per_token"]
        return 0.0 # Default to 0 if model not found

    def get_cheapest_model_in_tier(self, tier_name):
        """Returns the cheapest model available within a given tier."""
        cheapest_model = None
        min_cost = float('inf')

        if tier_name in self.model_tiers.get("tiers", {}):
            for model_info in self.model_tiers["tiers"][tier_name]:
                if model_info["cost_per_token"] < min_cost:
                    min_cost = model_info["cost_per_token"]
                    cheapest_model = model_info["name"]
        return cheapest_model

    def select_affordable_model(self, preferred_model, preferred_tier, budget_remaining):
        """Selects the most affordable model within budget, potentially downgrading tiers."""
        # Try the preferred model first
        cost_of_preferred = self.get_model_cost(preferred_model)
        if budget_remaining >= cost_of_preferred:
            return preferred_model, preferred_tier

        # If preferred model is too expensive, try to downgrade
        tier_hierarchy = ["diamond", "platinum", "premium", "gold", "standard", "silver", "cheap"]
        current_tier_index = tier_hierarchy.index(preferred_tier) if preferred_tier in tier_hierarchy else -1

        for i in range(current_tier_index + 1, len(tier_hierarchy)):
            downgrade_tier = tier_hierarchy[i]
            if downgrade_tier in self.model_tiers.get("tiers", {}):
                for model_info in self.model_tiers["tiers"][downgrade_tier]:
                    model_name = model_info["name"]
                    model_cost = self.get_model_cost(model_name)
                    if budget_remaining >= model_cost:
                        return model_name, downgrade_tier
        
        # If no affordable model found, return the cheapest available (even if over budget)
        cheapest_model = None
        min_cost = float('inf')
        for tier_name, models in self.model_tiers.get("tiers", {}).items():
            for model_info in models:
                if model_info["cost_per_token"] < min_cost:
                    min_cost = model_info["cost_per_token"]
                    cheapest_model = model_info["name"]
        
        return cheapest_model, "cheap" # Return cheapest and its tier (default to cheap)

    def get_daily_spending(self):
        """Returns a dictionary of daily spending."""
        daily_spending = defaultdict(float)
        if not os.path.exists(self.usage_log_path):
            return dict(daily_spending)

        with open(self.usage_log_path, "r") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    record_date = datetime.fromisoformat(record["timestamp"]).date().isoformat()
                    daily_spending[record_date] += record.get("cost", 0.0)
                except (json.JSONDecodeError, ValueError):
                    continue
        return dict(daily_spending)

    def get_model_spending(self):
        """Returns a dictionary of spending per model."""
        model_spending = defaultdict(float)
        if not os.path.exists(self.usage_log_path):
            return dict(model_spending)

        with open(self.usage_log_path, "r") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    model_spending[record["model"]] += record.get("cost", 0.0)
                except (json.JSONDecodeError, ValueError):
                    continue
        return dict(model_spending)