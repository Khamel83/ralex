from abc import ABC, abstractmethod


class CodeExecutor(ABC):
    @abstractmethod
    def execute(self, code: str, language: str) -> dict:
        """Executes code and returns a dictionary with success, stdout, and stderr."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Checks if the executor is available (e.g., tool is installed)."""
        pass
