import subprocess
from typing import Dict, Any
from ralex_core.task_models import Task

class GitSyncManager:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def commit_changes(self, commit_message: str):
        """Commit changes to git (without pushing)"""
        try:
            subprocess.run(["git", "add", ".ralex/"], cwd=self.repo_path, check=True)
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.repo_path, check=True)
            return {"success": True, "status": "success", "message": "Changes committed successfully"}
        except subprocess.CalledProcessError as e:
            return {"success": False, "status": "failed", "message": str(e)}

    def _create_commit_message(self, task: Any) -> str:
        print(f"DEBUG: _create_commit_message called with task: {task.id}")
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

        commit_msg = f"""feat: complete Task {task.id} - {task.name}\n\n✅ Implementation verified:\n{verification_text}\n\n🔧 Files modified:\n{files_text}\n\n📋 Next: {next_info}\n\n🤖 Generated with [Claude Code](https://claude.ai/code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"""
        print(f"DEBUG: Generated commit message: {commit_msg[:100]}...")
        return commit_msg

    def sync(self, commit_message: str):
        print(f"DEBUG: sync method called with commit_message: {commit_message[:100]}...")
        """Full sync with push"""
        try:
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True)
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.repo_path, check=True)
            commit_hash = self._get_latest_commit_hash()
            push_result = self._push_to_remote()
            result = {
                "success": True,
                "commit_hash": commit_hash,
                "commit_message": commit_message,
                "push_result": push_result
            }
            print(f"DEBUG: sync method returning: {result}")
            return result
        except subprocess.CalledProcessError as e:
            error_result = {"success": False, "error": str(e)}
            print(f"DEBUG: sync method caught exception: {error_result}")
            return error_result

    def _get_latest_commit_hash(self) -> str:
        """Get the hash of the latest commit"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except:
            return "unknown"

    def _push_to_remote(self) -> Dict[str, Any]:
        """Attempt to push to remote repository"""
        try:
            remote_result = subprocess.run(
                ['git', 'remote', '-v'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )

            if not remote_result.stdout.strip():
                return {"status": "no_remote", "message": "No remote repository configured"}

            push_result = subprocess.run(
                ['git', 'push'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=60
            )

            if push_result.returncode == 0:
                return {"status": "success", "message": "Successfully pushed to remote"}
            else:
                return {"status": "failed", "message": f"Push failed: {push_result.stderr}"}

        except subprocess.TimeoutExpired:
            return {"status": "timeout", "message": "Push operation timed out"}
        except Exception as e:
            return {"status": "error", "message": f"Push error: {str(e)}"}