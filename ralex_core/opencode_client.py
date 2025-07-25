import subprocess

class OpenCodeClient:
    def __init__(self, project_path: str):
        self.project_path = project_path

    def execute_command(self, command: str) -> dict:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self.project_path)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    def read_file(self, file_path: str) -> dict:
        command = f"cat {file_path}"
        return self.execute_command(command)

    def write_file(self, file_path: str, content: str) -> dict:
        # Using printf to handle special characters and newlines better than echo
        command = f"printf \"%s\" \"{content}\" > {file_path}"
        return self.execute_command(command)