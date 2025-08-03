import subprocess
import os

from .utils import find_available_port


class CCRManager:
    def __init__(self):
        self.pid = None
        self.port = None

    def check_installation(self):
        try:
            subprocess.run(
                ["npm", "-g", "list", "@musistudio/claude-code-router"],
                check=True,
                capture_output=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def install(self):
        print("Installing @musistudio/claude-code-router...")
        try:
            subprocess.run(
                ["npm", "install", "-g", "@musistudio/claude-code-router"], check=True
            )
            print("Installation successful.")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Installation failed: {e}")
            return False

    def start_server(self):
        if self.is_running():
            print("CCR server is already running.")
            return

        self.port = find_available_port()
        if not self.port:
            print("Could not find an available port.")
            return

        print(f"Starting CCR server on port {self.port}...")
        try:
            process = subprocess.Popen(
                ["ccr", "start", "--port", str(self.port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.pid = process.pid
            print(f"CCR server started with PID: {self.pid}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Failed to start CCR server: {e}")

    def stop_server(self):
        if not self.is_running():
            print("CCR server is not running.")
            return

        print(f"Stopping CCR server with PID: {self.pid}...")
        try:
            os.kill(self.pid, 15)  # SIGTERM
            print("CCR server stopped.")
            self.pid = None
        except OSError as e:
            print(f"Failed to stop CCR server: {e}")

    def is_running(self):
        if not self.pid:
            return False
        try:
            os.kill(self.pid, 0)
        except OSError:
            return False
        else:
            return True
