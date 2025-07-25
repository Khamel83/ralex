#!/usr/bin/env python3
"""
Ralex V2: Simple Cost Tracker (30 lines)
"""
import json
import os
from datetime import datetime
from typing import Dict, Any

class RalexBudgetTracker:
    def __init__(self, daily_limit: float = 5.0):
        self.daily_limit = daily_limit
        self.log_file = "ralex_costs.json"
    
    def log_request(self, model: str, tokens: int, cost: float) -> None:
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Load existing data
        data = {}
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                data = json.load(f)
        
        # Initialize today's data
        if today not in data:
            data[today] = {"total_cost": 0, "requests": []}
        
        # Add new request
        data[today]["total_cost"] += cost
        data[today]["requests"].append({
            "model": model,
            "tokens": tokens, 
            "cost": cost,
            "timestamp": datetime.now().isoformat()
        })
        
        # Save data
        with open(self.log_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Check budget
        if data[today]["total_cost"] > self.daily_limit:
            print(f"⚠️  Budget alert: ${data[today]['total_cost']:.3f} > ${self.daily_limit}")
        
        print(f"💰 Today's spend: ${data[today]['total_cost']:.3f} ({len(data[today]['requests'])} requests)")

if __name__ == "__main__":
    tracker = RalexBudgetTracker()
    print("Ralex V2 Cost Tracker initialized")
    print(f"Daily budget: ${tracker.daily_limit}")