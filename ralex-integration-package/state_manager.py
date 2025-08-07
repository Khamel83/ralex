#!/usr/bin/env python3
"""
State Manager - Handles the saving and loading of conversational context.

This module is the core of the context-aware state management system for k83.
It is responsible for:
- Detecting which AI development tool was used last.
- Exporting the conversational history from that tool.
- Formatting the history into a universal format.
- Writing the context to a project-specific file.
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

class StateManager:
    """Manages the state of conversations across different AI tools."""

    def __init__(self, project_root: str = "."):
        """
        Initializes the StateManager.

        Args:
            project_root: The root directory of the project.
        """
        self.project_root = Path(project_root).resolve()
        self.user_home = Path.home()

        # Define paths to known history locations
        self.history_paths = {
            "claude_code": self.user_home / ".claude" / "projects",
            "cursor": self.user_home / "Library" / "Application Support" / "Cursor" / "User" / "workspaceStorage",
            "ccr": self.user_home / ".config" / "ccr" / "history"
        }

    def save_state(self) -> Tuple[bool, str]:
        """
        Detects the last used tool, extracts its history, and saves it.

        This is the main entry point for the `k83 save` command.

        Returns:
            A tuple of (success, message).
        """
        # 1. Detect the most recently used tool
        active_tool, history_file = self._detect_active_tool()

        if not active_tool:
            return False, "Could not determine the last active AI tool. No recent history found."

        # 2. Export the context from that tool
        exported_context = self._export_context(active_tool, history_file)

        if not exported_context:
            return False, f"Failed to export context from {active_tool}."

        # 3. Write the context to the universal file
        self._write_project_context(exported_context)

        message = f"Successfully saved context from {active_tool} to claude_context.md."
        print(message)
        return True, message

    def _detect_active_tool(self) -> Optional[Tuple[str, Path]]:
        """
        Detects the most recently used AI tool by checking file modification times.

        Returns:
            A tuple containing the tool name and the path to its most recent history file,
            or None if no recent history is found.
        """
        latest_file = None
        latest_tool = None
        latest_time = 0

        # Check Claude Code
        claude_path = self.history_paths["claude_code"]
        if claude_path.exists():
            for project_dir in claude_path.iterdir():
                if project_dir.is_dir():
                    for file in project_dir.glob("*.jsonl"):
                        try:
                            mtime = file.stat().st_mtime
                            if mtime > latest_time:
                                latest_time = mtime
                                latest_tool = "claude_code"
                                latest_file = file
                        except FileNotFoundError:
                            continue
        
        # Check Cursor
        cursor_path = self.history_paths["cursor"]
        if cursor_path.exists():
            for workspace_dir in cursor_path.iterdir():
                if workspace_dir.is_dir():
                    db_file = workspace_dir / "state.vscdb"
                    if db_file.exists():
                        try:
                            mtime = db_file.stat().st_mtime
                            if mtime > latest_time:
                                latest_time = mtime
                                latest_tool = "cursor"
                                latest_file = db_file
                        except FileNotFoundError:
                            continue

        # Placeholder for CCR detection logic
        # This will be implemented in Epic 2
        ccr_path = self.history_paths["ccr"]
        if ccr_path.exists():
            for file in ccr_path.glob("*.md"):
                try:
                    mtime = file.stat().st_mtime
                    if mtime > latest_time:
                        latest_time = mtime
                        latest_tool = "ccr"
                        latest_file = file
                except FileNotFoundError:
                    continue

        if latest_tool:
            return latest_tool, latest_file
        return None

    def _export_context(self, tool_name: str, history_file: Path) -> Optional[List[Dict]]:
        """
        Routes to the correct exporter based on the tool name.

        Args:
            tool_name: The name of the tool (e.g., 'claude_code').
            history_file: The path to the specific history file.

        Returns:
            A list of message dictionaries, or None on failure.
        """
        if tool_name == "claude_code":
            return self._export_claude_history(history_file)
        elif tool_name == "cursor":
            return self._export_cursor_history(history_file)
        elif tool_name == "ccr":
            return self._export_ccr_history(history_file)
        return None

    def _write_project_context(self, context: List[Dict], filename: str = "claude_context.md"):
        """
        Writes the exported context to the project's context file.

        Args:
            context: A list of message dictionaries.
            filename: The name of the context file to write.
        """
        output_path = self.project_root / filename
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Universal AI Conversation Log\n\n")
            f.write(f"**Last Updated:** {datetime.now().isoformat()}\n\n")
            f.write("---\n\n")

            for message in context:
                speaker = message.get("speaker", "Unknown")
                content = message.get("message", "")
                f.write(f"**Speaker: {speaker.capitalize()}**\n\n")
                f.write(f"```\n{content}\n```\n\n")
                f.write("---\n\n")
        print(f"Context successfully written to {output_path}")

    # --- Tool-Specific Exporters (to be implemented in Epic 2) ---

    def _export_claude_history(self, file_path: Path) -> Optional[List[Dict]]:
        """
        Exports history from a Claude Code .jsonl file.

        The .jsonl file contains a series of JSON objects, one per line.
        Each object represents an event in the conversation. We are interested
        in 'Human' and 'Assistant' message events.

        Args:
            file_path: The path to the .jsonl history file.

        Returns:
            A list of message dictionaries in the universal format.
        """
        print(f"Exporting Claude Code history from: {file_path}")
        context = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        # We only care about message events
                        if entry.get("type") == "message" and "message" in entry:
                            message_data = entry["message"]
                            speaker = message_data.get("speaker")
                            text = message_data.get("text")

                            if speaker and text:
                                # Standardize speaker names
                                universal_speaker = "user" if speaker == "Human" else "assistant"
                                context.append({
                                    "speaker": universal_speaker,
                                    "message": text
                                })
                    except (json.JSONDecodeError, KeyError):
                        # Ignore lines that are not valid JSON or don't have the expected structure
                        continue
            return context
        except FileNotFoundError:
            print(f"Error: History file not found at {file_path}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while parsing {file_path}: {e}")
            return None


    def _export_cursor_history(self, file_path: Path) -> Optional[List[Dict]]:
        """
        Exports history from a Cursor .vscdb SQLite file.

        The chat history is stored in the 'ItemTable' table.
        We need to query this table and parse the JSON content.

        Args:
            file_path: The path to the .vscdb history file.

        Returns:
            A list of message dictionaries in the universal format.
        """
        print(f"Exporting Cursor history from: {file_path}")
        context = []
        try:
            con = sqlite3.connect(f"file:{file_path}?mode=ro", uri=True)
            cur = con.cursor()
            
            # Query the table that stores conversation history
            res = cur.execute("SELECT value FROM ItemTable WHERE key = 'history.chats'")
            row = res.fetchone()
            
            if not row:
                print("Could not find 'history.chats' key in the database.")
                return None

            # The data is a JSON string
            history_data = json.loads(row[0])

            # The structure is a list of conversations, we'll take the last one
            if not history_data:
                return []
            
            # Find the most recent conversation thread
            latest_convo = max(history_data, key=lambda c: c.get('lastUpdated', 0))

            for message in latest_convo.get("messages", []):
                speaker = message.get("role", "unknown")
                content = message.get("content", "")

                if content:
                    # Standardize speaker names
                    universal_speaker = "user" if speaker == "user" else "assistant"
                    context.append({
                        "speaker": universal_speaker,
                        "message": content
                    })

            con.close()
            return context

        except sqlite3.Error as e:
            print(f"SQLite error while reading {file_path}: {e}")
            return None
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing JSON from Cursor history: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while parsing {file_path}: {e}")
            return None

    def _export_ccr_history(self, file_path: Path) -> Optional[List[Dict]]:
        """
        Exports history from a ccr transcript file.

        The format is a Markdown file with a specific structure for speakers and messages.

        Args:
            file_path: The path to the ccr history file.

        Returns:
            A list of message dictionaries.
        """
        print(f"Exporting CCR history from: {file_path}")
        context = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Split the conversation into blocks based on the separator
            blocks = content.split("\n---\n\n")
            for block in blocks:
                if not block.strip():
                    continue

                # Extract speaker and message from each block
                parts = block.split("**\n\n```\n")
                if len(parts) != 2:
                    continue

                speaker_part, message_part = parts
                
                speaker_line = speaker_part.strip()
                message = message_part.replace("\n```", "").strip()

                if speaker_line.startswith("**Speaker: "):
                    speaker = speaker_line.replace("**Speaker: ", "").replace("**", "").strip().lower()
                    universal_speaker = "user" if speaker == "user" else "assistant"
                    
                    context.append({
                        "speaker": universal_speaker,
                        "message": message
                    })

            return context
        except FileNotFoundError:
            print(f"Error: History file not found at {file_path}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while parsing {file_path}: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # This demonstrates how the StateManager would be used.
    # We're in the ralex project root, so it will run here.
    print("Running StateManager standalone example...")
    manager = StateManager()
    success, message = manager.save_state()
    print(f"Result: {success} - {message}")
