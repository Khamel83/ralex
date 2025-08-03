import os
import json
from datetime import datetime, timedelta, timezone

class ProjectStatusAssessment:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.status_file = os.path.join(project_root, 'agent-os-status.json')

    def _load_status(self):
        if os.path.exists(self.status_file):
            with open(self.status_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_status(self, status_data):
        with open(self.status_file, 'w') as f:
            json.dump(status_data, f, indent=4)

    def assess_status(self):
        status = self._load_status()
        status['last_assessment'] = datetime.now(timezone.utc).isoformat()

        # Example assessment: count of Python files
        python_files = 0
        for root, _, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.py'):
                    python_files += 1
        status['python_file_count'] = python_files

        # Example assessment: recent git activity
        try:
            import subprocess
            result = subprocess.run(['git', 'log', '-1', '--format=%cI'], capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                last_commit_date_str = result.stdout.strip()
                status['last_git_commit'] = last_commit_date_str
            else:
                status['last_git_commit'] = "N/A"
        except Exception:
            status['last_git_commit'] = "Error assessing git status"

        self._save_status(status)
        return status

if __name__ == "__main__":
    # Example usage
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Assuming agent_os is in the root
    assessor = ProjectStatusAssessment(project_root)
    current_status = assessor.assess_status()
    print("Project Status:")
    print(json.dumps(current_status, indent=4))
