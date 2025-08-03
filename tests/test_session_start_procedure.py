import asyncio
import os
import sys
import json
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ralex_core.launcher import run_interactive_mode
from agent_os.session_manager import SessionManager

# Mock dependencies for run_interactive_mode
@patch('ralex_core.launcher.OpenRouterClient')
@patch('ralex_core.launcher.SemanticClassifier')
@patch('ralex_core.launcher.BudgetManager')
@patch('ralex_core.launcher.AgentOSEnhancer')
async def test_start_command_scenarios(MockAgentOSEnhancer, MockBudgetManager, MockSemanticClassifier, MockOpenRouterClient):
    print("\n--- Testing /start command scenarios ---")

    # Setup mocks
    mock_agentos = MockAgentOSEnhancer.return_value
    mock_agentos.get_slash_commands.return_value = {"test_command": MagicMock()}
    mock_budget_manager = MockBudgetManager.return_value
    mock_budget_manager.free_mode_manager = MagicMock()
    mock_budget_manager.free_model_selector = MagicMock()

    # Create a temporary session directory for testing
    test_session_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'temp_test_sessions'))
    if not os.path.exists(test_session_dir):
        os.makedirs(test_session_dir)
    
    # Override SessionManager's session_dir for testing
    with patch('ralex_core.launcher.SessionManager') as MockSessionManager:
        mock_session_manager_instance = MockSessionManager.return_value
        mock_session_manager_instance.session_dir = test_session_dir
        # No side_effect here, let the mock track calls

        # Scenario 1: Basic /start command
        with patch('builtins.input', side_effect=['/start', '/exit']):
            print("\nScenario 1: Basic /start command")
            await run_interactive_mode({}, {}, {}, MockOpenRouterClient.return_value, MockSemanticClassifier.return_value, mock_budget_manager)
            mock_session_manager_instance.create_new_session.assert_called_once_with(session_id=None, template_name=None)
            print("  ✅ Basic /start command test passed.")

        mock_session_manager_instance.create_new_session.reset_mock()

        # Scenario 2: /start with a specific session ID
        with patch('builtins.input', side_effect=['/start my_custom_session', '/exit']):
            print("\nScenario 2: /start with a specific session ID")
            await run_interactive_mode({}, {}, {}, MockOpenRouterClient.return_value, MockSemanticClassifier.return_value, mock_budget_manager)
            mock_session_manager_instance.create_new_session.assert_called_once_with(session_id='my_custom_session', template_name=None)
            print("  ✅ /start with specific session ID test passed.")

        mock_session_manager_instance.create_new_session.reset_mock()

        # Scenario 3: /start with a template name
        with patch('builtins.input', side_effect=['/start --template bug_fix', '/exit']):
            print("\nScenario 3: /start with a template name")
            await run_interactive_mode({}, {}, {}, MockOpenRouterClient.return_value, MockSemanticClassifier.return_value, mock_budget_manager)
            mock_session_manager_instance.create_new_session.assert_called_once_with(session_id=None, template_name='bug_fix')
            print("  ✅ /start with template name test passed.")

        mock_session_manager_instance.create_new_session.reset_mock()

        # Scenario 4: /start with both ID and template
        with patch('builtins.input', side_effect=['/start my_bug_fix_session --template bug_fix', '/exit']):
            print("\nScenario 4: /start with both ID and template")
            await run_interactive_mode({}, {}, {}, MockOpenRouterClient.return_value, MockSemanticClassifier.return_value, mock_budget_manager)
            mock_session_manager_instance.create_new_session.assert_called_once_with(session_id='my_bug_fix_session', template_name='bug_fix')
            print("  ✅ /start with both ID and template test passed.")

    print("\n--- All /start command scenarios tested. ---")

    # Clean up temporary session directory
    import shutil
    if os.path.exists(test_session_dir):
        shutil.rmtree(test_session_dir)

if __name__ == "__main__":
    asyncio.run(test_start_command_scenarios())
