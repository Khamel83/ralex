import os
import json
from datetime import datetime

class SessionManager:
    def __init__(self, session_dir: str):
        self.session_dir = session_dir
        os.makedirs(session_dir, exist_ok=True)

    def create_new_session(self, session_id: str = None, template_name: str = None) -> dict:
        if session_id is None:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        session_path = os.path.join(self.session_dir, f"session_{session_id}.json")
        
        session_state = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "context": {},
            "history": [],
            "tasks": [],
            "current_task_index": -1
        }

        if template_name:
            template = self._load_template(template_name)
            if template:
                session_state["name"] = template.get("name", "Untitled Session")
                session_state["description"] = template.get("description", "")
                session_state["tasks"] = template.get("initial_tasks", [])
                session_state["context_files"] = template.get("context_files", [])
                print(f"Applied template '{template_name}' to session.")
            else:
                print(f"Warning: Template '{template_name}' not found.")
        
        self._save_session(session_path, session_state)
        print(f"Created new session: {session_id}")
        return session_state

    def _load_template(self, template_name: str) -> dict:
        template_path = os.path.join(os.path.dirname(__file__), 'session_templates', f"{template_name}.json")
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                return json.load(f)
        return None

    def load_session(self, session_id: str) -> dict:
        session_path = os.path.join(self.session_dir, f"session_{session_id}.json")
        if os.path.exists(session_path):
            with open(session_path, 'r') as f:
                session_state = json.load(f)
            print(f"Loaded session: {session_id}")
            return session_state
        else:
            print(f"Session {session_id} not found.")
            return None

    def _save_session(self, session_path: str, session_state: dict):
        with open(session_path, 'w') as f:
            json.dump(session_state, f, indent=4)
        print(f"Saved session state to {session_path}")

    def update_session(self, session_state: dict):
        session_id = session_state.get("session_id")
        if session_id:
            session_path = os.path.join(self.session_dir, f"session_{session_id}.json")
            self._save_session(session_path, session_state)
        else:
            print("Error: Session ID not found in session state. Cannot update.")

if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    session_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'session'))
    manager = SessionManager(session_dir)

    # Create a new session from a template
    new_session = manager.create_new_session(template_name="bug_fix")
    print(f"New session ID: {new_session['session_id']}")
    print(f"Session Name: {new_session.get('name')}")
    print(f"Initial Tasks: {new_session.get('tasks')}")

    # Load the session
    loaded_session = manager.load_session(new_session['session_id'])
    if loaded_session:
        loaded_session['status'] = "in_progress"
        manager.update_session(loaded_session)

    # Try to load a non-existent session
    manager.load_session("non_existent_session")
