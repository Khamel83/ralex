import subprocess

class GitSyncManager:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def sync(self, commit_message: str):
        subprocess.run(["git", "add", "."], cwd=self.repo_path)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=self.repo_path)
        subprocess.run(["git", "push"], cwd=self.repo_path)