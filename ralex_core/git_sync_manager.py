import subprocess

class GitSyncManager:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def commit_changes(self, commit_message: str):
        """Commit changes to git (without pushing)"""
        try:
            subprocess.run(["git", "add", ".ralex/"], cwd=self.repo_path, check=True)
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.repo_path, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def sync(self, commit_message: str):
        """Full sync with push"""
        try:
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True)
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.repo_path, check=True)
            subprocess.run(["git", "push"], cwd=self.repo_path, check=True)
            return True
        except subprocess.CalledProcessError:
            return False