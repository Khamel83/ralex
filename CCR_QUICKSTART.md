# Quickstart: Using the Qwen Coder Agent

This document explains how to set up and run a powerful, free-to-use coding agent powered by the Qwen 3 Coder model. This setup uses `claude-code-router` to feel just like using a different version of Claude Code.

## Prerequisites

Make sure you have the following tools installed on your new machine:
- `git`
- `node` and `npm`

## One-Time Setup on a New Machine

Follow these simple steps to get started.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Khamel83/ralex.git
cd ralex
```

### Step 2: Create Your Secrets File

All your secret API keys are managed in a single `.env` file that is never checked into git. 

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit the new `.env` file and add your secret key from [https://openrouter.ai/](https://openrouter.ai/):
   ```ini
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   ```

### Step 3: Run the Setup Script

Execute the setup script. This will install the necessary tools and configure them to use your API key.

```bash
./setup-claude-code-router.sh
```

## How to Run Your New Agent

After the one-time setup, you can start using the agent.

1.  **Start the Router in the Background**:
    In your terminal, run the following command. This starts the server process that directs traffic to the Qwen model and runs it in the background so you can continue using the same terminal.
    ```bash
    ccr &
    ```

2.  **Run the Qwen Agent**:
    Now, you can start the agent. It will feel exactly like using Claude Code.
    ```bash
    ccr code
    ```

### (Optional) Create a Simple Alias

To make it feel even more like a dedicated agent, you can add this alias to your shell's startup file (e.g., `.bashrc`, `.zshrc`):

```bash
alias qwen-agent="ccr code"
```

After adding that, you can simply run `qwen-agent` to start your new coding assistant.
