#!/bin/bash

# RalexOS Demo Script
# Demonstrates how to use your new RalexOS setup

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() { echo -e "${NC}[INFO] $*${NC}"; }
success() { echo -e "${GREEN}[SUCCESS] $*${NC}"; }
warn() { echo -e "${YELLOW}[WARNING] $*${NC}"; }
error() { echo -e "${RED}[ERROR] $*${NC}"; }
highlight() { echo -e "${BLUE}[DEMO] $*${NC}"; }

# Check if OpenCode is installed
check_opencode() {
    if command -v opencode >/dev/null 2>&1; then
        success "OpenCode found: $(command -v opencode)"
        return 0
    else
        error "OpenCode not found. Please run ralexos-complete.sh first."
        return 1
    fi
}

# Demo 1: Show available models
demo_models() {
    highlight "Demo 1: Showing available models"
    echo "Running: opencode models"
    echo "------------------------"
    opencode models
    echo "------------------------"
    success "Models listed successfully"
    echo
}

# Demo 2: One-shot command with YOLO mode
demo_yolo() {
    highlight "Demo 2: One-shot command in YOLO mode"
    echo "Running: oy \"@yolo Create a simple README.md for a new project called 'my-awesome-project'\""
    echo "------------------------"
    oy "@yolo Create a simple README.md for a new project called 'my-awesome-project'"
    echo "------------------------"
    success "YOLO command executed"
    echo
}

# Demo 3: Check MCP servers
demo_mcp() {
    highlight "Demo 3: Checking MCP servers"
    echo "You can check MCP servers in the OpenCode TUI by typing '/mcp'"
    echo "Let's verify the commands are available:"
    echo "------------------------"
    
    local mcp_servers=("context7-mcp" "github-mcp-server" "server-puppeteer" 
                       "mcp-sequential-thinking" "zen-mcp-server" "memory-bank-mcp")
    
    for server in "${mcp_servers[@]}"; do
        if command -v "$server" >/dev/null 2>&1; then
            success "Found: $server"
        else
            warn "Missing: $server"
        fi
    done
    
    echo "------------------------"
    success "MCP servers check completed"
    echo
}

# Demo 4: Model switching
demo_model_switching() {
    highlight "Demo 4: Using model aliases"
    echo "You can use these shortcuts:"
    echo "  ocp  - Claude Pro"
    echo "  ocq  - Qwen3 Coder"
    echo "  ocg  - Gemini Flash"
    echo "  ock  - Kimi K2"
    echo
    echo "Example: ocq \"Write a Python function to calculate Fibonacci numbers\""
    echo
}

# Demo 5: Show configuration
demo_config() {
    highlight "Demo 5: Showing configuration"
    local config_file="$HOME/.config/opencode/opencode.json"
    if [[ -f "$config_file" ]]; then
        echo "Configuration file: $config_file"
        echo "------------------------"
        cat "$config_file" | jq '.' 2>/dev/null || cat "$config_file"
        echo "------------------------"
    else
        warn "Configuration file not found at $config_file"
    fi
    success "Configuration displayed"
    echo
}

# Main demo function
main() {
    log "Starting RalexOS demo..."
    
    # Check prerequisites
    if ! check_opencode; then
        log "Please run the ralexos-complete.sh script first to set up your environment."
        exit 1
    fi
    
    # Run demos
    demo_models
    demo_yolo
    demo_mcp
    demo_model_switching
    demo_config
    
    highlight "Demo complete!"
    log "You're now ready to use your RalexOS setup."
    log "Try running 'opencode' to start the TUI, or use the shortcuts like 'ocp' and 'oy'."
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi