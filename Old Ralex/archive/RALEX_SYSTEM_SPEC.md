
# Project Spec: `k83` Context-Aware State Management System

## 1. Vision & Overview

The `k83` AgentOS variant will be enhanced to become a truly context-aware development orchestrator. It will eliminate the friction of switching between different AI development environments (Claude Code, Cursor, `ccr`) by automating the capture, translation, and injection of conversational context.

The user will be able to move seamlessly between their preferred proprietary tools (like the Claude Code subscription app) and flexible, multi-model environments (`ccr`) without manual effort. A simple command, `k83 save`, will persist the session state from any tool, and `k83 resume` will inject that state into a new environment, creating a continuous, unbroken workflow.

## 2. The Core Problem

Development context, specifically the conversational history, is currently trapped within the proprietary silos of individual tools. Each tool stores this history in a different location and a different format. Manually exporting, translating, and importing this context is tedious, error-prone, and a significant barrier to a fluid workflow. This project solves the problem of **interoperability and state portability** between AI coding tools.

## 3. Proposed Architecture

We will build a new, core module within the `k83` Python codebase called the `StateManager`. This module will encapsulate all logic for detecting, exporting, and formatting context from various sources.

This new functionality will be exposed through two primary commands added to the `k83` CLI:
- `k83 save`: Detects the last active tool, extracts its history, formats it into a universal `claude_context.md`, and archives it to Git.
- `k83 resume`: Intelligently selects the next model in a predefined rotation and launches the `ccr` environment with the universal context pre-loaded.

The existing `ralex-*.sh` scripts will be refactored into simple aliases for these core `k83` commands.

## 4. Key Features (Epics)

- **Epic 1:** Foundational `StateManager` Module
- **Epic 2:** Tool-Specific History Exporters
- **Epic 3:** Core Workflow Command Implementation (`save`/`resume`)
- **Epic 4:** `ccr` Environment Integration

## 5. Detailed Task Breakdown

### Epic 1: Foundational `StateManager` Module
- [ ] **Task: Analyze existing `k83` codebase.**
  - [ ] Sub-task: Review `agent_os_bridge.py`, `context_analyzer.py`, and `methodology_engine.py` to identify integration points.
- [ ] **Task: Design the `StateManager` class.**
  - [ ] Sub-task: Define the class structure, methods, and properties in a new `ralex-integration-package/state_manager.py` file.
  - [ ] Sub-task: Define the universal context format (e.g., a list of Python dictionaries with `speaker` and `message` keys).
- [ ] **Task: Implement a tool detection mechanism.**
  - [ ] Sub-task: Write a function `detect_active_tool()` that checks the last modified times of history files for Claude Code, Cursor, and `ccr` to determine the most recent one.

### Epic 2: Tool-Specific History Exporters
- [ ] **Task: Implement Claude Code Exporter.**
  - [ ] Sub-task: Create `export_claude_history()` method.
  - [ ] Sub-task: Add logic to locate the correct `.jsonl` file within `~/.claude/projects/`.
  - [ ] Sub-task: Write a parser to read the JSON Lines format and convert it to the universal context format.
- [ ] **Task: Implement Cursor Exporter.**
  - [ ] Sub-task: Create `export_cursor_history()` method.
  - [ ] Sub-task: Add logic to locate the `state.vscdb` file for both macOS (`~/Library/Application Support/Cursor/`) and Linux (`~/.config/Cursor/`).
  - [ ] Sub-task: Write a SQL query to extract the conversation history.
  - [ ] Sub-task: Write a parser to convert the SQL results to the universal context format.
- [ ] **Task: Implement `ccr` Exporter.**
  - [ ] Sub-task: Create `export_ccr_history()` method.
  - [ ] Sub-task: Add logic to read and parse the transcript from `~/.config/ccr/history/`.

### Epic 3: Core Workflow Command Implementation
- [ ] **Task: Implement the `k83 save` command.**
  - [ ] Sub-task: Add the `save` command to `agent_os_bridge.py`.
  - [ ] Sub-task: The command logic should call the `StateManager` to get the context, format it into Markdown, and write it to `claude_context.md` in the current project directory.
  - [ ] Sub-task: Integrate with existing `k83` Git logic to automatically add, commit, and push `claude_context.md` and any other changed files.
- [ ] **Task: Implement the `k83 resume` command.**
  - [ ] Sub-task: Add the `resume` command to `agent_os_bridge.py`.
  - [ ] Sub-task: Implement a model rotation mechanism that reads/writes the last-used model from a `.ralex_state` file.
  - [ ] Sub-task: The command logic should construct and execute the `ccr code --model [next_model] --file claude_context.md` shell command.

### Epic 4: `ccr` Environment Integration
- [ ] **Task: Create a `ccr` configuration file.**
  - [ ] Sub-task: Define custom commands (`/flash`, `/bang`, `/product-spec`, `/execute-tasks`) in a `ccr_config.yaml`.
  - [ ] Sub-task: Map these commands to execute the corresponding `k83` Python functions (e.g., `/flash` will call the `save` logic).
- [ ] **Task: Modify `k83 resume` to use the custom config.**
  - [ ] Sub-task: Update the `ccr` launch command to include the `--config ccr_config.yaml` flag.

## 6. High-Level User Workflow

1.  **Start:** User works in `claude code`.
2.  **Stop:** User closes `claude code`.
3.  **Save State:** User opens a terminal in the project root and runs `k83 save`.
    - *`k83` automatically finds the Claude history, creates `claude_context.md`, and pushes all work to GitHub.*
4.  **Resume:** User runs `k83 resume`.
    - *`k83` sees the last model was Claude, picks Qwen-Coder from the rotation, and launches `ccr`.*
5.  **Work:** The `ccr` environment appears, pre-loaded with the full conversation history. All custom commands like `/product-spec` are available.
6.  **Switch Again:** User types `/flash` inside `ccr`.
    - *The `k83 save` logic is triggered automatically. The `ccr` session history is saved and pushed to Git.*
7.  **Exit and Resume:** User types `exit`, then runs `k83 resume` again.
    - *`k83` sees the last model was Qwen, picks DeepSeek from the rotation, and launches a new `ccr` session with the updated context.*

This specification outlines a clear path to transforming `k83` into the powerful, seamless development assistant you have envisioned.
