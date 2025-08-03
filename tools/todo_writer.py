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
from ralex_core.git_sync_manager import GitSyncManager
from ralex_core.task_models import Task
from dataclasses import dataclass, asdict


from dataclasses import asdict


class TodoWriteError(Exception):
    """Custom exception for TodoWrite operations"""
    pass





class TodoWriter:
    """Main TodoWrite tool with git integration"""
    
    def __init__(self, tasks_file: str = None):
        self.tasks_file = tasks_file or os.path.join(os.getcwd(), ".ralex_tasks.json")
        self.git_manager = GitSyncManager(repo_path=os.getcwd())
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
        self._create_github_issue(task)
        
        return {"success": True, "task": asdict(task)}

    def _create_github_issue(self, task: Task):
        """Create a GitHub issue for the task."""
        try:
            subprocess.run(["gh", "issue", "create", "--title", task.name, "--body", task.description], check=True)
            self.logger.info(f"Successfully created GitHub issue for task {task.id}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.logger.error(f"Failed to create GitHub issue for task {task.id}: {e}")
    
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
            git_result = self.git_manager.sync(GitSyncManager._create_commit_message(task))
        
        if git_result is None:
            self.logger.error(f"Git sync returned None for task {task_id}")
            git_result = {"success": False, "error": "Git sync returned None"}
        
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
