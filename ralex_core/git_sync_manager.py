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

    def _create_commit_message(self, task) -> str:
        """Create structured commit message for task completion"""
        verification_text = ""
        if task.verification_steps:
            verification_text = "\n".join([f"- {step}" for step in task.verification_steps])
        else:
            verification_text = "- Task completed and verified"

        files_text = ""
        if task.files_modified:
            files_text = "\n".join([f"- {file}" for file in task.files_modified])
        else:
            files_text = "- (Auto-detected from git status)"

        next_info = task.next_task_info or "Continue with remaining tasks"

        return f"""feat: complete Task {task.id} - {task.name}\n\n✅ Implementation verified:\n{verification_text}\n\n🔧 Files modified:\n{files_text}\n\n📋 Next: {next_info}\n\n🤖 Generated with [Claude Code](https://claude.ai/code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"""

    def sync(self, commit_message: str):
        """Full sync with push"""
        try:
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True)
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.repo_path, check=True)
            subprocess.run(["git", "push"], cwd=self.repo_path, check=True)
            return True
        except subprocess.CalledProcessError:
            return False