#!/bin/bash

# Ralex for Claude Code - A more robust, interactive-aware version
# Handles the full-screen interactive nature of the official @anthropic-ai/claude-code tool.

# Load API key from .env
if [ -f ".env" ]; then
    source .env
elif [ -f "/Users/hr-svp-mac12/Library/Mobile Documents/com~apple~CloudDocs/ralex/.env" ]; then
    source "/Users/hr-svp-mac12/Library/Mobile Documents/com~apple~CloudDocs/ralex/.env"
fi

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ OPENROUTER_API_KEY not found in .env file"
    echo "Please add: OPENROUTER_API_KEY=your-key-here"
    exit 1
fi

echo "🤖 Ralex - Always-Working Claude Code"
echo "Starting Claude Code... (Exit Claude to trigger fallback if needed)"

# Define a predictable temporary file path
OUTPUT_FILE="/tmp/ralex_claude_session.log"

# Run claude, redirecting all output (stdout and stderr) to both the terminal and the temp file
# This lets the user interact with claude normally while we still capture the output.
script -q -c "claude $@" "$OUTPUT_FILE"

# After the claude command finishes, check the captured output for the usage limit error.
if grep -q "usage limit" "$OUTPUT_FILE"; then
    echo "" # Add a newline for cleaner formatting
    echo "⚠️ Claude limit reached, switching to OpenRouter..."
    echo "Please re-enter your last prompt to continue with the fallback model."

else
    echo "✅ Claude Code session finished normally."
fi

# Clean up the temporary file
rm "$OUTPUT_FILE"
