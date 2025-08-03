import os
import sys
from pathlib import Path

# Add project root and tools directory to Python path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "tools"))

from todo_writer import TodoWriter
from ralex_core.git_sync_manager import GitSyncManager

def run_manual_test():
    print("--- Manual TodoWrite Tool Test ---")

    # Initialize TodoWriter
    todo_writer = TodoWriter()

    # --- Test 1: Create a task ---
    print("\n1. Creating a new task...")
    task_id = "MANUAL_TEST_001"
    task_name = "Verify TodoWrite Tool Manually"
    task_description = "This task is created to manually verify the functionality of the TodoWrite tool and its Git integration."
    create_result = todo_writer.create_task(task_id, task_name, task_description)

    if create_result.get("success"):
        print(f"✅ Task '{task_id}' created successfully.")
    else:
        print(f"❌ Failed to create task '{task_id}': {create_result.get('error')}")
        if "already exists" in create_result.get("error", ""):
            print("   (Task might already exist from a previous run. Proceeding to update.)")

    # --- Test 2: Complete the task and trigger Git commit ---
    print("\n2. Completing the task and triggering Git commit...")
    files_modified = [
        "tools/todo_writer.py",
        "test_todowrite_manual.py",
        ".ralex_tasks.json"
    ]
    verification_steps = [
        "Manual test script executed successfully",
        "Task marked as completed in .ralex_tasks.json",
        "Automatic git commit triggered and pushed"
    ]

    complete_result = todo_writer.complete_task(task_id, verification_steps, files_modified)

    if complete_result.get("success"):
        print(f"✅ Task '{task_id}' completed successfully.")
        git_commit_info = complete_result.get("git_commit")
        if git_commit_info:
            print(f"   Git Commit Status: {git_commit_info.get('status', 'N/A')}")
            print(f"   Commit Hash: {git_commit_info.get('commit_hash', 'N/A')}")
            print(f"   Commit Message: {git_commit_info.get('commit_message', 'N/A')}")
            print(f"   Push Result: {git_commit_info.get('push_result', {}).get('message', 'N/A')}")
        else:
            print("   ⚠️ No Git commit information returned.")
    else:
        print(f"❌ Failed to complete task '{task_id}': {complete_result.get('error')}")

    # --- Test 3: Verify task status ---
    print("\n3. Verifying task status...")
    task_status_result = todo_writer.get_task(task_id)
    if task_status_result.get("task"):
        task = task_status_result["task"]
        print(f"✅ Task '{task_id}' status: {task['status']}")
        print(f"   Last updated: {task['updated_at']}")
    else:
        print(f"❌ Failed to retrieve task '{task_id}': {task_status_result.get('error')}")

    print("\n--- Manual Test Complete ---")

if __name__ == "__main__":
    run_manual_test()
