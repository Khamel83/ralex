#!/bin/bash

# Sets up the claude-code-router configuration by injecting the 
# OpenRouter API key from an environment variable into a template file.

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log() { echo -e "${NC}[INFO] $*${NC}"; }
success() { echo -e "${GREEN}[SUCCESS] $*${NC}"; }
warn() { echo -e "${YELLOW}[WARNING] $*${NC}"; }
error() { echo -e "${RED}[ERROR] $*${NC}"; }

# --- Configuration ---
CONFIG_TEMPLATE_PATH="./config/ccr.config.template.json"
CONFIG_TARGET_DIR="$HOME/.claude-code-router"
CONFIG_TARGET_PATH="$CONFIG_TARGET_DIR/config.json"
ENV_FILE="./.env"

# --- Main Logic ---

# Function to load environment variables from .env file
load_env() {
    if [ -f "$ENV_FILE" ]; then
        log "Sourcing environment variables from $ENV_FILE..."
        set -o allexport
        source "$ENV_FILE"
        set +o allexport
    else
        warn "$ENV_FILE not found. Assuming environment variables are already set."
    fi
}

# Function to set up the configuration
setup_router_config() {
    log "Setting up claude-code-router configuration..."

    # Check if the API key is set
    if [ -z "${OPENROUTER_API_KEY}" ]; then
        error "OPENROUTER_API_KEY is not set. Please add it to your .env file or export it."
        exit 1
    fi
    log "Found OPENROUTER_API_KEY."

    # Check if template file exists
    if [ ! -f "$CONFIG_TEMPLATE_PATH" ]; then
        error "Configuration template not found at: $CONFIG_TEMPLATE_PATH"
        exit 1
    fi

    # Create the target directory if it doesn't exist
    mkdir -p "$CONFIG_TARGET_DIR"
    log "Ensured config directory exists: $CONFIG_TARGET_DIR"

    # Replace placeholder with the actual API key and create the final config file
    sed "s|__OPENROUTER_API_KEY__|${OPENROUTER_API_KEY}|" "$CONFIG_TEMPLATE_PATH" > "$CONFIG_TARGET_PATH"

    success "Configuration successfully written to $CONFIG_TARGET_PATH"
    log "The router is now configured to use the Qwen Coder model via OpenRouter."
}

# --- Execution ---
main() {
    load_env
    setup_router_config
    echo
    log "To start the router server, run: ccr"
    log "To use the agent in a new terminal, run: ccr code"
}

main
