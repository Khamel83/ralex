
import unittest
from ralex_core.command_parser import CommandParser

class TestCommandParser(unittest.TestCase):
    def setUp(self):
        self.parser = CommandParser()

    def test_parse_read_file(self):
        command = "read file /path/to/my/file.txt"
        parsed = self.parser.parse(command)
        self.assertEqual(parsed["intent"], "read_file")
        self.assertEqual(parsed["params"]["file_path"], "/path/to/my/file.txt")

    def test_parse_write_file(self):
        command = "write file /path/to/new/file.py with content print('Hello')"
        parsed = self.parser.parse(command)
        self.assertEqual(parsed["intent"], "write_file")
        self.assertEqual(parsed["params"]["file_path"], "/path/to/new/file.py")
        self.assertEqual(parsed["params"]["content"], "print('Hello')")

    def test_parse_fix_bug(self):
        command = "fix bug in src/main.py"
        parsed = self.parser.parse(command)
        self.assertEqual(parsed["intent"], "fix_bug")
        self.assertEqual(parsed["params"]["file_path"], "src/main.py")

    def test_parse_create_component(self):
        command = "create component named MyComponent"
        parsed = self.parser.parse(command)
        self.assertEqual(parsed["intent"], "create_component")
        self.assertEqual(parsed["params"]["name"], "MyComponent")

    def test_parse_list_directory(self):
        command = "list directory"
        parsed = self.parser.parse(command)
        self.assertEqual(parsed["intent"], "list_directory")

    def test_parse_default(self):
        command = "what is the weather like?"
        parsed = self.parser.parse(command)
        self.assertEqual(parsed["intent"], "default")

    def test_validate_safe_command(self):
        parsed = {"intent": "read_file"}
        self.assertTrue(self.parser.validate_command(parsed))

    def test_validate_unsafe_command(self):
        # Assuming 'delete_all' is not in safe_operations
        parsed = {"intent": "delete_all"}
        self.assertFalse(self.parser.validate_command(parsed))

    def test_classify_complexity_low(self):
        parsed = {"intent": "read_file"}
        self.assertEqual(self.parser.classify_complexity(parsed), "low")

    def test_classify_complexity_medium(self):
        parsed = {"intent": "write_file"}
        self.assertEqual(self.parser.classify_complexity(parsed), "medium")

    def test_classify_complexity_high(self):
        parsed = {"intent": "fix_bug"}
        self.assertEqual(self.parser.classify_complexity(parsed), "high")

    def test_classify_complexity_default(self):
        parsed = {"intent": "unknown_intent"}
        self.assertEqual(self.parser.classify_complexity(parsed), "medium")

if __name__ == '__main__':
    unittest.main()
