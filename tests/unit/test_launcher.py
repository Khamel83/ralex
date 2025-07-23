import unittest
import os
import sys
import json
from unittest.mock import patch, mock_open

# Add the parent directory to the sys.path to allow importing ralex_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ralex_core.launcher import parse_file_modifications, parse_code_blocks, load_config, classify_intent

class TestLauncherFunctions(unittest.TestCase):

    def test_parse_file_modifications(self):
        response_text = """
Some text before.
```path/to/file1.py
# content of file1
line 2 of file1
```
Some text in between.
```another/file.txt
new content for another file
```
Some text after.
"""
        modifications = parse_file_modifications(response_text)
        expected = {
            "path/to/file1.py": "# content of file1\nline 2 of file1",
            "another/file.txt": "new content for another file"
        }
        self.assertEqual(modifications, expected)

    def test_parse_file_modifications_no_blocks(self):
        response_text = "Just some regular text without code blocks."
        modifications = parse_file_modifications(response_text)
        self.assertEqual(modifications, {})

    def test_parse_code_blocks(self):
        response_text = """
Assistant output.
```python
print('Hello')
```
More text.
```bash
ls -l
```
End.
"""
        code_blocks = parse_code_blocks(response_text)
        expected = [
            {"language": "python", "code": "print('Hello')"},
            {"language": "bash", "code": "ls -l"}
        ]
        self.assertEqual(code_blocks, expected)

    def test_parse_code_blocks_no_blocks(self):
        response_text = "No code here."
        code_blocks = parse_code_blocks(response_text)
        self.assertEqual(code_blocks, [])

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_config_success(self, mock_file):
        config = load_config("config.json")
        self.assertEqual(config, {"key": "value"})

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.exit')
    def test_load_config_file_not_found(self, mock_exit, mock_open):
        with self.assertRaises(SystemExit):
            load_config("non_existent.json")
        mock_exit.assert_called_once_with(1)

    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('sys.exit')
    def test_load_config_invalid_json(self, mock_exit, mock_open):
        with self.assertRaises(SystemExit):
            load_config("invalid.json")
        mock_exit.assert_called_once_with(1)

    def test_classify_intent(self):
        self.assertEqual(classify_intent("fix a bug"), "debug")
        self.assertEqual(classify_intent("create a new feature"), "generate")
        self.assertEqual(classify_intent("modify the code"), "edit")
        self.assertEqual(classify_intent("review my pull request"), "review")
        self.assertEqual(classify_intent("optimize this algorithm"), "optimize")
        self.assertEqual(classify_intent("format the file"), "format")
        self.assertEqual(classify_intent("explain this function"), "explain")
        self.assertEqual(classify_intent("what is this"), "default")

if __name__ == '__main__':
    unittest.main()
