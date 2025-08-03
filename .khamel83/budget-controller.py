#!/usr/bin/env python3
"""
Budget Controller for Ralex Operations
Manages daily/hourly budget limits and prevents overrun.
"""

import os
import json
import time
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Optional

class BudgetController:
    def __init__(self, config_file: str = ".khamel83/budget-config.json"):
        self.config_file = Path(config_file)
        self.daily_budget = float(os.getenv("DAILY_BUDGET", "5.00"))
        self.hourly_limit = float(os.getenv("HOURLY_LIMIT", "1.25"))
        self.budget_data = self.load_budget_data()
        
    def load_budget_data(self) -> Dict:
        if self.config_file.exists():
            with open(self.config_file) as f:
                return json.load(f)
        return {"daily_spend": {}, "hourly_spend": {}}
    
    def save_budget_data(self):
        self.config_file.parent.mkdir(exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(self.budget_data, f, indent=2)
    
    def get_current_day_key(self) -> str:
        return date.today().isoformat()
    
    def get_current_hour_key(self) -> str:
        return datetime.now().strftime("%Y-%m-%d-%H")
    
    def check_budget_available(self, requested_amount: float) -> bool:
        day_key = self.get_current_day_key()
        hour_key = self.get_current_hour_key()
        
        daily_spent = self.budget_data["daily_spend"].get(day_key, 0.0)
        hourly_spent = self.budget_data["hourly_spend"].get(hour_key, 0.0)
        
        daily_available = self.daily_budget - daily_spent
        hourly_available = self.hourly_limit - hourly_spent
        
        return (requested_amount <= daily_available and 
                requested_amount <= hourly_available)
    
    def record_spend(self, amount: float, operation_id: str):
        day_key = self.get_current_day_key()
        hour_key = self.get_current_hour_key()
        
        if day_key not in self.budget_data["daily_spend"]:
            self.budget_data["daily_spend"][day_key] = 0.0
        if hour_key not in self.budget_data["hourly_spend"]:
            self.budget_data["hourly_spend"][hour_key] = 0.0
            
        self.budget_data["daily_spend"][day_key] += amount
        self.budget_data["hourly_spend"][hour_key] += amount
        
        self.save_budget_data()
    
    def get_budget_status(self) -> Dict:
        day_key = self.get_current_day_key()
        hour_key = self.get_current_hour_key()
        
        daily_spent = self.budget_data["daily_spend"].get(day_key, 0.0)
        hourly_spent = self.budget_data["hourly_spend"].get(hour_key, 0.0)
        
        return {
            "daily": {
                "budget": self.daily_budget,
                "spent": daily_spent,
                "remaining": self.daily_budget - daily_spent
            },
            "hourly": {
                "limit": self.hourly_limit,
                "spent": hourly_spent,
                "remaining": self.hourly_limit - hourly_spent
            }
        }