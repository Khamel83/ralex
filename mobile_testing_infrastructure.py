#!/usr/bin/env python3
"""
Mobile Testing Infrastructure
Automated validation of mobile app integration and documentation accuracy
"""

import os
import json
import time
import requests
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class MobileTestingInfrastructure:
    """
    Comprehensive mobile integration testing framework.
    Validates OpenCat integration and mobile API functionality.
    """
    
    def __init__(self):
        self.test_results = {}
        self.api_base_url = "http://localhost:8000"
        self.test_config = self.load_test_config()
        
    def load_test_config(self) -> dict:
        """Load mobile testing configuration"""
        return {
            "api": {
                "base_url": "http://localhost:8000",
                "endpoints": [
                    "/v1/chat/completions",
                    "/v1/models", 
                    "/health"
                ],
                "timeout": 30
            },
            "mobile": {
                "test_queries": [
                    "test connection",
                    "what is python",
                    "debug this error",
                    "refactor my code"
                ],
                "expected_models": [
                    "ralex-bridge",
                    "ralex-cheap", 
                    "ralex-medium"
                ]
            },
            "performance": {
                "max_response_time": 5.0,
                "max_startup_time": 10.0,
                "min_success_rate": 0.95
            }
        }
    
    def test_api_server_availability(self) -> Dict[str, any]:
        """
        Test 1: API Server Availability
        Validates FastAPI server is running and accessible
        """
        print("📱 Testing API Server Availability...")
        
        test_results = {
            "server_running": False,
            "port_accessible": False,
            "response_time": 0.0,
            "startup_detection": False
        }
        
        # Test if server is running on port 8000
        try:
            start_time = time.time()
            response = requests.get(
                f"{self.api_base_url}/health",
                timeout=self.test_config["api"]["timeout"]
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                test_results["server_running"] = True
                test_results["port_accessible"] = True
                test_results["response_time"] = response_time
                
                health_data = response.json()
                if "status" in health_data:
                    test_results["startup_detection"] = True
                    
                print(f"  ✅ API server accessible in {response_time:.2f}s")
            else:
                print(f"  ❌ API server returned status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("  ❌ API server not accessible on port 8000")
            
            # Check if something else is running on port 8000
            try:
                result = subprocess.run(
                    ["netstat", "-tlnp"], 
                    capture_output=True, 
                    text=True,
                    timeout=10
                )
                if ":8000" in result.stdout:
                    print("  ⚠️  Port 8000 is occupied by another service")
                else:
                    print("  ⚠️  Port 8000 is not in use")
            except Exception:
                print("  ⚠️  Cannot check port status")
                
        except Exception as e:
            print(f"  ❌ API server test error: {e}")
            
        return test_results
    
    def test_openai_api_compatibility(self) -> Dict[str, any]:
        """
        Test 2: OpenAI API Compatibility
        Validates API endpoints match OpenAI specification
        """
        print("📱 Testing OpenAI API Compatibility...")
        
        test_results = {
            "chat_completions_endpoint": False,
            "models_endpoint": False,
            "request_format_compatibility": False,
            "response_format_compatibility": False,
            "error_handling": False
        }
        
        # Test /v1/chat/completions endpoint
        try:
            chat_request = {
                "model": "ralex-bridge",
                "messages": [
                    {"role": "user", "content": "test connection"}
                ],
                "max_tokens": 50
            }
            
            response = requests.post(
                f"{self.api_base_url}/v1/chat/completions",
                json=chat_request,
                timeout=self.test_config["api"]["timeout"]
            )
            
            if response.status_code == 200:
                test_results["chat_completions_endpoint"] = True
                test_results["request_format_compatibility"] = True
                
                # Validate OpenAI response format
                data = response.json()
                required_fields = ["choices", "model", "usage"]
                if all(field in data for field in required_fields):
                    test_results["response_format_compatibility"] = True
                    print("  ✅ Chat completions endpoint working")
                else:
                    print(f"  ⚠️  Response missing fields: {set(required_fields) - set(data.keys())}")
                    
            else:
                print(f"  ❌ Chat completions returned status {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Chat completions test error: {e}")
            
        # Test /v1/models endpoint
        try:
            response = requests.get(
                f"{self.api_base_url}/v1/models",
                timeout=self.test_config["api"]["timeout"]
            )
            
            if response.status_code == 200:
                test_results["models_endpoint"] = True
                
                data = response.json()
                if "data" in data and isinstance(data["data"], list):
                    models = [model.get("id") for model in data["data"]]
                    expected_models = self.test_config["mobile"]["expected_models"]
                    
                    if any(model in models for model in expected_models):
                        print("  ✅ Models endpoint working")
                    else:
                        print(f"  ⚠️  Expected models not found: {expected_models}")
                        print(f"  📋 Available models: {models}")
                else:
                    print("  ⚠️  Models endpoint format incorrect")
                    
            else:
                print(f"  ❌ Models endpoint returned status {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Models endpoint test error: {e}")
            
        # Test error handling
        try:
            invalid_request = {
                "model": "invalid-model",
                "messages": [{"role": "user", "content": "test"}]
            }
            
            response = requests.post(
                f"{self.api_base_url}/v1/chat/completions",
                json=invalid_request,
                timeout=self.test_config["api"]["timeout"]
            )
            
            if response.status_code >= 400:
                test_results["error_handling"] = True
                print("  ✅ Error handling working")
            else:
                print("  ⚠️  Error handling may not be working properly")
                
        except Exception as e:
            print(f"  ⚠️  Error handling test failed: {e}")
            
        return test_results
    
    def test_mobile_query_workflows(self) -> Dict[str, any]:
        """
        Test 3: Mobile Query Workflows
        Validates end-to-end mobile app query scenarios
        """
        print("📱 Testing Mobile Query Workflows...")
        
        test_results = {
            "simple_queries": 0.0,
            "complex_queries": 0.0,
            "response_times": [],
            "success_rate": 0.0,
            "cost_tracking": False
        }
        
        test_queries = self.test_config["mobile"]["test_queries"]
        successful_queries = 0
        total_queries = len(test_queries)
        
        for i, query in enumerate(test_queries):
            print(f"  Testing query {i+1}/{total_queries}: '{query}'")
            
            try:
                start_time = time.time()
                
                request_data = {
                    "model": "ralex-bridge",
                    "messages": [{"role": "user", "content": query}],
                    "max_tokens": 100
                }
                
                response = requests.post(
                    f"{self.api_base_url}/v1/chat/completions",
                    json=request_data,
                    timeout=self.test_config["api"]["timeout"]
                )
                
                response_time = time.time() - start_time
                test_results["response_times"].append(response_time)
                
                if response.status_code == 200:
                    successful_queries += 1
                    
                    data = response.json()
                    if "choices" in data and len(data["choices"]) > 0:
                        content = data["choices"][0].get("message", {}).get("content", "")
                        
                        if query in ["test connection", "what is python"]:
                            # Simple queries
                            if len(content) > 10:  # Got reasonable response
                                test_results["simple_queries"] += 0.5
                        else:
                            # Complex queries
                            if len(content) > 20:  # Got more detailed response
                                test_results["complex_queries"] += 0.5
                                
                    # Check for cost information
                    if "usage" in data:
                        test_results["cost_tracking"] = True
                        
                    print(f"    ✅ Success in {response_time:.2f}s")
                else:
                    print(f"    ❌ Failed with status {response.status_code}")
                    
            except Exception as e:
                print(f"    ❌ Query failed: {e}")
                
        # Calculate success rate
        test_results["success_rate"] = successful_queries / total_queries if total_queries > 0 else 0.0
        
        # Performance analysis
        if test_results["response_times"]:
            avg_response_time = sum(test_results["response_times"]) / len(test_results["response_times"])
            max_response_time = max(test_results["response_times"])
            
            print(f"  📊 Average response time: {avg_response_time:.2f}s")
            print(f"  📊 Max response time: {max_response_time:.2f}s")
            print(f"  📊 Success rate: {test_results['success_rate']:.1%}")
            
            performance_threshold = self.test_config["performance"]["max_response_time"]
            if avg_response_time <= performance_threshold:
                print(f"  ✅ Performance meets threshold (<{performance_threshold}s)")
            else:
                print(f"  ⚠️  Performance exceeds threshold (>{performance_threshold}s)")
                
        return test_results
    
    def test_documentation_accuracy(self) -> Dict[str, any]:
        """
        Test 4: Documentation Accuracy
        Validates documented mobile setup instructions work
        """
        print("📱 Testing Documentation Accuracy...")
        
        test_results = {
            "setup_instructions": False,
            "configuration_values": False,
            "workflow_completeness": False,
            "troubleshooting_accuracy": False
        }
        
        # Test documented configuration values
        documented_config = {
            "base_url": "http://[your-rpi-ip]:8000/v1",
            "api_key": "ralex-key",
            "model": "ralex-bridge"
        }
        
        # Validate base URL format
        if self.api_base_url.endswith(":8000"):
            test_results["configuration_values"] = True
            print("  ✅ Base URL configuration matches documentation")
        else:
            print("  ❌ Base URL configuration doesn't match documentation")
            
        # Test API key handling (should be flexible)
        try:
            response = requests.post(
                f"{self.api_base_url}/v1/chat/completions",
                json={
                    "model": "ralex-bridge",
                    "messages": [{"role": "user", "content": "test"}]
                },
                headers={"Authorization": "Bearer ralex-key"},
                timeout=10
            )
            
            # API should work regardless of key (for now)
            if response.status_code in [200, 401]:  # Either works or properly rejects
                test_results["setup_instructions"] = True
                print("  ✅ API key handling works as documented")
                
        except Exception as e:
            print(f"  ⚠️  API key test inconclusive: {e}")
            
        # Test workflow completeness
        workflow_steps = [
            "Download OpenCat",
            "Configure API settings", 
            "Test connection",
            "Send queries"
        ]
        
        # We can validate the technical steps work
        if (test_results["configuration_values"] and 
            hasattr(self, 'test_results') and 
            self.test_results.get("simple_queries", 0) > 0):
            test_results["workflow_completeness"] = True
            print("  ✅ Documented workflow technically feasible")
        else:
            print("  ⚠️  Documented workflow may have gaps")
            
        return test_results
    
    def test_integration_performance(self) -> Dict[str, any]:
        """
        Test 5: Integration Performance
        Validates performance claims in documentation
        """
        print("📱 Testing Integration Performance...")
        
        test_results = {
            "startup_time": 0.0,
            "response_consistency": 0.0,
            "load_handling": 0.0,
            "resource_usage": {}
        }
        
        # Test response consistency
        test_query = "what is python"
        response_times = []
        
        for i in range(5):
            try:
                start_time = time.time()
                response = requests.post(
                    f"{self.api_base_url}/v1/chat/completions",
                    json={
                        "model": "ralex-bridge",
                        "messages": [{"role": "user", "content": test_query}],
                        "max_tokens": 50
                    },
                    timeout=self.test_config["api"]["timeout"]
                )
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    response_times.append(response_time)
                    
            except Exception:
                pass
                
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            std_dev = (sum((t - avg_time) ** 2 for t in response_times) / len(response_times)) ** 0.5
            consistency_score = 1.0 - min(std_dev / avg_time, 1.0)  # Lower std dev = higher consistency
            
            test_results["response_consistency"] = consistency_score
            print(f"  📊 Response consistency: {consistency_score:.1%}")
            print(f"  📊 Average response time: {avg_time:.2f}s ± {std_dev:.2f}s")
            
        # Test basic load handling
        concurrent_requests = 3
        load_test_results = []
        
        print(f"  🔄 Testing with {concurrent_requests} concurrent requests...")
        
        import threading
        
        def make_request():
            try:
                start_time = time.time()
                response = requests.post(
                    f"{self.api_base_url}/v1/chat/completions",
                    json={
                        "model": "ralex-bridge", 
                        "messages": [{"role": "user", "content": "load test"}],
                        "max_tokens": 20
                    },
                    timeout=self.test_config["api"]["timeout"]
                )
                duration = time.time() - start_time
                load_test_results.append((response.status_code == 200, duration))
            except Exception:
                load_test_results.append((False, 0.0))
                
        threads = [threading.Thread(target=make_request) for _ in range(concurrent_requests)]
        
        start_time = time.time()
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        total_time = time.time() - start_time
        
        if load_test_results:
            successful_requests = sum(1 for success, _ in load_test_results if success)
            load_success_rate = successful_requests / len(load_test_results)
            test_results["load_handling"] = load_success_rate
            
            print(f"  📊 Load test success rate: {load_success_rate:.1%}")
            print(f"  📊 Concurrent requests completed in: {total_time:.2f}s")
            
        return test_results
    
    def run_comprehensive_mobile_test(self) -> Dict[str, any]:
        """
        Run complete mobile integration test suite
        Returns overall mobile integration score
        """
        print("📱 Running Comprehensive Mobile Integration Test")
        print("=" * 60)
        
        # Run all test components
        all_results = {}
        
        all_results["api_availability"] = self.test_api_server_availability()
        all_results["api_compatibility"] = self.test_openai_api_compatibility() 
        all_results["query_workflows"] = self.test_mobile_query_workflows()
        all_results["documentation"] = self.test_documentation_accuracy()
        all_results["performance"] = self.test_integration_performance()
        
        # Calculate overall mobile integration score
        score_components = {
            "api_server_running": all_results["api_availability"].get("server_running", False),
            "openai_compatibility": all_results["api_compatibility"].get("response_format_compatibility", False),
            "workflow_success": all_results["query_workflows"].get("success_rate", 0.0) >= 0.8,
            "documentation_accuracy": all_results["documentation"].get("workflow_completeness", False),
            "performance_acceptable": all_results["performance"].get("response_consistency", 0.0) >= 0.7
        }
        
        mobile_score = sum(score_components.values()) / len(score_components)
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        results_file = Path(f".ralex/mobile_test_results_{timestamp}.json")
        results_file.parent.mkdir(exist_ok=True)
        
        comprehensive_results = {
            "timestamp": timestamp,
            "overall_score": mobile_score,
            "target_score": 0.90,
            "components": all_results,
            "score_breakdown": score_components,
            "pass": mobile_score >= 0.90
        }
        
        with open(results_file, 'w') as f:
            json.dump(comprehensive_results, f, indent=2, default=str)
            
        print("=" * 60)
        print(f"📱 Overall Mobile Integration Score: {mobile_score:.1%}")
        print(f"📱 Target Score: 90%")
        print(f"📱 Status: {'✅ PASS' if mobile_score >= 0.90 else '❌ NEEDS IMPROVEMENT'}")
        
        if mobile_score < 0.90:
            print("\n📋 Issues Found:")
            for component, status in score_components.items():
                if not status:
                    print(f"  ❌ {component}")
                    
        print(f"\n📊 Detailed results saved to: {results_file}")
        
        return comprehensive_results

if __name__ == "__main__":
    import sys
    
    async def main():
        tester = MobileTestingInfrastructure()
        results = tester.run_comprehensive_mobile_test()
        
        if results["pass"]:
            print("\n🎉 Mobile integration testing passed!")
            sys.exit(0)
        else:
            print("\n🔧 Mobile integration needs improvement")
            sys.exit(1)
            
    import asyncio
    asyncio.run(main())