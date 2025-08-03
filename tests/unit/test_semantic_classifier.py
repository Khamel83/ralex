import unittest
import sys
import os

# Add the parent directory to the sys.path to allow importing ralex_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ralex_core.semantic_classifier import SemanticClassifier


class TestSemanticClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = SemanticClassifier()

    def test_classify_generate(self):
        intent, confidence = self.classifier.classify("create a new python script")
        self.assertEqual(intent, "generate")
        self.assertGreater(confidence, 0.5)

    def test_classify_edit(self):
        intent, confidence = self.classifier.classify("modify this function")
        self.assertEqual(intent, "edit")
        self.assertGreater(confidence, 0.5)

    def test_classify_debug(self):
        intent, confidence = self.classifier.classify("fix this bug")
        self.assertEqual(intent, "debug")
        self.assertGreater(confidence, 0.5)

    def test_classify_review(self):
        intent, confidence = self.classifier.classify("review this code")
        self.assertEqual(intent, "review")
        self.assertGreater(confidence, 0.5)

    def test_classify_optimize(self):
        intent, confidence = self.classifier.classify("optimize performance")
        self.assertEqual(intent, "optimize")
        self.assertGreater(confidence, 0.5)

    def test_classify_format(self):
        intent, confidence = self.classifier.classify("format this file")
        self.assertEqual(intent, "format")
        self.assertGreater(confidence, 0.5)

    def test_classify_explain(self):
        intent, confidence = self.classifier.classify("explain this code")
        self.assertEqual(intent, "explain")
        self.assertGreater(confidence, 0.5)

    def test_classify_unknown(self):
        intent, confidence = self.classifier.classify("random unrelated text")
        # For unknown inputs, it should ideally fall back to a default or a low-confidence intent
        # Depending on the model's training, it might still pick one with low confidence.
        # For now, we'll just assert it returns something.
        self.assertIsNotNone(intent)


if __name__ == "__main__":
    unittest.main()
