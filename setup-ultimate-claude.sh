#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Setting up Ultimate Claude Code (Always Free, Always Working)"

# 1. Install Claude Code (official)
echo "Installing Claude Code..."
npm install -g @anthropic-ai/claude-code

# 2. Install Claude Code Router
echo "Installing Claude Code Router..."
npm install -g @musistudio/claude-code-router

# 3. Clone your Agent-OS fork
AGENT_OS_DIR="${HOME}/.agent-os"
if [ -d "$AGENT_OS_DIR" ]; then
  echo "Agent-OS directory already exists. Skipping clone."
  cd "$AGENT_OS_DIR"
  git checkout agent-os-ultimate || git checkout -b agent-os-ultimate
  git pull origin agent-os-ultimate
else
  echo "Cloning Agent-OS fork..."
  git clone https://github.com/Khamel83/agent-os "$AGENT_OS_DIR"
  cd "$AGENT_OS_DIR"
  git checkout -b agent-os-ultimate # Create and switch to the ultimate branch
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
ln -sf "${KHAMEL83_TEMPLATES_DIR}" "${CLAUDE_ROUTER_CONFIG_DIR}/khamel83"

# 5. Configure everything
# Copy the integration config to the Claude Code Router config directory
cp "${KHAMEL83_TEMPLATES_DIR}/integration-configs/claude-router-config.json" "${CLAUDE_ROUTER_CONFIG_DIR}/config.json"

echo "✅ Setup complete! Run: claude"
echo "✅ Features: Claude Pro → Auto Router → Free Models → Infinite Usage"
echo "✅ Yolo Mode: Auto-approves everything"
