import logging
import time

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class ErrorHandler:
    def __init__(self, max_retries: int = 3, initial_backoff: float = 1.0):
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff

    def handle_error(self, error: Exception, context: str = "", retryable: bool = False) -> bool:
        error_message = f"An error occurred: {error}"
        if context:
            error_message += f" in context: {context}"
        logging.error(error_message)

        if retryable:
            logging.info(f"Attempting retry (max_retries: {self.max_retries})")
            return True # Indicate that a retry should be attempted by the caller
        return False # Indicate no retry or retry not applicable

    def exponential_backoff(self, attempt: int) -> float:
        return self.initial_backoff * (2 ** (attempt - 1))

    def get_user_friendly_message(self, error: Exception) -> str:
        if isinstance(error, FileNotFoundError):
            return "I couldn't find the specified file. Please check the path and try again."
        elif isinstance(error, PermissionError):
            return "I don't have permission to access that file or directory. Please check your permissions."
        elif "API" in str(error) or "network" in str(error):
            return "There was an issue connecting to the AI service. Please check your internet connection or API key."
        else:
            return "An unexpected error occurred. I've logged the details for further investigation."
