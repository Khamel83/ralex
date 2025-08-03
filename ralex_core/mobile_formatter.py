import logging
import re
from typing import Dict

logger = logging.getLogger(__name__)

class MobileResponseFormatter:
    def __init__(self):
        pass

    def format_code_for_mobile(self, code_content: str, language: str = "python") -> str:
        """Applies mobile-optimized formatting to code blocks, including basic syntax highlighting simulation."""
        # This is a simplified simulation of syntax highlighting for text-based output.
        # In a real mobile app, this would be handled by the UI framework.
        highlighted_code = []
        keywords = {
            "python": ["def", "class", "import", "from", "if", "else", "elif", "for", "while", "return", "True", "False", "None"],
            "bash": ["#!/bin/bash", "ls", "cd", "mkdir", "rm", "cp", "mv", "echo", "export"],
            # Add more languages and keywords as needed
        }

        for line in code_content.splitlines():
            formatted_line = line
            for keyword in keywords.get(language, []):
                formatted_line = re.sub(r'\b' + re.escape(keyword) + r'\b', f'**{keyword}**', formatted_line) # Bold keywords
            highlighted_code.append(formatted_line)
        
        return "\n".join(highlighted_code)

    def make_collapsible(self, content: str, title: str = "Details") -> str:
        """Wraps content in a markdown-like collapsible block for mobile display."""
        # This is a conceptual representation. Actual mobile UI would render this.
        return f"<details><summary>{title}</summary>\n\n{content}\n\n</details>"

    def format_file_preview(self, file_content: str, lines: int = 5) -> str:
        """Generates a short preview of a file's content."""
        preview_lines = file_content.splitlines()[:lines]
        return "\n".join(preview_lines) + ("\n..." if len(file_content.splitlines()) > lines else "")

    def optimize_markdown_for_mobile(self, markdown_content: str) -> str:
        """Optimizes general markdown content for mobile readability."""
        # Example: Reduce excessive newlines, ensure images are responsive (conceptual)
        optimized_content = re.sub(r'\n{3,}', '\n\n', markdown_content) # Reduce multiple newlines
        # More complex markdown parsing and reformatting would go here
        return optimized_content

# Example Usage (for testing/demonstration)
if __name__ == "__main__":
    formatter = MobileResponseFormatter()

    # Test code formatting
    python_code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
"""
    formatted_python = formatter.format_code_for_mobile(python_code, "python")
    print("\n--- Formatted Python Code ---")
    print(formatted_python)

    bash_code = """
#!/bin/bash
ls -la
mkdir new_dir
echo "Hello World"
"""
    formatted_bash = formatter.format_code_for_mobile(bash_code, "bash")
    print("\n--- Formatted Bash Code ---")
    print(formatted_bash)

    # Test collapsible content
    collapsible_text = "This is some detailed information that can be hidden."
    collapsible_block = formatter.make_collapsible(collapsible_text, "Show More Info")
    print("\n--- Collapsible Block ---")
    print(collapsible_block)

    # Test file preview
    long_file_content = """
Line 1
Line 2
Line 3
Line 4
Line 5
Line 6
Line 7
"""
    file_preview = formatter.format_file_preview(long_file_content, lines=3)
    print("\n--- File Preview ---")
    print(file_preview)

    # Test markdown optimization
    raw_markdown = """
# Title



Paragraph 1


Paragraph 2
"""
    optimized_markdown = formatter.optimize_markdown_for_mobile(raw_markdown)
    print("\n--- Optimized Markdown ---")
    print(optimized_markdown)

