#!/bin/bash
#
# k83-setup.sh
# This script installs the core Agent OS command framework, making it available
# to Claude Code and other tools.

set -e

# --- Configuration ---
AGENT_OS_DIR="$HOME/.agent-os"
INSTRUCTIONS_DIR="$AGENT_OS_DIR/instructions"
CLAUDE_COMMANDS_DIR="$HOME/.claude/commands"
REPO_BASE_URL="https://raw.githubusercontent.com/buildermethods/agent-os/main"

INSTRUCTION_FILES=(
    "plan-product.md"
    "create-spec.md"
    "execute-tasks.md"
    "execute-task.md"
    "analyze-product.md"
)

# --- Functions ---
echo_green() {
    echo -e "\033[0;32m$1\033[0m"
}

echo_bold() {
    echo -e "\033[1m$1\033[0m"
}

# --- Main Script ---
echo_bold "Starting k83 Agent OS Framework Setup..."

# 1. Create necessary directories
echo "[1/3] Creating local directories..."
mkdir -p "$INSTRUCTIONS_DIR"
mkdir -p "$CLAUDE_COMMANDS_DIR"
echo_green ">= Directories created successfully."

# 2. Download core instruction files from the Agent OS repository
echo "[2/3] Downloading core instruction files..."
for file in "${INSTRUCTION_FILES[@]}"; do
    url="$REPO_BASE_URL/instructions/$file"
    dest="$INSTRUCTIONS_DIR/$file"
    echo "    -> Downloading $file..."
    if curl -sSL -f "$url" -o "$dest"; then
        echo "       Done."
    else
        echo "       Error: Could not download $file from $url. Please check the URL and your connection."
        exit 1
    fi
done
echo_green ">= All instruction files downloaded to $INSTRUCTIONS_DIR."

# 3. Create pointer files for Claude Code custom commands
echo "[3/3] Creating Claude Code command pointers..."
for file in "${INSTRUCTION_FILES[@]}"; do
    pointer_file="$CLAUDE_COMMANDS_DIR/$file"
    instruction_path="$INSTRUCTIONS_DIR/$file"
    
    # Create a markdown file that tells the AI to read the real instruction file
    cat > "$pointer_file" <<- EOM
# Role: Command Router

## Instructions
1.  This file is a pointer. Do not execute the instructions here.
2.  Your task is to read and execute the instructions located in the following file path:
    `$instruction_path`
3.  Use the user's prompt as the input for those instructions.
EOM
    echo "    -> Created pointer for $file."
done
echo_green ">= Claude Code commands are now set up."

echo_bold "\nSetup Complete!"
echo "You can now use commands like /create-spec directly in Claude Code."
