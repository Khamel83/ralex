import os
from pathlib import Path

class ContextManager:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.context_dir = self.project_path / ".ralex"
        self.context_dir.mkdir(exist_ok=True)

    def get_context(self, session_id: str) -> str:
        context_file = self.context_dir / f"{session_id}.txt"
        if context_file.exists():
            return context_file.read_text()
        return ""

    def update_context(self, session_id: str, context: str):
        context_file = self.context_dir / f"{session_id}.txt"
        context_file.write_text(context)