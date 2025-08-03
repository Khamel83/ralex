import unittest
import os
import sys
from unittest.mock import MagicMock, patch
from typing import Dict, List, Any

# Add the tools directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'tools')))


from todo_writer import TodoWriter, Task
from ralex_core.git_sync_manager import GitSyncManager


class TestTodoWriteAgentOSIntegration(unittest.TestCase):
    @patch('ralex_core.git_sync_manager.GitSyncManager')
    def test_complete_task_triggers_git_operations(self, MockGitManagerClass):
        # Move imports inside the test method to ensure patching takes effect
        from todo_writer import TodoWriter, Task

        # Initialize TodoWriter
        todo_writer = TodoWriter()

        # Configure the mock instance that todo_writer is using
        mock_git_manager_instance = MockGitManagerClass.return_value
        mock_git_manager_instance.committed_tasks = []
        mock_git_manager_instance.pushed = False
        mock_git_manager_instance.is_git_repo.return_value = True
        mock_git_manager_instance.commit_task_completion.side_effect = lambda task: (
            mock_git_manager_instance.committed_tasks.append(task),
            setattr(mock_git_manager_instance, 'pushed', True),
            {"success": True, "commit_hash": "mock_hash", "commit_message": "mock_message", "push_result": {"status": "success"}}
        )[2]
        todo_writer.git_manager = mock_git_manager_instance

        # Configure the mock instance
        mock_git_manager_instance.committed_tasks = []
        mock_git_manager_instance.pushed = False
        mock_git_manager_instance.is_git_repo.return_value = True
        mock_git_manager_instance.commit_task_completion.side_effect = lambda task: (
            mock_git_manager_instance.committed_tasks.append(task),
            setattr(mock_git_manager_instance, 'pushed', True),
            {"success": True, "commit_hash": "mock_hash", "commit_message": "mock_message", "push_result": {"status": "success"}}
        )[2]

        # Simulate marking a task as complete
        task_id = "A1"
        task_name = "Enhance TodoWrite Tool"
        task_description = "Implement automatic git commit functionality when tasks are marked as completed"
        files_modified = ["tools/todo_writer.py", "tools/__init__.py", "tools/todo_cli.py"]
        verification_steps = [
            "TodoWrite tool successfully created with GitManager integration",
            "Automatic git commit functionality tested and working",
            "Task completion triggers structured commit messages",
            "Push to remote repository implemented with error handling"
        ]

        # Create a task first
        todo_writer.create_task(task_id, task_name, task_description)

        # Call the complete_task method
        todo_writer.complete_task(task_id, verification_steps, files_modified)

        # Assert that GitManager methods were called
        self.assertEqual(len(mock_git_manager_instance.committed_tasks), 1)
        committed_task = mock_git_manager_instance.committed_tasks[0]

        self.assertEqual(committed_task.id, task_id)
        self.assertEqual(committed_task.status, "completed")
        self.assertListEqual(sorted(committed_task.files_modified), sorted(files_modified))
        self.assertListEqual(committed_task.verification_steps, verification_steps)
        self.assertTrue(mock_git_manager_instance.pushed)

if __name__ == '__main__':
    unittest.main()