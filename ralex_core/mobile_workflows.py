import json
import os
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class MobileWorkflowManager:
    def __init__(self, templates_dir: str):
        self.templates_dir = templates_dir
        os.makedirs(templates_dir, exist_ok=True)

    def load_workflow_template(self, template_name: str) -> Optional[Dict]:
        """Loads a mobile workflow template from a JSON file."""
        file_path = os.path.join(self.templates_dir, f"{template_name}.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    template = json.load(f)
                logger.info(f"Loaded mobile workflow template: {template_name}")
                return template
            except Exception as e:
                logger.error(f"Failed to load template {template_name}: {e}")
                return None
        logger.warning(f"Mobile workflow template {template_name} not found.")
        return None

    def list_available_templates(self) -> List[str]:
        """Lists all available mobile workflow template names."""
        templates = []
        for filename in os.listdir(self.templates_dir):
            if filename.endswith(".json"):
                templates.append(filename[:-len(".json")])
        return templates

    def generate_workflow_prompt(self, template_name: str, user_input: str, context: Dict) -> Optional[str]:
        """Generates a tailored prompt based on a workflow template and user input."""
        template = self.load_workflow_template(template_name)
        if not template:
            return None

        prompt_template = template.get("prompt_template", "")
        
        # Basic placeholder for prompt generation. More complex logic would involve
        # filling placeholders from user_input and context.
        full_prompt = prompt_template.format(user_input=user_input, **context)
        logger.info(f"Generated workflow prompt for {template_name}.")
        return full_prompt

    def create_workflow_template(self, template_name: str, template_data: Dict) -> bool:
        """Creates a new mobile workflow template file."""
        file_path = os.path.join(self.templates_dir, f"{template_name}.json")
        try:
            with open(file_path, 'w') as f:
                json.dump(template_data, f, indent=4)
            logger.info(f"Created new mobile workflow template: {template_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create template {template_name}: {e}")
            return False

# Example Usage (for testing/demonstration)
if __name__ == "__main__":
    # Setup a temporary directory for templates
    templates_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.agent-os', 'mobile'))
    os.makedirs(templates_base_dir, exist_ok=True)

    manager = MobileWorkflowManager(templates_base_dir)

    # Create an example template
    example_template_data = {
        "name": "Refactor Function",
        "description": "Workflow for refactoring a Python function.",
        "prompt_template": "Refactor the following Python function: {user_input}. Consider the following context: {file_content}",
        "expected_output": "Refactored Python code and explanation."
    }
    manager.create_workflow_template("refactor_python", example_template_data)

    # List available templates
    print("\nAvailable Templates:")
    for template in manager.list_available_templates():
        print(f"- {template}")

    # Load and generate a prompt from a template
    user_code = "def old_function(a, b): return a + b"
    file_context = {"file_content": "# main.py\n" + user_code}
    generated_prompt = manager.generate_workflow_prompt("refactor_python", user_code, file_context)
    print(f"\nGenerated Prompt:\n{generated_prompt}")

    # Clean up temporary directory
    import shutil
    shutil.rmtree(templates_base_dir)
    print(f"\nCleaned up test directory: {templates_base_dir}")
