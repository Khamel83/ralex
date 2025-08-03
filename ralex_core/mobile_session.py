import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class MobileSessionManager:
    def __init__(self, session_data_dir: str):
        self.session_data_dir = session_data_dir
        os.makedirs(session_data_dir, exist_ok=True)

    def save_mobile_session(self, session_id: str, session_state: Dict):
        """Saves a mobile session state to a JSON file."""
        file_path = os.path.join(self.session_data_dir, f"mobile_session_{session_id}.json")
        try:
            with open(file_path, 'w') as f:
                json.dump(session_state, f, indent=4)
            logger.info(f"Mobile session {session_id} saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save mobile session {session_id}: {e}")

    def load_mobile_session(self, session_id: str) -> Optional[Dict]:
        """Loads a mobile session state from a JSON file."""
        file_path = os.path.join(self.session_data_dir, f"mobile_session_{session_id}.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    session_state = json.load(f)
                logger.info(f"Mobile session {session_id} loaded from {file_path}")
                return session_state
            except Exception as e:
                logger.error(f"Failed to load mobile session {session_id}: {e}")
                return None
        logger.info(f"Mobile session {session_id} not found at {file_path}")
        return None

    def delete_mobile_session(self, session_id: str):
        """Deletes a mobile session file."""
        file_path = os.path.join(self.session_data_dir, f"mobile_session_{session_id}.json")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Mobile session {session_id} deleted.")
            except Exception as e:
                logger.error(f"Failed to delete mobile session {session_id}: {e}")

    def list_mobile_sessions(self) -> Dict[str, datetime]:
        """Lists all available mobile sessions and their last modified times."""
        sessions = {}
        for filename in os.listdir(self.session_data_dir):
            if filename.startswith("mobile_session_") and filename.endswith(".json"):
                session_id = filename[len("mobile_session_"):-len(".json")]
                file_path = os.path.join(self.session_data_dir, filename)
                try:
                    last_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                    sessions[session_id] = last_modified
                except Exception as e:
                    logger.warning(f"Could not get info for {filename}: {e}")
        return sessions

# Example Usage (for testing/demonstration)
if __name__ == "__main__":
    # Setup a temporary directory for testing
    test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'temp_mobile_sessions'))
    os.makedirs(test_dir, exist_ok=True)

    manager = MobileSessionManager(test_dir)

    # Test 1: Save a new session
    session_id_1 = "user1_deviceA"
    session_state_1 = {"user": "user1", "device": "deviceA", "data": {"key": "value1"}}
    manager.save_mobile_session(session_id_1, session_state_1)

    # Test 2: Load the session
    loaded_state_1 = manager.load_mobile_session(session_id_1)
    print(f"Loaded session 1: {loaded_state_1}")

    # Test 3: Update and save the session
    if loaded_state_1:
        loaded_state_1["data"]["key"] = "updated_value"
        manager.save_mobile_session(session_id_1, loaded_state_1)
        loaded_state_1_updated = manager.load_mobile_session(session_id_1)
        print(f"Loaded updated session 1: {loaded_state_1_updated}")

    # Test 4: List sessions
    print("\nAvailable sessions:")
    for sid, mod_time in manager.list_mobile_sessions().items():
        print(f"  - {sid}: {mod_time}")

    # Test 5: Delete a session
    manager.delete_mobile_session(session_id_1)
    print(f"\nLoaded session 1 after deletion: {manager.load_mobile_session(session_id_1)}")

    # Clean up temporary directory
    import shutil
    shutil.rmtree(test_dir)
    print(f"\nCleaned up test directory: {test_dir}")
