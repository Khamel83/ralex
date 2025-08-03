import re


class CommandParser:
    def __init__(self):
        self.safe_operations = [
            "read_file",
            "write_file",
            "list_directory",
            "fix_bug",
            "create_component",
            "run_tests",
            "review_code",
            "explain_code",
        ]

    def parse(self, command: str) -> dict:
        command_lower = command.lower()
        parsed_command = {
            "original_command": command,
            "intent": "default",
            "params": {},
        }

        # Pattern for "read file <path>"
        # Pattern for "read file <path>"
        match = re.match(r"read file (.+)", command)
        if match:
            parsed_command["intent"] = "read_file"
            parsed_command["params"]["file_path"] = match.group(1).strip()
            return parsed_command

        # Pattern for "write file <path> with content <content>"
        match = re.match(r"write file (.+) with content (.+)", command)
        if match:
            parsed_command["intent"] = "write_file"
            parsed_command["params"]["file_path"] = match.group(1).strip()
            parsed_command["params"]["content"] = match.group(2).strip()
            return parsed_command

        # Pattern for "fix bug in <path>"
        match = re.match(r"fix bug in (.+)", command)
        if match:
            parsed_command["intent"] = "fix_bug"
            parsed_command["params"]["file_path"] = match.group(1).strip()
            return parsed_command

        # Pattern for "create component named <name>"
        match = re.match(r"create component named (.+)", command)
        if match:
            parsed_command["intent"] = "create_component"
            parsed_command["params"]["name"] = match.group(1).strip()
            return parsed_command

        # Simple keyword-based intent classification for other commands
        if "list directory" in command_lower:
            parsed_command["intent"] = "list_directory"
        elif "run tests" in command_lower:
            parsed_command["intent"] = "run_tests"
        elif "review code" in command_lower:
            parsed_command["intent"] = "review_code"
        elif "explain code" in command_lower:
            parsed_command["intent"] = "explain_code"

        return parsed_command

    def validate_command(self, parsed_command: dict) -> bool:
        intent = parsed_command.get("intent")
        return intent in self.safe_operations

    def classify_complexity(self, parsed_command: dict) -> str:
        intent = parsed_command.get("intent")
        if intent in ["read_file", "list_directory"]:
            return "low"
        elif intent in ["write_file", "run_tests", "explain_code"]:
            return "medium"
        elif intent in ["fix_bug", "create_component", "review_code"]:
            return "high"
        return "medium"  # Default for "default" intent or unclassified
