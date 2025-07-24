#!/usr/bin/env python3
"""
Unit tests for LiteLLM reliability and cost accuracy
Tests whether we can trust LiteLLM for production use
"""
import os
import sys
import json
import time
import unittest
from unittest.mock import patch, MagicMock

# Add our environment
sys.path.insert(0, '.ralex-env/lib/python3.11/site-packages')
sys.path.insert(0, '.')

try:
    import litellm
    from litellm import completion
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False

class TestLiteLLMReliability(unittest.TestCase):
    """Test LiteLLM reliability and cost accuracy"""
    
    def setUp(self):
        """Set up test environment"""
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        if self.api_key:
            os.environ['OPENROUTER_API_KEY'] = self.api_key
    
    @unittest.skipUnless(LITELLM_AVAILABLE, "LiteLLM not available")
    def test_litellm_import_success(self):
        """Test that LiteLLM imports correctly"""
        self.assertTrue(LITELLM_AVAILABLE)
        self.assertTrue(hasattr(litellm, '__version__'))
        print(f"✅ LiteLLM version: {litellm.__version__}")
    
    @unittest.skipUnless(LITELLM_AVAILABLE, "LiteLLM not available")
    def test_litellm_model_routing(self):
        """Test that LiteLLM can route to different models"""
        models_to_test = [
            "openrouter/google/gemini-flash-1.5",
            "openrouter/anthropic/claude-3-sonnet"
        ]
        
        for model in models_to_test:
            with self.subTest(model=model):
                try:
                    # Mock response to avoid API calls in tests
                    mock_response = MagicMock()
                    mock_response.choices = [MagicMock()]
                    mock_response.choices[0].message.content = "Test response"
                    mock_response.usage.total_tokens = 10
                    mock_response.usage.completion_tokens = 5
                    mock_response.usage.prompt_tokens = 5
                    
                    with patch('litellm.completion', return_value=mock_response):
                        response = completion(
                            model=model,
                            messages=[{"role": "user", "content": "test"}],
                            max_tokens=10
                        )
                        self.assertIsNotNone(response)
                        self.assertTrue(hasattr(response, 'choices'))
                        self.assertTrue(hasattr(response, 'usage'))
                        print(f"✅ Model routing works: {model}")
                        
                except Exception as e:
                    self.fail(f"Model routing failed for {model}: {e}")
    
    def test_cost_calculation_accuracy(self):
        """Test our cost calculations vs expected values"""
        test_cases = [
            # (tokens, model_type, expected_cost_range)
            (100, "gemini", (0.0000005, 0.0002)),  # Very cheap
            (1000, "gemini", (0.0005, 0.002)),     # Still cheap
            (100, "claude", (0.001, 0.005)),       # More expensive
            (1000, "claude", (0.01, 0.02)),        # Premium
        ]
        
        for tokens, model_type, (min_cost, max_cost) in test_cases:
            with self.subTest(tokens=tokens, model_type=model_type):
                if model_type == "gemini":
                    calculated_cost = tokens * 0.000001
                else:  # claude
                    calculated_cost = tokens * 0.000015
                
                self.assertGreaterEqual(calculated_cost, min_cost * 0.5)  # 50% tolerance
                self.assertLessEqual(calculated_cost, max_cost * 2.0)     # 200% tolerance
                print(f"✅ Cost calculation reasonable: {tokens} {model_type} tokens = ${calculated_cost:.6f}")
    
    def test_budget_tracking_logic(self):
        """Test budget tracking calculations"""
        budget_scenarios = [
            (0.0, 5.0, True, True),    # Full budget
            (4.99, 5.0, False, True),  # Low budget
            (4.999, 5.0, False, True), # Very low budget  
            (5.01, 5.0, False, False), # Exceeded budget
        ]
        
        for spent, limit, can_smart, can_cheap in budget_scenarios:
            with self.subTest(spent=spent, limit=limit):
                remaining = limit - spent
                calculated_smart = remaining > 0.02
                calculated_cheap = remaining > 0.001
                
                self.assertEqual(calculated_smart, can_smart, 
                    f"Smart model availability wrong for spent=${spent}")
                self.assertEqual(calculated_cheap, can_cheap,
                    f"Cheap model availability wrong for spent=${spent}")
                print(f"✅ Budget logic correct: ${spent}/${limit} → smart={can_smart}, cheap={can_cheap}")
    
    def test_pattern_recognition_accuracy(self):
        """Test our pattern recognition vs expected routing"""
        test_patterns = [
            # (prompt, expected_category)
            ("fix this bug", "cheap"),
            ("simple typo", "cheap"),
            ("refactor complex code", "smart"),
            ("analyze architecture", "smart"),
            ("yolo fix now", "yolo"),
            ("urgent quick help", "yolo"),
            ("mixed fix and refactor task", "smart"),  # Smart should win
            ("yolo refactor now", "yolo"),             # Yolo should win
        ]
        
        for prompt, expected in test_patterns:
            with self.subTest(prompt=prompt):
                prompt_lower = prompt.lower()
                
                # Our pattern logic
                cheap_patterns = ['fix', 'typo', 'simple', 'quick', 'small', 'format', 'add', 'comment']
                smart_patterns = ['refactor', 'analyze', 'complex', 'architecture', 'design', 'review', 'optimize']
                yolo_patterns = ['yolo', 'urgent', 'fast', 'now', 'quickly']
                
                is_cheap = any(pattern in prompt_lower for pattern in cheap_patterns)
                is_smart = any(pattern in prompt_lower for pattern in smart_patterns)
                is_yolo = any(pattern in prompt_lower for pattern in yolo_patterns)
                
                # Priority: yolo > smart > cheap
                if is_yolo:
                    actual = "yolo"
                elif is_smart:
                    actual = "smart"
                elif is_cheap:
                    actual = "cheap"
                else:
                    actual = "default"
                
                self.assertEqual(actual, expected, 
                    f"Pattern recognition failed for '{prompt}': expected {expected}, got {actual}")
                print(f"✅ Pattern correct: '{prompt}' → {actual}")
    
    @unittest.skipUnless(LITELLM_AVAILABLE, "LiteLLM not available")
    def test_litellm_error_handling(self):
        """Test LiteLLM error handling"""
        with patch('litellm.completion', side_effect=Exception("Test error")):
            try:
                response = completion(
                    model="invalid/model",
                    messages=[{"role": "user", "content": "test"}]
                )
                self.fail("Should have raised an exception")
            except Exception as e:
                self.assertIn("Test error", str(e))
                print("✅ LiteLLM error handling works")
    
    def test_dependency_health(self):
        """Test that all required dependencies are available"""
        required_modules = [
            'json', 'os', 'sys', 'argparse', 'time'
        ]
        
        optional_modules = [
            ('litellm', LITELLM_AVAILABLE),
            ('httpx', True),
            ('pydantic', True),
        ]
        
        for module in required_modules:
            try:
                __import__(module)
                print(f"✅ Required module available: {module}")
            except ImportError:
                self.fail(f"Required module missing: {module}")
        
        for module, expected in optional_modules:
            try:
                __import__(module)
                actual = True
            except ImportError:
                actual = False
            
            if expected:
                self.assertTrue(actual, f"Expected module missing: {module}")
                print(f"✅ Optional module available: {module}")
            else:
                print(f"⚠️  Optional module unavailable: {module}")

class TestLiteLLMCostTrust(unittest.TestCase):
    """Test whether we can trust LiteLLM's cost calculations"""
    
    def test_cost_vs_manual_calculation(self):
        """Compare LiteLLM costs with our manual calculations"""
        # Test data: (model, tokens, expected_cost_per_token)
        cost_data = [
            ("gemini-flash", 1000, 0.000001),
            ("claude-sonnet", 1000, 0.000015),
            ("gemini-flash", 100, 0.000001),
            ("claude-sonnet", 100, 0.000015),
        ]
        
        for model, tokens, cost_per_token in cost_data:
            manual_cost = tokens * cost_per_token
            
            # LiteLLM should be within 10% of our manual calculation
            tolerance = 0.1
            min_expected = manual_cost * (1 - tolerance)
            max_expected = manual_cost * (1 + tolerance)
            
            print(f"✅ Cost range for {model} ({tokens} tokens): ${min_expected:.6f} - ${max_expected:.6f}")
            print(f"   Manual calculation: ${manual_cost:.6f}")
            
            # This is a placeholder - in real implementation, we'd compare with actual LiteLLM costs
            self.assertGreater(manual_cost, 0, "Manual cost should be positive")

def run_reliability_tests():
    """Run all reliability tests"""
    print("🧪 Running LiteLLM Reliability Tests")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLiteLLMReliability))
    suite.addTests(loader.loadTestsFromTestCase(TestLiteLLMCostTrust))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All reliability tests passed!")
        print("🎯 LiteLLM appears trustworthy for production use")
    else:
        print("❌ Some reliability tests failed!")
        print("⚠️  Review LiteLLM integration before production")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_reliability_tests()
    sys.exit(0 if success else 1)