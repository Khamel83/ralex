"""
TodoWrite Tool with Automatic Git Integration
Enhanced task management with persistent tracking across machines and LLM handoffs.
"""

import json
import os
import subprocess
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class Task:
    """Task data structure"""
    id: str
    name: str
    description: str
    status: str  # "pending", "in_progress", "completed", "blocked"
    created_at: str
    updated_at: str
    files_modified: List[str] = None
    verification_steps: List[str] = None
    next_task_info: str = ""
    priority: str = "medium"  # "low", "medium", "high", "critical"
    
    def __post_init__(self):
        if self.files_modified is None:
            self.files_modified = []
        if self.verification_steps is None:
            self.verification_steps = []


class TodoWriteError(Exception):
    """Custom exception for TodoWrite operations"""
    pass


class GitManager:
    """Handles git operations for task completion commits"""
    
    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.getcwd()
        self.logger = logging.getLogger(__name__)
        
    def is_git_repo(self) -> bool:
        """Check if current directory is a git repository"""
        try:
            result = subprocess.run(
                ['git', 'status'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def commit_task_completion(self, task: Task) -> Dict[str, Any]:
        """Create a git commit for task completion"""
        if not self.is_git_repo():
            return {"error": "Not a git repository"}
        
        try:
            # Add all modified files to staging
            add_result = subprocess.run(
                ['git', 'add', '.'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if add_result.returncode != 0:
                return {"error": f"Failed to stage files: {add_result.stderr}"}
            
            # Create commit message
            commit_message = self._create_commit_message(task)
            
            # Create commit using Python string for message
            commit_result = subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if commit_result.returncode != 0:
                if "nothing to commit" in commit_result.stdout:
                    return {"warning": "No changes to commit"}
                return {"error": f"Failed to create commit: {commit_result.stderr}"}
            
            commit_hash = self._get_latest_commit_hash()
            push_result = self._push_to_remote()
            
            return {
                "success": True,
                "commit_hash": commit_hash,
                "commit_message": commit_message,
                "push_result": push_result
            }
            
        except subprocess.TimeoutExpired:
            return {"error": "Git operation timed out"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def _create_commit_message(self, task: Task) -> str:
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
        
        return f"""feat: complete Task {task.id} - {task.name}

✅ Implementation verified:
{verification_text}

🔧 Files modified:
{files_text}

📋 Next: {next_info}

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""
    
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


class TodoWriter:
    """Main TodoWrite tool with git integration"""
    
    def __init__(self, tasks_file: str = None):
        self.tasks_file = tasks_file or os.path.join(os.getcwd(), ".ralex_tasks.json")
        self.git_manager = GitManager()
        self.logger = logging.getLogger(__name__)
        self.tasks = self._load_tasks()
        
    def _load_tasks(self) -> Dict[str, Task]:
        """Load tasks from file"""
        if not os.path.exists(self.tasks_file):
            return {}
        
        try:
            with open(self.tasks_file, 'r') as f:
                data = json.load(f)
                return {task_id: Task(**task_data) for task_id, task_data in data.items()}
        except (json.JSONDecodeError, TypeError) as e:
            self.logger.error(f"Failed to load tasks: {e}")
            return {}
    
    def _save_tasks(self):
        """Save tasks to file"""
        try:
            data = {task_id: asdict(task) for task_id, task in self.tasks.items()}
            with open(self.tasks_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save tasks: {e}")
            raise TodoWriteError(f"Failed to save tasks: {e}")
    
    def create_task(self, task_id: str, name: str, description: str, 
                   priority: str = "medium") -> Dict[str, Any]:
        """Create a new task"""
        if task_id in self.tasks:
            return {"error": f"Task {task_id} already exists"}
        
        now = datetime.now().isoformat()
        task = Task(
            id=task_id,
            name=name,
            description=description,
            status="pending",
            created_at=now,
            updated_at=now,
            priority=priority
        )
        
        self.tasks[task_id] = task
        self._save_tasks()
        
        return {"success": True, "task": asdict(task)}
    
    def update_task(self, task_id: str, **updates) -> Dict[str, Any]:
        """Update an existing task"""
        if task_id not in self.tasks:
            return {"error": f"Task {task_id} not found"}
        
        task = self.tasks[task_id]
        old_status = task.status
        
        for field, value in updates.items():
            if hasattr(task, field):
                setattr(task, field, value)
        
        task.updated_at = datetime.now().isoformat()
        
        git_result = None
        if old_status != "completed" and task.status == "completed":
            self.logger.info(f"Task {task_id} marked as completed, creating git commit...")
            git_result = self.git_manager.commit_task_completion(task)
        
        self._save_tasks()
        
        result = {"success": True, "task": asdict(task)}
        if git_result:
            result["git_commit"] = git_result
            
        return result
    
    def complete_task(self, task_id: str, verification_steps: List[str] = None,
                     files_modified: List[str] = None, next_task_info: str = "") -> Dict[str, Any]:
        """Mark task as completed and create git commit"""
        if task_id not in self.tasks:
            return {"error": f"Task {task_id} not found"}
        
        updates = {
            "status": "completed",
            "verification_steps": verification_steps or [],
            "files_modified": files_modified or [],
            "next_task_info": next_task_info
        }
        
        return self.update_task(task_id, **updates)
    
    def list_tasks(self, status_filter: str = None) -> Dict[str, Any]:
        """List all tasks, optionally filtered by status"""
        filtered_tasks = self.tasks
        
        if status_filter:
            filtered_tasks = {
                task_id: task for task_id, task in self.tasks.items() 
                if task.status == status_filter
            }
        
        return {
            "tasks": {task_id: asdict(task) for task_id, task in filtered_tasks.items()},
            "count": len(filtered_tasks)
        }
    
    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get a specific task"""
        if task_id not in self.tasks:
            return {"error": f"Task {task_id} not found"}
        
        return {"task": asdict(self.tasks[task_id])}


# Convenience functions for easy integration
def create_todo_writer(tasks_file: str = None) -> TodoWriter:
    """Create a TodoWriter instance"""
    return TodoWriter(tasks_file)


def quick_complete_task(task_id: str, verification_steps: List[str] = None,
                       files_modified: List[str] = None, next_task_info: str = "",
                       tasks_file: str = None) -> Dict[str, Any]:
    """Quick function to complete a task with git commit"""
    writer = TodoWriter(tasks_file)
    return writer.complete_task(task_id, verification_steps, files_modified, next_task_info)
