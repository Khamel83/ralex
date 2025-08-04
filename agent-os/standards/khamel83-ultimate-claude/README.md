# Khamel83 Agent-OS Enhancements: Ultimate Claude Code Setup

This document outlines the architecture and setup for the "Ultimate Claude Code" system, integrating Claude Code, Claude Code Router, and Agent-OS with Khamel83's custom enhancements. The goal is to provide an always-free, always-working coding assistant experience with intelligent model fallbacks and auto-approval.

## Core Principles

-   **Always Free**: Leverages Claude Pro tokens when available, seamlessly falling back to free models from OpenRouter when tokens are exhausted or unavailable.
-   **Always Working**: Ensures continuous operation by intelligently cycling through available free models and retrying requests.
-   **Yolo Mode**: Automatically approves all Claude Code requests for a frictionless workflow, with built-in Git safety for rollback capabilities.
-   **Quality First**: Prioritizes free models based on a quality ranking (e.g., usage, context size, benchmarks) to ensure the best possible performance.
-   **Model-Agnostic Execution**: Workflows are designed as granular, execute-level tasks that can be run by any capable LLM (GPT, Claude, Llama, Gemini, etc.).

## Architecture Overview

User Command → Claude Code UI → Claude Code Router → Agent-OS/.khamel83/ (Intelligence & Tracking) → OpenRouter (Free Models) / Claude Pro

### Key Components:

1.  **Claude Code (Official)**: The primary user interface and entry point for coding tasks. Handles direct interaction and leverages Claude Pro tokens.
2.  **Claude Code Router**: A well-supported routing layer that intercepts requests from Claude Code and directs them to the appropriate model based on our custom logic.
3.  **Agent-OS (Your Fork)**: The intelligence layer. It orchestrates the entire process, manages token tracking, ranks free models, and handles auto-approvals.
    -   `.khamel83/`: Contains all custom enhancements, including:
        -   `claude-pro-tracker/`: Monitors Claude Pro token status and refresh cycles.
        -   `free-model-ranker/`: Discovers and ranks free models from OpenRouter.
        -   `yolo-mode/`: Implements the auto-approval logic with Git safety.
        -   `integration-configs/`: Stores the main `claude-router-config.json` that links all components.
4.  **OpenRouter**: Provides access to a wide range of language models, including many free options. Our system filters and ranks these to ensure optimal fallback.

## Installation (One-Command Setup)

To set up the entire system, simply run the `setup-ultimate-claude.sh` script. This script will:

1.  Install `claude-code` and `claude-code-router` globally.
2.  Clone your `Khamel83/agent-os` fork into `~/.agent-os` (or update it if it already exists).
3.  Create the necessary directory structure within `~/.agent-os/.khamel83/`.
4.  Symlink your custom `.khamel83` templates to the Claude Code Router's configuration directory.
5.  Copy the main `claude-router-config.json` to configure the router.

```bash
curl -sSL https://raw.githubusercontent.com/Khamel83/agent-os/agent-os-ultimate/setup-ultimate-claude.sh | bash
```

**Note on Global vs. Per-Project Installation:**

-   **Global (Recommended)**: Running the setup script as shown above installs the core components globally, making `claude` and `ccr` commands available system-wide. This is generally preferred for a consistent experience across all your coding projects.
-   **Per-Project**: While the core tools are global, the Agent-OS workflows and `.khamel83` configurations are designed to be flexible. You can manage project-specific configurations by adjusting the `claude-router-config.json` or by using environment variables to point to different Agent-OS instances if needed. For most users, the global setup will suffice.

## Workflows (Agent-OS Style)

The system is broken down into modular Agent-OS workflows, each defining a specific set of tasks:

-   **`setup-ultimate-claude.yaml`**: Handles initial installation and configuration.
-   **`token-management.yaml`**: Manages Claude Pro token status and refresh cycles.
-   **`model-fallback.yaml`**: Implements the intelligent routing and fallback logic between Claude Pro and free OpenRouter models.
-   **`yolo-mode.yaml`**: Manages the auto-approval system and Git safety mechanisms.

These workflows are designed to be executed by any capable LLM, ensuring maximum flexibility and future-proofing.

## Git Safety for Auto-Approval (Yolo Mode)

To ensure safe auto-approvals, the system integrates with Git:

-   **Pre-Action Commits**: Before any potentially destructive or significant action, the system will attempt to `git add . && git commit -m "auto-commit before action"` to create a rollback point. This ensures that every change is tracked and can be undone.
-   **Git Repository Check**: Auto-approval will only proceed if the current working directory is a Git repository.
-   **Rollback Capability**: The auto-commit strategy provides a clear history, allowing for easy rollback to previous states if an auto-approved action leads to undesirable results.
-   **Necessary Answer Check**: If a decision requires external context (e.g., from `README` files or existing documentation) that cannot be programmatically resolved, the system will *not* auto-approve and will prompt the user for intervention.

## Logging

Comprehensive logging is enabled by default through the Claude Code Router's native logging capabilities. All inbound and outbound requests, model selections, and errors will be logged locally. This provides a detailed audit trail for analysis and debugging, without uploading sensitive information to remote repositories.

## Model Context Switching

When switching between models (e.g., due to rate limits or token exhaustion), the full conversation context will be passed to the new model. The new model will then be responsible for compacting or summarizing the context as needed to fit its context window, ensuring continuity of the conversation and task.

## Free Model Quality Ranking (OpenRouter)

Free models from OpenRouter will be ranked based on a combination of factors, prioritizing:

1.  **Usage Popularity**: Models with higher recent usage (if available via OpenRouter API or programmatic parsing of leaderboards) will be preferred.
2.  **Context Window Size**: Models with larger context windows will be favored for their ability to handle more complex tasks and longer conversations.
3.  **Coding Benchmarks**: If programmatic access to coding-specific benchmarks is available, these will be incorporated into the ranking.

The ranking will be dynamic, re-evaluating periodically or upon model failure to ensure the best available free model is always selected.

## Future-Proofing (OpenCode Compatibility)

The architecture is designed to be highly resilient. If Claude Code or Claude Code Router were to become unavailable or change in breaking ways, the system can be trivially ported to OpenCode (a Claude Code clone) with minimal changes, as the Agent-OS layer abstracts the underlying model interface.

## Success Criteria

The ultimate success of this system is defined by:

-   **One-Command Setup**: A single command installs and configures the entire system.
-   **Seamless Operation**: You can type `claude "build me a simple API"` and it works without any manual prompts or approvals.
-   **Continuous Functionality**: The system continues to work even after Claude Pro tokens are exhausted, seamlessly falling back to free models.
-   **Uninterrupted Workflow**: The project is completed without manual intervention due to model limitations or cost concerns.

This comprehensive setup ensures a powerful, cost-effective, and highly automated coding assistant experience.
