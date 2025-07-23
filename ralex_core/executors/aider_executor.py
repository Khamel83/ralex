import subprocess
import shutil
from ralex_core.executors.base import CodeExecutor

class AiderExecutor(CodeExecutor):
    def execute(self, code: str, language: str = "python") -> dict:
        # Aider doesn't directly execute code snippets, it modifies files.
        # For now, this executor will just return an error if direct execution is attempted.
        return {"success": False, "stdout": "", "stderr": "AiderExecutor does not support direct code execution."}

    def is_available(self) -> bool:
        return shutil.which("aider") is not None
