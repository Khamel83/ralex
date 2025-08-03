from dataclasses import dataclass
from typing import List


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
