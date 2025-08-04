#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
# set -e # Temporarily disable strict exit for debugging

echo "Setting up Ultimate Claude Code (Always Free, Always Working)"

# 1. Install Claude Code (official)
echo "Installing Claude Code..."
npm install -g @anthropic-ai/claude-code

# 2. Install Claude Code Router
echo "Installing Claude Code Router..."
npm install -g @musistudio/claude-code-router

# 3. Clone your Agent-OS fork
AGENT_OS_DIR="${HOME}/.agent-os"
AGENT_OS_REPO="https://github.com/Khamel83/agent-os"
AGENT_OS_BRANCH="agent-os-ultimate"

if [ -d "$AGENT_OS_DIR" ]; then
  echo "Agent-OS directory already exists. Checking if it's a valid Git repository..."
  if [ -d "$AGENT_OS_DIR/.git" ]; then
    cd "$AGENT_OS_DIR"
    # Ensure the remote is correct
    if ! git remote get-url origin | grep -q "$AGENT_OS_REPO"; then
      echo "Incorrect Git remote. Removing and re-cloning Agent-OS."
      cd "${HOME}"
      rm -rf "$AGENT_OS_DIR"
      git clone -b "$AGENT_OS_BRANCH" "$AGENT_OS_REPO" "$AGENT_OS_DIR"
      cd "$AGENT_OS_DIR"
    else
      echo "Updating Agent-OS..."
      git fetch origin
      git checkout "$AGENT_OS_BRANCH" || git checkout -b "$AGENT_OS_BRANCH"
      git pull origin "$AGENT_OS_BRANCH"
    fi
  else
    echo "Agent-OS directory exists but is not a Git repository. Removing and re-cloning."
    cd "${HOME}"
    rm -rf "$AGENT_OS_DIR"
    git clone -b "$AGENT_OS_BRANCH" "$AGENT_OS_REPO" "$AGENT_OS_DIR"
    cd "$AGENT_OS_DIR"
  fi
else
  echo "Cloning Agent-OS fork..."
  git clone -b "$AGENT_OS_BRANCH" "$AGENT_OS_REPO" "$AGENT_OS_DIR"
  cd "$AGENT_OS_DIR"
fi

# Run Agent-OS install script if it exists
if [ -f "./install.sh" ]; then
  echo "Running Agent-OS install script..."
  ./install.sh
fi

# 4. Link Khamel83 enhancements
KHAMEL83_TEMPLATES_DIR="${AGENT_OS_DIR}/templates/.khamel83"
CLAUDE_ROUTER_CONFIG_DIR="${HOME}/.claude-code-router"

echo "Linking Khamel83 enhancements..."
mkdir -p "${CLAUDE_ROUTER_CONFIG_DIR}"
rm -rf "${CLAUDE_ROUTER_CONFIG_DIR}/khamel83" # Remove existing symlink or directory
echo "Attempting symlink: ln -sf ${KHAMEL83_TEMPLATES_DIR} ${CLAUDE_ROUTER_CONFIG_DIR}/khamel83"
ln -sf "${KHAMEL83_TEMPLATES_DIR}" "${CLAUDE_ROUTER_CONFIG_DIR}/khamel83"
echo "Symlink command completed."

echo "Verifying Khamel83 templates directory contents:"
ls -l "${KHAMEL83_TEMPLATES_DIR}"
ls -l "${KHAMEL83_TEMPLATES_DIR}/claude-pro-tracker"
ls -l "${KHAMEL83_TEMPLATES_DIR}/free-model-ranker"
ls -l "${KHAMEL83_TEMPLATES_DIR}/integration-configs"

echo "Attempting to write config.json..."
echo '{
  "routing": {
    "default": {
      "custom_router": "'"${KHAMEL83_TEMPLATES_DIR}/claude-pro-tracker/router.js"'"
    }
  },
  "workflows": {
    "setup": "'"${AGENT_OS_DIR}/workflows/setup-ultimate-claude.yaml"'",
    "token_management": "'"${AGENT_OS_DIR}/workflows/token-management.yaml"'",
    "fallback": "'"${AGENT_OS_DIR}/workflows/model-fallback.yaml"'",
    "yolo_mode": "'"${AGENT_OS_DIR}/workflows/yolo-mode.yaml"'"
  },
  "execution": {
    "model_agnostic": true,
    "can_run_on": ["gpt-4", "claude-3", "llama-3", "gemini", "any-capable-model"]
  },
  "openrouter_budget_usd": 1.00
}' > "${CLAUDE_ROUTER_CONFIG_DIR}/config.json"

# Re-enable strict exit if it was disabled
# set -e # Temporarily disable strict exit for debugging


echo "\n--- OpenRouter API Key Setup ---"
read -p "Enter your OpenRouter API Key (leave blank if you don\'t have one): " OPENROUTER_API_KEY

if [ -n "$OPENROUTER_API_KEY" ]; then
  SHELL_RC_FILE=""
  if [ -f "$HOME/.bashrc" ]; then
    SHELL_RC_FILE="$HOME/.bashrc"
  elif [ -f "$HOME/.zshrc" ]; then
    SHELL_RC_FILE="$HOME/.zshrc"
  fi

  if [ -n "$SHELL_RC_FILE" ]; then
    echo "export OPENROUTER_API_KEY=\"$OPENROUTER_API_KEY\"" >> "$SHELL_RC_FILE"
    echo "OpenRouter API Key saved to $SHELL_RC_FILE. Please run 'source $SHELL_RC_FILE' or restart your terminal."
  else
    echo "Could not find .bashrc or .zshrc. Please manually set OPENROUTER_API_KEY environment variable."
  fi
else
  echo "No OpenRouter API Key provided. Free models may not work as expected."
fi

echo "✅ Setup complete! Run: claude"
echo "✅ Features: Claude Pro → Auto Router → Free Models → Infinite Usage"
echo "✅ Yolo Mode: Auto-approves everything"

