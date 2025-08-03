# Agent-OS TodoWrite Tool Integration

This document outlines the integration of the `TodoWrite` tool with Agent-OS, including the automatic git commit functionality.

## Overview

The `TodoWrite` tool has been enhanced to automatically commit changes to the git repository when a task is marked as completed. This ensures that all completed work is tracked and versioned, providing a clear history of changes.

## Integration with Agent-OS

The `TodoWrite` tool is designed to be used within the Agent-OS framework. It can be triggered by Agent-OS workflows to manage tasks and track their completion. When a task is marked as complete, the tool will automatically:

1.  Stage the modified files.
2.  Commit the changes with a structured commit message.
3.  Push the changes to the remote repository.

## Automatic Git Commit Functionality

The automatic git commit functionality is handled by the `GitManager` class, which is integrated into the `TodoWrite` tool. The `GitManager` class provides methods for staging, committing, and pushing changes to the git repository.

### Commit Message Format

The commit messages are structured to provide clear and concise information about the completed task. The format is as follows:

```
feat(agent-os): Complete task <task_id> - <task_name>

<task_description>

Verification:
- <verification_step_1>
- <verification_step_2>
```

### Error Handling

The `GitManager` class includes error handling to manage potential issues with the git operations. If an error occurs during the commit or push process, it will be logged, and the user will be notified.

## Testing

To test the integration with Agent-OS, you can create a simple workflow that uses the `TodoWrite` tool to create a task, mark it as complete, and verify that the changes are automatically committed and pushed to the repository.
