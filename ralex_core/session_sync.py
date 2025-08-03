import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class SessionSynchronizationSystem:
    def __init__(self, session_manager, sync_interval: int = 60):
        self.session_manager = session_manager
        self.sync_interval = sync_interval # seconds
        self.active_sessions: Dict[str, Dict] = {}
        self._sync_task = None

    async def start_sync(self):
        if self._sync_task is None or self._sync_task.done():
            logger.info(f"Starting session synchronization every {self.sync_interval} seconds.")
            self._sync_task = asyncio.create_task(self._sync_loop())

    async def stop_sync(self):
        if self._sync_task:
            logger.info("Stopping session synchronization.")
            self._sync_task.cancel()
            try:
                await self._sync_task
            except asyncio.CancelledError:
                logger.info("Session synchronization stopped.")

    async def _sync_loop(self):
        while True:
            try:
                await self.synchronize_all_sessions()
                await asyncio.sleep(self.sync_interval)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.error(f"Error during session synchronization: {e}")
                await asyncio.sleep(self.sync_interval) # Continue trying after error

    async def synchronize_all_sessions(self):
        logger.debug("Synchronizing all active sessions...")
        for session_id, session_state in list(self.active_sessions.items()):
            try:
                # Simulate fetching latest state from a central store or other device
                # For now, we'll just save the current in-memory state to disk
                self.session_manager.update_session(session_state)
                logger.debug(f"Session {session_id} synchronized.")
            except Exception as e:
                logger.error(f"Failed to synchronize session {session_id}: {e}")

    def register_session(self, session_state: Dict):
        session_id = session_state.get("session_id")
        if session_id:
            self.active_sessions[session_id] = session_state
            logger.info(f"Session {session_id} registered for synchronization.")
        else:
            logger.warning("Attempted to register session without an ID.")

    def unregister_session(self, session_id: str):
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            logger.info(f"Session {session_id} unregistered from synchronization.")

    def get_session_state(self, session_id: str) -> Optional[Dict]:
        return self.active_sessions.get(session_id)

    def update_session_state(self, session_id: str, new_state: Dict):
        if session_id in self.active_sessions:
            self.active_sessions[session_id].update(new_state)
            logger.debug(f"Session {session_id} in-memory state updated.")
        else:
            logger.warning(f"Attempted to update non-registered session {session_id}.")

# Example Usage (for testing/demonstration)
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    from agent_os.session_manager import SessionManager

    async def main():
        session_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'session'))
        sm = SessionManager(session_dir)
        sync_system = SessionSynchronizationSystem(sm, sync_interval=5) # Sync every 5 seconds

        # Create a new session and register it
        session1 = sm.create_new_session(session_id="test_session_1")
        sync_system.register_session(session1)

        # Simulate some changes to the session state
        session1['history'].append({"role": "user", "content": "Hello"})
        sync_system.update_session_state("test_session_1", session1)

        # Start synchronization
        await sync_system.start_sync()

        print("\nRunning for 15 seconds to observe synchronization...")
        await asyncio.sleep(15)

        # Simulate more changes
        session1['history'].append({"role": "assistant", "content": "Hi there!"})
        sync_system.update_session_state("test_session_1", session1)

        # Stop synchronization
        await sync_system.stop_sync()

        # Verify the session state on disk (optional)
        loaded_session = sm.load_session("test_session_1")
        print(f"\nFinal loaded session history: {loaded_session.get('history')}")

        # Clean up test session file
        os.remove(os.path.join(session_dir, "session_test_session_1.json"))
        print("Cleaned up test session file.")

    asyncio.run(main())