#!/usr/bin/env python3
"""
Philosophy Embodiment Testing Framework
Quantitative measurement of cost-first agentic thinking implementation
"""

import os
import time
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import asyncio

class PhilosophyEmbodimentTester:
    """
    Systematic testing framework for philosophy embodiment measurement.
    Target: Validate 95% philosophy embodiment achievement.
    """
    
    def __init__(self):
        self.test_results = {}
        self.philosophy_score = 0.0
        self.config = self.load_config()
        
    def load_config(self) -> dict:
        """Load testing configuration"""
        config_path = Path(".ralex/philosophy-testing-config.yaml")
        if config_path.exists():
            with open(config_path) as f:
                return yaml.safe_load(f)
        return self.create_default_config()
    
    def create_default_config(self) -> dict:
        """Create default testing configuration"""
        return {
            "testing": {
                "budget_limits": [0.01, 0.10, 1.00, 5.00],
                "test_queries": {
                    "simple": [
                        "what is python",
                        "explain functions", 
                        "how to print hello world",
                        "define variables"
                    ],
                    "complex": [
                        "refactor this complex architecture",
                        "debug memory leak in application", 
                        "create comprehensive test suite",
                        "optimize database performance"
                    ],
                    "expensive": [
                        "analyze entire codebase for patterns",
                        "generate complete documentation suite",
                        "create comprehensive migration strategy"
                    ]
                },
                "philosophy_weights": {
                    "budget_enforcement": 0.30,     # 30% of total score
                    "cost_first_routing": 0.25,     # 25% of total score  
                    "agentic_thinking": 0.20,       # 20% of total score
                    "graceful_failure": 0.15,       # 15% of total score
                    "systematic_methodology": 0.10   # 10% of total score
                }
            }
        }
    
    async def test_budget_enforcement(self) -> Dict[str, float]:
        """
        Test 1: Budget Enforcement (30% of philosophy score)
        Validates 'strict dollar constraints' never violated
        """
        print("🧪 Testing Budget Enforcement...")
        
        test_results = {
            "hard_stops": 0.0,
            "cost_estimation": 0.0, 
            "budget_tracking": 0.0,
            "graceful_messages": 0.0
        }
        
        # Test hard stops with various budget limits
        for budget_limit in self.config["testing"]["budget_limits"]:
            print(f"  Testing budget limit: ${budget_limit}")
            
            # Test expensive query that should exceed budget
            expensive_query = self.config["testing"]["test_queries"]["expensive"][0]
            
            try:
                # This should be implemented in the budget enforcer
                from budget_enforcer import BudgetEnforcer
                enforcer = BudgetEnforcer(daily_limit=budget_limit)
                
                # Test cost estimation
                estimated_cost = enforcer.estimate_cost(expensive_query, "gpt-4")
                if estimated_cost > 0:
                    test_results["cost_estimation"] += 0.25
                
                # Test budget check
                budget_check = enforcer.check_budget(estimated_cost)
                
                if budget_limit < 0.05 and not budget_check.get("allowed", True):
                    test_results["hard_stops"] += 0.25
                    
                    # Test graceful failure message quality
                    error_msg = budget_check.get("reason", "")
                    if "budget" in error_msg.lower() and "remaining" in str(budget_check):
                        test_results["graceful_messages"] += 0.25
                        
            except ImportError:
                print("    ❌ Budget enforcer not implemented")
                test_results["hard_stops"] = 0.0
                break
            except Exception as e:
                print(f"    ⚠️  Budget enforcement error: {e}")
        
        # Test real-time budget tracking
        try:
            cost_log_path = Path(".ralex/cost_log.txt")
            if cost_log_path.exists():
                with open(cost_log_path) as f:
                    logs = [line.strip() for line in f if line.strip()]
                    if len(logs) > 0:
                        test_results["budget_tracking"] = 1.0
        except Exception:
            test_results["budget_tracking"] = 0.0
            
        average_score = sum(test_results.values()) / len(test_results)
        print(f"  ✅ Budget Enforcement Score: {average_score:.2f}/1.0")
        
        return {"budget_enforcement": average_score, "details": test_results}
    
    async def test_cost_first_routing(self) -> Dict[str, float]:
        """
        Test 2: Cost-First Routing (25% of philosophy score)
        Validates 'cheap LLMs do thinking'
        """
        print("🧪 Testing Cost-First Routing...")
        
        test_results = {
            "simple_to_cheap": 0.0,
            "complex_routing": 0.0,
            "routing_consistency": 0.0,
            "cost_optimization": 0.0
        }
        
        try:
            from ralex_intelligent import RalexIntelligenceRouter
            router = RalexIntelligenceRouter()
            
            # Test simple queries route to cheap models
            simple_queries = self.config["testing"]["test_queries"]["simple"]
            cheap_model_count = 0
            
            for query in simple_queries:
                result = router.route_query(query)
                model_tier = result.get("model_tier", "unknown")
                if model_tier == "cheap":
                    cheap_model_count += 1
                    
            test_results["simple_to_cheap"] = cheap_model_count / len(simple_queries)
            
            # Test complex queries use appropriate routing
            complex_queries = self.config["testing"]["test_queries"]["complex"]
            complex_routing_count = 0
            
            for query in complex_queries:
                result = router.route_query(query)
                route = result.get("route", "unknown")
                if route in ["agent-os", "template"]:
                    complex_routing_count += 1
                    
            test_results["complex_routing"] = complex_routing_count / len(complex_queries)
            
            # Test routing consistency
            test_query = simple_queries[0]
            results = [router.route_query(test_query) for _ in range(5)]
            models = [r.get("model_tier") for r in results]
            if len(set(models)) == 1:  # All same model tier
                test_results["routing_consistency"] = 1.0
                
            # Test cost optimization (cheap models preferred)
            all_queries = simple_queries + complex_queries
            total_cheap = sum(1 for q in all_queries 
                            if router.route_query(q).get("model_tier") == "cheap")
            test_results["cost_optimization"] = total_cheap / len(all_queries)
            
        except ImportError:
            print("    ❌ Intelligence router not available")
            return {"cost_first_routing": 0.0, "details": test_results}
        except Exception as e:
            print(f"    ⚠️  Routing test error: {e}")
            
        average_score = sum(test_results.values()) / len(test_results)
        print(f"  ✅ Cost-First Routing Score: {average_score:.2f}/1.0")
        
        return {"cost_first_routing": average_score, "details": test_results}
    
    async def test_agentic_thinking(self) -> Dict[str, float]:
        """
        Test 3: Agentic Thinking (20% of philosophy score)
        Validates systematic methodology application
        """
        print("🧪 Testing Agentic Thinking...")
        
        test_results = {
            "template_loading": 0.0,
            "template_application": 0.0,
            "methodology_difference": 0.0,
            "systematic_approach": 0.0
        }
        
        try:
            # Test template loading
            template_files = list(Path(".agent-os/templates").glob("*.yaml"))
            if len(template_files) >= 3:  # debug, refactor, test templates
                test_results["template_loading"] = 1.0
                
            # Test template application
            from ralex_bridge import RalexBridge
            bridge = RalexBridge()
            
            complex_queries = self.config["testing"]["test_queries"]["complex"]
            template_applied_count = 0
            
            for query in complex_queries:
                if "debug" in query.lower():
                    result = await bridge.process_request(query)
                    thinking = result.get("thinking", {})
                    if "template" in thinking and thinking.get("template"):
                        template_applied_count += 1
                        
            if len(complex_queries) > 0:
                test_results["template_application"] = template_applied_count / len(complex_queries)
                
            # Test methodology difference (agentic vs direct)
            simple_query = self.config["testing"]["test_queries"]["simple"][0]
            complex_query = self.config["testing"]["test_queries"]["complex"][0]
            
            simple_result = await bridge.process_request(simple_query)
            complex_result = await bridge.process_request(complex_query)
            
            simple_agentic = simple_result.get("thinking", {}).get("route") == "agent-os"
            complex_agentic = complex_result.get("thinking", {}).get("route") == "agent-os"
            
            if not simple_agentic and complex_agentic:
                test_results["methodology_difference"] = 1.0
            elif simple_agentic == complex_agentic:
                test_results["methodology_difference"] = 0.5  # Some differentiation
                
            # Test systematic approach (templates contain workflows)
            if template_files:
                systematic_count = 0
                for template_file in template_files:
                    with open(template_file) as f:
                        template_content = yaml.safe_load(f)
                        if "workflow" in template_content:
                            systematic_count += 1
                            
                test_results["systematic_approach"] = systematic_count / len(template_files)
                
        except Exception as e:
            print(f"    ⚠️  Agentic thinking test error: {e}")
            
        average_score = sum(test_results.values()) / len(test_results)
        print(f"  ✅ Agentic Thinking Score: {average_score:.2f}/1.0")
        
        return {"agentic_thinking": average_score, "details": test_results}
    
    async def test_graceful_failure(self) -> Dict[str, float]:
        """
        Test 4: Graceful Failure (15% of philosophy score)
        Validates 'know it's impossible and stop'
        """
        print("🧪 Testing Graceful Failure...")
        
        test_results = {
            "budget_exceeded_messages": 0.0,
            "alternative_suggestions": 0.0,
            "educational_value": 0.0,
            "cost_transparency": 0.0
        }
        
        try:
            from budget_enforcer import BudgetEnforcer
            
            # Test budget exceeded messages
            enforcer = BudgetEnforcer(daily_limit=0.01)  # Very low budget
            expensive_query = self.config["testing"]["test_queries"]["expensive"][0]
            estimated_cost = enforcer.estimate_cost(expensive_query, "gpt-4")
            budget_check = enforcer.check_budget(estimated_cost)
            
            if not budget_check.get("allowed", True):
                error_msg = budget_check.get("reason", "")
                if "budget" in error_msg.lower():
                    test_results["budget_exceeded_messages"] = 1.0
                    
                # Test cost transparency
                if "remaining" in str(budget_check):
                    test_results["cost_transparency"] = 1.0
                    
                # Test alternative suggestions (if implemented)
                if "suggestion" in str(budget_check) or "alternative" in str(budget_check):
                    test_results["alternative_suggestions"] = 1.0
                    
                # Test educational value
                if "optimization" in str(budget_check) or "cheaper" in str(budget_check):
                    test_results["educational_value"] = 1.0
                    
        except ImportError:
            print("    ❌ Budget enforcer not implemented")
            return {"graceful_failure": 0.0, "details": test_results}
        except Exception as e:
            print(f"    ⚠️  Graceful failure test error: {e}")
            
        average_score = sum(test_results.values()) / len(test_results)
        print(f"  ✅ Graceful Failure Score: {average_score:.2f}/1.0")
        
        return {"graceful_failure": average_score, "details": test_results}
    
    async def test_systematic_methodology(self) -> Dict[str, float]:
        """
        Test 5: Systematic Methodology (10% of philosophy score)
        Validates agent-os principles implementation
        """
        print("🧪 Testing Systematic Methodology...")
        
        test_results = {
            "agent_os_structure": 0.0,
            "template_methodology": 0.0,
            "cost_first_decisions": 0.0,
            "measurable_outcomes": 0.0
        }
        
        # Test agent-os structure exists
        agent_os_path = Path(".agent-os")
        if agent_os_path.exists():
            required_dirs = ["templates", "task-specs", "philosophy"]
            existing_dirs = [d.name for d in agent_os_path.iterdir() if d.is_dir()]
            
            structure_score = len(set(required_dirs) & set(existing_dirs)) / len(required_dirs)
            test_results["agent_os_structure"] = structure_score
            
        # Test template methodology
        templates_path = Path(".agent-os/templates")
        if templates_path.exists():
            template_files = list(templates_path.glob("*.yaml"))
            methodology_count = 0
            
            for template_file in template_files:
                try:
                    with open(template_file) as f:
                        template = yaml.safe_load(f)
                        if "workflow" in template and "philosophy" in template:
                            methodology_count += 1
                except Exception:
                    continue
                    
            if template_files:
                test_results["template_methodology"] = methodology_count / len(template_files)
                
        # Test cost-first decisions in configuration
        config_path = Path(".ralex/intelligence-config.yaml")
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = yaml.safe_load(f)
                    if "cost_limits" in config or "model_tiers" in config:
                        test_results["cost_first_decisions"] = 1.0
            except Exception:
                pass
                
        # Test measurable outcomes (cost logging)
        cost_log_path = Path(".ralex/cost_log.txt")
        if cost_log_path.exists():
            test_results["measurable_outcomes"] = 1.0
            
        average_score = sum(test_results.values()) / len(test_results)
        print(f"  ✅ Systematic Methodology Score: {average_score:.2f}/1.0")
        
        return {"systematic_methodology": average_score, "details": test_results}
    
    async def run_comprehensive_philosophy_test(self) -> Dict[str, float]:
        """
        Run complete philosophy embodiment test suite
        Returns overall philosophy embodiment score (target: 95%)
        """
        print("🎯 Running Comprehensive Philosophy Embodiment Test")
        print("=" * 60)
        
        # Run all test components
        test_results = {}
        
        test_results.update(await self.test_budget_enforcement())
        test_results.update(await self.test_cost_first_routing())
        test_results.update(await self.test_agentic_thinking())
        test_results.update(await self.test_graceful_failure())
        test_results.update(await self.test_systematic_methodology())
        
        # Calculate weighted philosophy score
        weights = self.config["testing"]["philosophy_weights"]
        total_score = 0.0
        
        for component, weight in weights.items():
            component_score = test_results.get(component, 0.0)
            weighted_score = component_score * weight
            total_score += weighted_score
            
        self.philosophy_score = total_score
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        results_file = Path(f".ralex/philosophy_test_results_{timestamp}.json")
        
        detailed_results = {
            "timestamp": timestamp,
            "overall_score": total_score,
            "target_score": 0.95,
            "components": test_results,
            "weights": weights,
            "pass": total_score >= 0.95
        }
        
        with open(results_file, 'w') as f:
            json.dump(detailed_results, f, indent=2)
            
        print("=" * 60)
        print(f"🎯 Overall Philosophy Embodiment Score: {total_score:.1%}")
        print(f"🎯 Target Score: 95%")
        print(f"🎯 Status: {'✅ PASS' if total_score >= 0.95 else '❌ NEEDS IMPROVEMENT'}")
        
        if total_score < 0.95:
            print("\n📋 Improvement Areas:")
            for component, weight in weights.items():
                component_score = test_results.get(component, 0.0)
                if component_score < 0.8:  # Below 80% threshold
                    print(f"  ⚠️  {component}: {component_score:.1%} (Weight: {weight:.0%})")
                    
        print(f"\n📊 Detailed results saved to: {results_file}")
        
        return detailed_results

def create_philosophy_testing_config():
    """Create philosophy testing configuration file"""
    config_path = Path(".ralex/philosophy-testing-config.yaml")
    config_path.parent.mkdir(exist_ok=True)
    
    tester = PhilosophyEmbodimentTester()
    config = tester.create_default_config()
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
        
    print(f"✅ Created philosophy testing config: {config_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--create-config":
        create_philosophy_testing_config()
        sys.exit(0)
        
    async def main():
        tester = PhilosophyEmbodimentTester()
        results = await tester.run_comprehensive_philosophy_test()
        
        if results["pass"]:
            print("\n🎉 Philosophy embodiment target achieved!")
            sys.exit(0)
        else:
            print("\n🔧 Philosophy embodiment needs improvement")
            sys.exit(1)
            
    asyncio.run(main())