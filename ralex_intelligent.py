#\!/usr/bin/env python3
"""
Ralex Intelligence Router - Cost-first complexity detection and routing
Lightweight wrapper approach using existing infrastructure
"""

import os
import time
import yaml
from pathlib import Path
from datetime import datetime

class RalexIntelligenceRouter:
    """Minimal intelligence routing with cost optimization"""
    
    def __init__(self):
        self.config_path = Path(".ralex/intelligence-config.yaml") 
        self.config = self.load_config()
        self.context_memory = {}
        
    def load_config(self):
        """Load intelligence configuration"""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return yaml.safe_load(f)
        return {"enabled": False}
    
    def classify_intent(self, query: str) -> str:
        """Simple intent classification - 2 second max"""
        start_time = time.time()
        
        query_lower = query.lower()
        
        # Check for simple intents
        simple_words = self.config.get("intent_mappings", {}).get("simple", [])
        for word in simple_words:
            if word in query_lower:
                self.log_performance("classify_intent", time.time() - start_time)
                return "simple"
        
        # Check for complex intents  
        complex_words = self.config.get("intent_mappings", {}).get("complex", [])
        for word in complex_words:
            if word in query_lower:
                self.log_performance("classify_intent", time.time() - start_time)
                return "complex"
        
        # Default to simple for unknown
        self.log_performance("classify_intent", time.time() - start_time)
        return "simple"
    
    def add_context_hint(self, query: str) -> str:
        """Add 3-5 token context hint"""
        if not self.config.get("performance", {}).get("context_token_limit", 0):
            return query
            
        # Simple context state tracking
        context_hint = ""
        if "code" in query.lower() or "function" in query.lower():
            context_hint = " [context:coding-session]"
        elif "debug" in query.lower() or "error" in query.lower():
            context_hint = " [context:debugging]"
        
        return query + context_hint
    
    def route_query(self, query: str) -> dict:
        """Main routing logic"""
        if not self.config.get("enabled", False):
            return {
                "route": "direct",
                "model_tier": "medium", 
                "query": query,
                "reasoning": "Intelligence routing disabled"
            }
        
        start_time = time.time()
        
        try:
            # Step 1: Classify intent (cost-effective)
            intent = self.classify_intent(query)
            
            # Step 2: Add context hints
            enhanced_query = self.add_context_hint(query)
            
            # Step 3: Route based on intent
            if intent == "simple":
                result = {
                    "route": "direct",
                    "model_tier": "cheap",
                    "query": enhanced_query,
                    "reasoning": f"Simple query routed to cheap model"
                }
            else:
                result = {
                    "route": "agent-os", 
                    "model_tier": "medium",
                    "query": enhanced_query,
                    "reasoning": f"Complex query routed to agent-os workflow"
                }
            
            # Log routing decision
            self.log_routing_decision(query, result, time.time() - start_time)
            return result
            
        except Exception as e:
            # Graceful fallback
            return {
                "route": "direct",
                "model_tier": "medium",
                "query": query, 
                "reasoning": f"Routing failed, using fallback: {str(e)}"
            }
    
    def log_routing_decision(self, query: str, result: dict, duration: float):
        """Log routing decision for cost tracking"""
        if not self.config.get("metrics", {}).get("cost_tracking", False):
            return
            
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query_length": len(query),
            "intent": result.get("reasoning", ""),
            "route": result["route"],
            "model_tier": result["model_tier"],
            "routing_time": duration
        }
        
        log_file = Path(self.config.get("metrics", {}).get("log_file", ".ralex/cost_log.txt"))
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, "a") as f:
            f.write(f"{log_entry}\n")
    
    def log_performance(self, operation: str, duration: float):
        """Log performance metrics"""
        if duration > 3.0:  # Performance warning
            print(f"⚠️  Performance: {operation} took {duration:.2f}s (>3s threshold)")

def test_fallbacks():
    """Test fallback mechanisms"""
    router = RalexIntelligenceRouter()
    
    # Test with intelligence disabled
    result = router.route_query("test query")
    assert result["route"] == "direct"
    
    # Test with simple query
    router.config["enabled"] = True
    result = router.route_query("what is python")
    assert result["model_tier"] == "cheap"
    
    # Test with complex query
    result = router.route_query("refactor this code")
    assert result["route"] == "agent-os"
    
    print("✅ All fallback tests passed")

if __name__ == "__main__":
    test_fallbacks()
EOF < /dev/null
