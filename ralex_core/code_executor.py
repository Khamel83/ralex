import subprocess
import sys
import tempfile
import os
import time

from ralex_core.executors.base import CodeExecutor as BaseCodeExecutor


class CodeExecutor(BaseCodeExecutor):
    def execute(self, code: str, language: str = "python") -> dict:
        if language == "python":
            return self.execute_python_code(code)
        else:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Language {language} not supported by local executor.",
            }

    def is_available(self) -> bool:
        return True  # Local executor is always available

    def execute_python_code(self, code: str, timeout: int = 10) -> dict:
        """Executes Python code in a temporary directory with a timeout and captures stdout/stderr."""
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = os.path.join(tmpdir, "script.py")
            with open(script_path, "w") as f:
                f.write(code)

            try:
                process = subprocess.run(
                    [sys.executable, script_path],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=timeout,
                    cwd=tmpdir,  # Run in temporary directory
                )
                return {
                    "success": True,
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                }
            except subprocess.CalledProcessError as e:
                return {"success": False, "stdout": e.stdout, "stderr": e.stderr}
            except subprocess.TimeoutExpired:
                return {
                    "success": False,
                    "stdout": "",
                    "stderr": f"Execution timed out after {timeout} seconds.",
                }
            except Exception as e:
                return {"success": False, "stdout": "", "stderr": str(e)}
