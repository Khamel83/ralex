import unittest
import os
import json
from datetime import datetime, timedelta
import sys

# Add the parent directory to the sys.path to allow importing ralex_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ralex_core.budget_optimizer import BudgetOptimizer

class TestBudgetOptimizer(unittest.TestCase):
    def setUp(self):
        self.test_log_path = "data/test_usage_log.jsonl"
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(self.test_log_path), exist_ok=True)
        if os.path.exists(self.test_log_path):
            os.remove(self.test_log_path)
        self.budget_optimizer = BudgetOptimizer(usage_log_path=self.test_log_path, daily_limit=10.0)

    def tearDown(self):
        if os.path.exists(self.test_log_path):
            os.remove(self.test_log_path)

    def test_record_usage(self):
        self.budget_optimizer.record_usage("model_a", 100, 50, 0.01)
        self.assertTrue(os.path.exists(self.test_log_path))
        with open(self.test_log_path, "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            record = json.loads(lines[0])
            self.assertEqual(record["model"], "model_a")
            self.assertEqual(record["cost"], 0.01)

    def test_get_total_spent(self):
        self.assertEqual(self.budget_optimizer.get_total_spent(), 0.0)
        self.budget_optimizer.record_usage("model_a", 100, 50, 0.01)
        self.budget_optimizer.record_usage("model_b", 200, 100, 0.02)
        self.assertEqual(self.budget_optimizer.get_total_spent(), 0.03)

    def test_get_spent_today(self):
        # Record usage for today
        self.budget_optimizer.record_usage("model_a", 100, 50, 0.01)
        self.budget_optimizer.record_usage("model_b", 200, 100, 0.02)
        self.assertEqual(self.budget_optimizer.get_spent_today(), 0.03)

        # Record usage for yesterday (should not be counted)
        yesterday = datetime.now() - timedelta(days=1)
        with open(self.test_log_path, "a") as f:
            record = {
                "timestamp": yesterday.isoformat(),
                "model": "model_c",
                "tokens_sent": 50, "tokens_received": 25, "cost": 0.005
            }
            f.write(json.dumps(record) + "\n")
        self.assertEqual(self.budget_optimizer.get_spent_today(), 0.03)

    def test_check_budget_status_safe(self):
        self.budget_optimizer.record_usage("model_a", 100, 50, 1.0)
        status = self.budget_optimizer.check_budget_status()
        self.assertEqual(status["status"], "safe")
        self.assertAlmostEqual(status["spent_today"], 1.0)
        self.assertEqual(status["daily_limit"], 10.0)

    def test_check_budget_status_warning(self):
        self.budget_optimizer.record_usage("model_a", 100, 50, 8.5)
        status = self.budget_optimizer.check_budget_status()
        self.assertEqual(status["status"], "warning")
        self.assertAlmostEqual(status["spent_today"], 8.5)

    def test_check_budget_status_exceeded(self):
        self.budget_optimizer.record_usage("model_a", 100, 50, 10.5)
        status = self.budget_optimizer.check_budget_status()
        self.assertEqual(status["status"], "exceeded")
        self.assertAlmostEqual(status["spent_today"], 10.5)

    def test_check_budget_status_no_limit(self):
        budget_optimizer_no_limit = BudgetOptimizer(usage_log_path=self.test_log_path, daily_limit=None)
        budget_optimizer_no_limit.record_usage("model_a", 100, 50, 1.0)
        status = budget_optimizer_no_limit.check_budget_status()
        self.assertEqual(status["status"], "no_limit")
        self.assertAlmostEqual(status["spent_today"], 1.0)
        self.assertIsNone(status["daily_limit"])

if __name__ == '__main__':
    unittest.main()
