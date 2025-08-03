import unittest
from unittest.mock import patch
from ralex_core.error_handler import ErrorHandler


class TestErrorHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ErrorHandler()

    @patch("logging.error")
    def test_handle_error_no_retry(self, mock_logging_error):
        error = ValueError("Test error")
        result = self.handler.handle_error(error)
        mock_logging_error.assert_called_once_with("An error occurred: Test error")
        self.assertFalse(result)

    @patch("logging.error")
    @patch("logging.info")
    def test_handle_error_retryable(self, mock_logging_info, mock_logging_error):
        error = ConnectionError("Network issue")
        result = self.handler.handle_error(error, retryable=True)
        mock_logging_error.assert_called_once_with("An error occurred: Network issue")
        mock_logging_info.assert_called_once_with("Attempting retry (max_retries: 3)")
        self.assertTrue(result)

    def test_exponential_backoff(self):
        self.assertEqual(self.handler.exponential_backoff(1), 1.0)
        self.assertEqual(self.handler.exponential_backoff(2), 2.0)
        self.assertEqual(self.handler.exponential_backoff(3), 4.0)
        self.assertEqual(self.handler.exponential_backoff(4), 8.0)

    def test_get_user_friendly_message_file_not_found(self):
        error = FileNotFoundError("file.txt")
        message = self.handler.get_user_friendly_message(error)
        self.assertEqual(
            message,
            "I couldn't find the specified file. Please check the path and try again.",
        )

    def test_get_user_friendly_message_permission_error(self):
        error = PermissionError("access denied")
        message = self.handler.get_user_friendly_message(error)
        self.assertEqual(
            message,
            "I don't have permission to access that file or directory. Please check your permissions.",
        )

    def test_get_user_friendly_message_api_error(self):
        error = Exception("API call failed")
        message = self.handler.get_user_friendly_message(error)
        self.assertEqual(
            message,
            "There was an issue connecting to the AI service. Please check your internet connection or API key.",
        )

    def test_get_user_friendly_message_generic_error(self):
        error = TypeError("Invalid type")
        message = self.handler.get_user_friendly_message(error)
        self.assertEqual(
            message,
            "An unexpected error occurred. I've logged the details for further investigation.",
        )


if __name__ == "__main__":
    unittest.main()
