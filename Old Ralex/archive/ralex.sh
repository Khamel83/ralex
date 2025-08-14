#!/bin/bash
# Main entry point for the ralex tool.
# This script routes to appropriate handler based on usage mode.

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Check if using direct command mode (non-interactive)
if [[ "$*" == *--direct* ]]; then
    # Remove --direct flag and pass remaining arguments
    ARGS="${*//--direct/}"
    "$SCRIPT_DIR/ralex-simple.sh" $ARGS
elif [[ $# -gt 0 ]]; then
    # Use simple script for direct commands
    "$SCRIPT_DIR/ralex-simple.sh" "$@"
else
    # Use expect wrapper for interactive sessions
    "$SCRIPT_DIR/ralex-wrapper.exp" "$@"
fi
