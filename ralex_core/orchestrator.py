from .context_manager import ContextManager
from .opencode_client import OpenCodeClient
from .litellm_router import LiteLLMRouter
from .agentos_enhancer import AgentOSEnhancer
from .git_sync_manager import GitSyncManager
from .command_parser import CommandParser
from .security_manager import SecurityManager
from .error_handler import ErrorHandler
from .workflow_engine import WorkflowEngine
from .ccr_manager import CCRManager
import os
from tools.todo_writer import TodoWriter, Task # Import TodoWriter and Task

import requests

class RalexOrchestrator:
    def __init__(self):
        project_path = os.getcwd()
        self.context_manager = ContextManager(project_path)
        self.opencode_client = OpenCodeClient(project_path)
        self.agentos_enhancer = AgentOSEnhancer()
        self.git_sync_manager = GitSyncManager(project_path)
        self.command_parser = CommandParser()
        self.security_manager = SecurityManager()
        self.error_handler = ErrorHandler()
        self.ccr_manager = CCRManager()
        # Assuming a default workflows.yaml for now, will be configurable later
        self.workflow_engine = WorkflowEngine(os.path.join(project_path, "config", "workflows.yaml"))

        # Load model tiers and initialize budget optimizer
        config_dir = os.path.join(project_path, "config")
        # Import load_config function
        from ralex_core.launcher import load_config
        self.model_tiers = load_config(os.path.join(config_dir, "model_tiers.json"))
        from ralex_core.budget import BudgetManager
        self.budget_optimizer = BudgetManager(daily_limit=10.0) # Daily limit is a placeholder

        # Start CCR server
        if not self.ccr_manager.check_installation():
            self.ccr_manager.install()
        self.ccr_manager.start_server()

    async def process_claude_command(self, prompt: str) -> dict:
        if not self.ccr_manager.is_running():
            return {"status": "error", "message": "Claude Code Router is not running."}

        try:
            response = requests.post(
                f"http://localhost:{self.ccr_manager.port}",
                json={"prompt": prompt, "stream": True}
            )
            response.raise_for_status()
            # For now, we just return the whole response. Streaming would be implemented here.
            return {"status": "success", "output": response.text}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Failed to connect to Claude Code Router: {e}"}

    async def process_voice_command(self, command: str, session_id: str, assume_yes: bool = False, think_harder: bool = False) -> dict:
        try:
            # 1. Parse the command
            parsed_command = self.command_parser.parse(command)
            intent = parsed_command.get("intent", "default")
            params = parsed_command.get("params", {})

            # 2. Validate the command
            if not self.security_manager.validate_command(parsed_command):
                return {"status": "error", "message": "Command not allowed."}

            # Check for dangerous commands and ask for confirmation
            if not assume_yes and self.security_manager.is_dangerous_command(parsed_command):
                # In a real interactive CLI, you'd prompt the user here.
                # For now, we'll return an error indicating manual confirmation is needed.
                return {"status": "error", "message": "Dangerous command detected. Manual confirmation required.", "user_message": "This command is potentially dangerous. Please confirm manually if you wish to proceed."}

            # 3. Classify complexity
            complexity = self.command_parser.classify_complexity(parsed_command)

            # 4. Enhance the command (placeholder for AgentOS)
            enhanced_command = await self.agentos_enhancer.enhance(command, session_id)

            # 5. Route to the appropriate model (placeholder for LiteLLM)
            # For now, we'll just use the enhanced command as the query
            model_response = await self.litellm_router.route(enhanced_command, complexity, think_harder=think_harder)

            # 6. Execute the command based on intent
            execution_result = {"status": "success", "output": ""}
            if intent == "read_file":
                file_path = params.get("file_path")
                if file_path:
                    cmd_result = self.opencode_client.read_file(file_path)
                    if cmd_result["returncode"] == 0:
                        execution_result["output"] = cmd_result["stdout"]
                    else:
                        execution_result = {"status": "error", "message": f"Failed to read file: {cmd_result['stderr']}", "user_message": "Could not read the file. Please check the file path and permissions."}
                else:
                    execution_result = {"status": "error", "message": "File path not provided for read_file.", "user_message": "Please specify which file you want to read."}
            elif intent == "write_file":
                file_path = params.get("file_path")
                content = params.get("content")
                if file_path and content:
                    cmd_result = self.opencode_client.write_file(file_path, content)
                    if cmd_result["returncode"] == 0:
                        execution_result["output"] = f"Successfully wrote to {file_path}"
                    else:
                        execution_result = {"status": "error", "message": f"Failed to write file: {cmd_result['stderr']}", "user_message": "Could not write to the file. Please check the file path and permissions."}
                else:
                    execution_result = {"status": "error", "message": "File path or content not provided for write_file.", "user_message": "Please specify the file and content you want to write."}
            elif intent == "list_directory":
                cmd_result = self.opencode_client.execute_command("ls -F")
                if cmd_result["returncode"] == 0:
                    execution_result["output"] = cmd_result["stdout"]
                else:
                    execution_result = {"status": "error", "message": f"Failed to list directory: {cmd_result['stderr']}", "user_message": "Could not list the directory."}
            elif intent == "fix_bug":
                # This would involve more complex interaction with LLM and code execution
                execution_result["output"] = f"Attempting to fix bug in {params.get('file_path', 'unknown file')}. Model response: {model_response}"
            elif intent == "create_component":
                execution_result["output"] = f"Creating component {params.get('name', 'unknown component')}. Model response: {model_response}"
            elif intent == "run_tests":
                cmd_result = self.opencode_client.execute_command("pytest")
                if cmd_result["returncode"] == 0:
                    execution_result["output"] = cmd_result["stdout"]
                else:
                    execution_result = {"status": "error", "message": f"Tests failed: {cmd_result['stderr']}", "user_message": "Tests failed. Please check the output for details."}
            elif intent == "review_code":
                execution_result["output"] = f"Reviewing code. Model response: {model_response}"
            elif intent == "explain_code":
                execution_result["output"] = f"Explaining code. Model response: {model_response}"
            else:
                execution_result["output"] = f"Processed command: {command}. Model response: {model_response}"

            # 7. Update context
            current_context = self.context_manager.get_context(session_id)
            new_context = f"{current_context}\nUser: {command}\nAssistant: {execution_result.get('output', '')}"
            self.context_manager.update_context(session_id, new_context)

            # 8. Audit operation (placeholder)
            self.security_manager.audit_operation(parsed_command, execution_result)

            return execution_result

        except Exception as e:
            user_message = self.error_handler.get_user_friendly_message(e)
            self.error_handler.handle_error(e, context=command)
            return {"status": "error", "message": str(e), "user_message": user_message}

    async def execute_workflow(self, workflow_name: str, params: dict) -> dict:
        try:
            workflow = self.workflow_engine.get_workflow(workflow_name)
            if not workflow:
                return {"status": "error", "message": f"Workflow '{workflow_name}' not found."}

            # Simplified workflow execution: just print steps
            output = []
            for step in workflow.get("steps", []):
                step_description = list(step.keys())[0]
                step_detail = step[step_description]
                output.append(f"Executing workflow step: {step_description} - {step_detail}")
                
                if "tool_command" in step_detail:
                    tool_command_str = step_detail["tool_command"]
                    tool_result = await self._execute_tool_command(tool_command_str)
                    output.append(f"Tool command result: {tool_result}")

            return {"status": "success", "output": "\n".join(output)}

        except Exception as e:
            user_message = self.error_handler.get_user_friendly_message(e)
            self.error_handler.handle_error(e, context=f"workflow: {workflow_name}")
            return {"status": "error", "message": str(e), "user_message": user_message}

    def shutdown(self):
        self.ccr_manager.stop_server()