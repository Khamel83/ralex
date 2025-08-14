# Project Specification: `ralex` - The `Agent OS` Controller

**Objective:** Architect a system where a local `khamel83`-versioned `Agent OS` instance serves as the master controller for all development tasks. The system will provide methodologies for "checking out" the agent's state to an external platform (like Claude Code) and "checking in" the results, ensuring the local `Agent OS` state remains canonical.

---

## Domain A: Core Environment Setup (`ralex-foundation`)

This domain covers the installation, configuration, and basic integration of the core third-party tools. It is the bedrock upon which the rest of the project is built.

- **Task A.1: Install `claude-code-router`**
  - **Description:** Perform a standard installation of the `musistudio/claude-code-router` server.
  - **Acceptance Criteria:** The `claude-code-router` server can be started successfully and is accessible locally.

- **Task A.2: Create Initial `claude-code-router` Configuration (`config.json`)**
  - **Description:** Define the initial `config.json` for `claude-code-router`. This will include setting up providers for OpenRouter and at least one high-speed model (e.g., Gemini Flash). Define basic routing rules for `default`, `fast`, and `powerful` models.
  - **Acceptance Criteria:** The `config.json` is valid, and `claude-code-router` can successfully route requests to the configured models.

- **Task A.3: Solidify `Agent OS` Environment**
  - **Description:** Ensure your forked `khamel83/agent-os` is installed in a dedicated Python virtual environment.
  - **Acceptance Criteria:** The basic `agent-os` commands are runnable from the command line within the project's virtual environment.

---

## Domain B: `Agent OS` Master Methodologies (`agent-os-updates`)

This domain contains the core logic that needs to be added to your `Agent OS` fork.

- **Task B.1: Create `Agent OS` Tool for `claude-code-router`**
  - **File to Create (in `agent-os/tools/`):** `ccr_tool.py`
  - **Description:** This Python tool will provide a simple interface for `Agent OS` to make calls to the `claude-code-router` server. It will have functions like `ccr.prompt(text, model='default')`. This ensures all LLM access is centralized through your router.
  - **Acceptance Criteria:** From within an `Agent OS` session, you can execute `ccr.prompt("hello")` and get a response from the configured default model.

- **Task B.2: NEW `Agent OS` Methodology: State Checkout**
  - **File to Create (in `agent-os/methodologies/`):** `checkout_to_claude.py`
  - **Command to Implement:** `/checkout`
  - **Description:** This is the critical "push" operation. This command gathers the *entire* relevant state of the `Agent OS` brain and synthesizes it into a single, large, meticulously formatted prompt designed to effectively "boot up" a temporary instance of the agent's brain inside Claude Code's context window.
  - **Acceptance Criteria:** Running `/checkout` generates a `checkout_prompt.md` file and copies its content to the clipboard.

- **Task B.3: NEW `Agent OS` Methodology: State Check-in**
  - **File to Create (in `agent-os/methodologies/`):** `checkin_from_claude.py`
  - **Command to Implement:** `/checkin`
  - **Description:** This is the critical "pull" operation. It ingests the results from the external session (copied from the clipboard), uses an LLM call to parse the transcript, and updates its own internal state with the results.
  - **Acceptance Criteria:** After running `/checkin`, the `Agent OS` task list and project state reflect the work that was completed in the external Claude Code session.

---

## Domain C: The `ralex` User Interface (`ralex-cli`)

This domain is the user's local command-line interface. It's a thin wrapper that directs all input to the `Agent OS` brain.

- **Task C.1: Create the Main CLI Script**
  - **File to Create (in project root):** `ralex.py`
  - **Description:** This script is the single entry point. It initializes the `Agent OS` environment and enters a loop, passing every piece of user input directly to the `Agent OS` instance for processing.
  - **Acceptance Criteria:** Running `python ralex.py` starts an interactive session controlled by `Agent OS`.

- **Task C.2: Implement Command Passthrough**
  - **Description:** The `ralex.py` script will not have any complex logic. It simply takes the user's string and hands it off to the `Agent OS` main processing loop.
  - **Acceptance Criteria:** Typing `/checkout` in the `ralex` CLI correctly triggers the `checkout_to_claude` methodology in `Agent OS`.
