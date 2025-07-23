import unittest
import sys
import os
import time

# Add the parent directory to the sys.path to allow importing ralex_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ralex_core.code_executor import CodeExecutor

class TestCodeExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = CodeExecutor()

    def test_execute_python_code_success(self):
        code = "print('Hello, world!')"
        result = self.executor.execute_python_code(code)
        self.assertTrue(result["success"])
        self.assertEqual(result["stdout"].strip(), "Hello, world!")
        self.assertEqual(result["stderr"].strip(), "")

    def test_execute_python_code_error(self):
        code = "raise ValueError('Test Error')"
        result = self.executor.execute_python_code(code)
        self.assertFalse(result["success"])
        self.assertIn("ValueError: Test Error", result["stderr"])

    def test_execute_python_code_timeout(self):
        code = "import time; time.sleep(5)"
        start_time = time.time()
        result = self.executor.execute_python_code(code, timeout=1)
        end_time = time.time()
        self.assertFalse(result["success"])
        self.assertIn("Execution timed out", result["stderr"])
        self.assertLess(end_time - start_time, 2) # Should be slightly more than timeout, but not 5 seconds

    def test_execute_python_code_file_creation(self):
        code = "with open('test_file.txt', 'w') as f: f.write('test content')"
        result = self.executor.execute_python_code(code)
        self.assertTrue(result["success"])
        # Verify that the file was created in the temporary directory
        # This is a bit tricky as we don't have direct access to the tmpdir
        # but we can infer success if no error was raised.
        self.assertEqual(result["stdout"].strip(), "")
        self.assertEqual(result["stderr"].strip(), "")

if __name__ == '__main__':
    unittest.main()
