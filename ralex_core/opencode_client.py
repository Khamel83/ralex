import subprocess


class OpenCodeClient:
    def __init__(self, project_path: str):
        self.project_path = project_path

    def execute_command(self, command: str) -> dict:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, cwd=self.project_path
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }

    def read_file(self, file_path: str) -> dict:
        command = f"cat {file_path}"
        return self.execute_command(command)

    def write_file(self, file_path: str, content: str) -> dict:
        # Write file directly using Python instead of shell command to avoid escaping issues
        try:
            with open(file_path, "w") as f:
                f.write(content)
            return {
                "stdout": f"Successfully wrote to {file_path}",
                "stderr": "",
                "returncode": 0,
            }
        except Exception as e:
            return {"stdout": "", "stderr": str(e), "returncode": 1}
