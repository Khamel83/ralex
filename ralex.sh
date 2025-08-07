#!/bin/bash
# Main entry point for the ralex tool.
# This script executes the expect wrapper script to provide a seamless
# fallback experience for claude-code.

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Execute the expect wrapper, passing all command-line arguments to it
"$SCRIPT_DIR/ralex-wrapper.exp" "$@"
