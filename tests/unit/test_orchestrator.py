import unittest
from unittest.mock import MagicMock, patch
from ralex_core.v4_orchestrator import RalexV4Orchestrator
import os

class TestRalexOrchestrator(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Mock dependencies
        self.mock_context_manager = MagicMock()
        self.mock_opencode_client = MagicMock()
        self.mock_litellm_router = MagicMock()
        self.mock_agentos_enhancer = MagicMock()
        self.mock_git_sync_manager = MagicMock()
        self.mock_command_parser = MagicMock()
        self.mock_security_manager = MagicMock()
        self.mock_error_handler = MagicMock()
        self.mock_workflow_engine = MagicMock()

        # Patch the constructor to inject mocks
        with patch.multiple(
            'ralex_core.orchestrator',
            ContextManager=MagicMock(return_value=self.mock_context_manager),
            OpenCodeClient=MagicMock(return_value=self.mock_opencode_client),
            LiteLLMRouter=MagicMock(return_value=self.mock_litellm_router),
            AgentOSEnhancer=MagicMock(return_value=self.mock_agentos_enhancer),
            GitSyncManager=MagicMock(return_value=self.mock_git_sync_manager),
            CommandParser=MagicMock(return_value=self.mock_command_parser),
            SecurityManager=MagicMock(return_value=self.mock_security_manager),
            ErrorHandler=MagicMock(return_value=self.mock_error_handler),
            WorkflowEngine=MagicMock(return_value=self.mock_workflow_engine)
        ),
        patch('os.getcwd', return_value="/mock/project/path"),
        patch('ralex_core.orchestrator.load_config', side_effect=lambda x: {
            os.path.join("/mock/project/path", "config", "model_tiers.json"): {"cheap": [{"name": "mock_cheap_model"}], "premium": [{"name": "mock_premium_model"}], "standard": [{"name": "gpt-3.5-turbo"}]},
            os.path.join("/mock/project/path", "config", "workflows.yaml"): {"example_workflow": {"description": "An example workflow", "steps": []}}
        }.get(x, {})):
            self.orchestrator = RalexOrchestrator()

    async def test_process_voice_command_read_file_success(self):
        self.mock_command_parser.parse.return_value = {"intent": "read_file", "params": {"file_path": "test.txt"}}
        self.mock_security_manager.validate_command.return_value = True
        self.mock_security_manager.is_dangerous_command.return_value = False
        async def mock_enhance(command, session_id):
            return "enhanced command"
        self.mock_agentos_enhancer.enhance.side_effect = mock_enhance
        async def mock_route(query, complexity):
            return "model response"
        self.mock_litellm_router.route.side_effect = mock_route
        self.mock_opencode_client.read_file.return_value = {"stdout": "file content", "stderr": "", "returncode": 0}
        self.mock_context_manager.get_context.return_value = ""

        result = await self.orchestrator.process_voice_command("read file test.txt", "session1")
        self.assertEqual(result["output"], "file content")
        self.mock_command_parser.parse.assert_called_once_with("read file test.txt")
        self.mock_security_manager.validate_command.assert_called_once()
        self.mock_agentos_enhancer.enhance.assert_called_once_with("read file test.txt", "session1")
        self.mock_litellm_router.route.assert_called_once_with("enhanced command", self.mock_command_parser.classify_complexity.return_value)
        self.mock_opencode_client.read_file.assert_called_once_with("test.txt")
        self.mock_context_manager.update_context.assert_called_once()
        self.mock_security_manager.audit_operation.assert_called_once()

    async def test_process_voice_command_write_file_success(self):
        self.mock_command_parser.parse.return_value = {"intent": "write_file", "params": {"file_path": "new.txt", "content": "hello"}}
        self.mock_security_manager.validate_command.return_value = True
        self.mock_security_manager.is_dangerous_command.return_value = False
        async def mock_enhance_write(command, session_id):
            return "enhanced command for write"
        self.mock_agentos_enhancer.enhance.side_effect = mock_enhance_write
        async def mock_route_write(query, complexity):
            return "model response for write"
        self.mock_litellm_router.route.side_effect = mock_route_write
        self.mock_context_manager.get_context.return_value = ""
        self.mock_opencode_client.write_file.return_value = {"stdout": "", "stderr": "", "returncode": 0}

        result = await self.orchestrator.process_voice_command("write file new.txt with content hello", "session1")
        self.assertIn("Successfully wrote to new.txt", result["output"])
        self.mock_opencode_client.write_file.assert_called_once_with("new.txt", "hello")

    async def test_process_voice_command_invalid_command(self):
        self.mock_command_parser.parse.return_value = {"intent": "malicious_command"}
        self.mock_security_manager.validate_command.return_value = False

        result = await self.orchestrator.process_voice_command("delete all files", "session1")

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Command not allowed.")
        self.mock_security_manager.validate_command.assert_called_once()

    async def test_process_voice_command_dangerous_command(self):
        self.mock_command_parser.parse.return_value = {"intent": "delete_all"}
        self.mock_security_manager.validate_command.return_value = True # Assume it passes initial validation
        self.mock_security_manager.is_dangerous_command.return_value = True

        result = await self.orchestrator.process_voice_command("rm -rf /", "session1")

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Dangerous command detected. Manual confirmation required.")
        self.assertEqual(result["user_message"], "This command is potentially dangerous. Please confirm manually if you wish to proceed.")
        self.mock_security_manager.is_dangerous_command.assert_called_once_with(self.mock_command_parser.parse.return_value)

    async def test_process_voice_command_error_handling(self):
        self.mock_command_parser.parse.side_effect = Exception("Parsing error")
        self.mock_error_handler.get_user_friendly_message.return_value = "User friendly error"

        result = await self.orchestrator.process_voice_command("some command", "session1")

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["user_message"], "User friendly error")
        self.mock_error_handler.handle_error.assert_called_once()

    async def test_execute_workflow_success(self):
        self.mock_workflow_engine.get_workflow.return_value = {
            "description": "Test workflow",
            "steps": [
                {"step1": "Do something"},
                {"step2": "Do something else"}
            ]
        }

        result = await self.orchestrator.execute_workflow("test_workflow", {})

        self.assertEqual(result["status"], "success")
        self.assertIn("Executing workflow step: step1 - Do something", result["output"])
        self.assertIn("Executing workflow step: step2 - Do something else", result["output"])
        self.mock_workflow_engine.get_workflow.assert_called_once_with("test_workflow")

    async def test_execute_workflow_not_found(self):
        self.mock_workflow_engine.get_workflow.return_value = None

        result = await self.orchestrator.execute_workflow("non_existent_workflow", {})

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Workflow 'non_existent_workflow' not found.")

    async def test_execute_workflow_error_handling(self):
        self.mock_workflow_engine.get_workflow.side_effect = Exception("Workflow error")
        self.mock_error_handler.get_user_friendly_message.return_value = "Workflow user friendly error"

        result = await self.orchestrator.execute_workflow("some_workflow", {})

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["user_message"], "Workflow user friendly error")
        self.mock_error_handler.handle_error.assert_called_once()

if __name__ == '__main__':
    unittest.main()