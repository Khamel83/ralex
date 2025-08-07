# Quickstart Guide: Getting Started with k83

This guide provides the essential steps to set up and use the `k83` context-aware development orchestrator.

---

## Step 1: One-Time Setup

### Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3:** The core `k83` scripts are written in Python.
2.  **Git:** For automated version control.
3.  **claude-code-router (`ccr`):** This is the flexible, multi-model environment `k83` uses for the "resume" functionality. If you don't have it, install it globally:
    ```bash
    pip install claude-code-router
    ```

### Dependencies

The `k83` system currently has no external Python dependencies, so no `pip install -r requirements.txt` is needed at this time. This may change as the system evolves.

### Environment Variables

1.  Navigate to your project root directory:
    ```bash
    cd "/Users/hr-svp-mac12/Library/Mobile Documents/com~apple~CloudDocs/ralex"
    ```
2.  Ensure you have a `.env` file. If not, create one (`touch .env`).
3.  Add your API keys to the `.env` file. `ccr` will need these to access the models. The most important one is `OPENROUTER_API_KEY`.
    ```bash
    # .env
    OPENROUTER_API_KEY="sk-or-your-key-here"
    ```

### Install the Agent OS Command Framework

This is the most important step. Run the following command in your terminal to download the core Agent OS instruction files and make them available to Claude Code.

```bash
cd "/Users/hr-svp-mac12/Library/Mobile Documents/com~apple~CloudDocs/ralex"
bash ./k83-setup.sh
```

This script only needs to be run once, or whenever you want to update to the latest version of the Agent OS framework.

---

## Step 2: The Daily Workflow

Here is how to use the `k83` system in your day-to-day work.

### Saving Your Session (`k83 save`)

Use this command when you have finished a work session in **any** of the supported tools (`claude code`, `Cursor`) and want to save your progress and conversational context.

1.  Close the AI tool you were using.
2.  Open your terminal in the project directory.
3.  Run the `save` command:

    ```bash
    python3 "/Users/hr-svp-mac12/Library/Mobile Documents/com~apple~CloudDocs/ralex/ralex-integration-package/agent_os_bridge.py" save
    ```

This will automatically find your last conversation, create the `claude_context.md` file, and push all your work to GitHub.

### Resuming Your Session (`k83 resume`)

Use this command to pick up where you left off. It will launch `ccr` with a new model and the full context of your last session.

1.  Open your terminal in the project directory.
2.  Run the `resume` command:

    ```bash
    python3 "/Users/hr-svp-mac12/Library/Mobile Documents/com~apple~CloudDocs/ralex/ralex-integration-package/agent_os_bridge.py" resume
    ```

Your terminal will be replaced by the `ccr` environment. The next model in the rotation will be active, and it will have the entire history from `claude_context.md` pre-loaded.

### In-Chat Saving (`/flash`)

When you are inside the `ccr` environment (after using `k83 resume`), you don't need to exit to save your progress. Simply type the `/flash` command directly into the chat.

```
/flash
```

This will trigger the exact same save process in the background, committing and pushing your latest work and the `ccr` conversation history.

---

## Recommended: Creating Shell Aliases

To make the commands easier to use, it is highly recommended to create shell aliases.

Edit your shell's configuration file (e.g., `~/.zshrc`, `~/.bashrc`) and add the following lines:

```bash
# k83 Aliases
alias k83-save="python3 '/Users/hr-svp-mac12/Library/Mobile Documents/com~apple~CloudDocs/ralex/ralex-integration-package/agent_os_bridge.py' save"
alias k83-resume="python3 '/Users/hr-svp-mac12/Library/Mobile Documents/com~apple~CloudDocs/ralex/ralex-integration-package/agent_os_bridge.py' resume"
```

After adding these lines, restart your terminal or source the config file (e.g., `source ~/.zshrc`). You can now simply use:

- `k83-save`
- `k83-resume`
