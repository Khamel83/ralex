#!/bin/bash

# RalexOS OpenCode Integration
# This script demonstrates how to use RalexOS with OpenCode

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

# Check if OpenCode is installed
check_opencode() {
    if command -v opencode >/dev/null 2>&1; then
        success "OpenCode found: $(command -v opencode)"
        return 0
    else
        error "OpenCode not found. Please install it first."
        return 1
    fi
}

# Set up MCP configuration
setup_mcp_config() {
    local config_source="/home/ubuntu/dev/RalexOS/config/zen-test-with-mcp.json"
    local config_target="$HOME/.config/opencode/opencode.json"
    
    # Create config directory if it doesn't exist
    mkdir -p "$(dirname "$config_target")"
    
    # Copy the MCP-enabled configuration
    if [[ -f "$config_source" ]]; then
        cp "$config_source" "$config_target"
        success "MCP configuration copied to $config_target"
    else
        error "MCP configuration file not found: $config_source"
        return 1
    fi
}

# Verify MCP servers
verify_mcp_servers() {
    log "Verifying MCP servers..."
    
    local servers=("context7-mcp" "github-mcp-server" "server-puppeteer" 
                   "mcp-sequential-thinking" "zen-mcp-server" "memory-bank-mcp")
    
    for server in "${servers[@]}"; do
        if command -v "$server" >/dev/null 2>&1; then
            success "Found $server"
        else
            warn "Missing $server - run ./ralexos.sh to install"
        fi
    done
}

# Show usage examples
show_usage() {
    echo
    echo "Usage examples:"
    echo "  opencode                    # Start OpenCode TUI"
    echo "  opencode run 'hello world'  # Run a quick command"
    echo "  opencode models             # List available models"
    echo
    echo "In the OpenCode TUI, you can use these commands:"
    echo "  /help     - Show help"
    echo "  /models   - Switch between models"
    echo "  /mcp      - Manage MCP servers"
    echo
}

# Main function
main() {
    log "Setting up RalexOS with OpenCode..."
    
    # Check if OpenCode is installed
    if ! check_opencode; then
        log "Please install OpenCode first:"
        log "curl -fsSL https://opencode.ai/install | bash"
        exit 1
    fi
    
    # Set up MCP configuration
    setup_mcp_config
    
    # Verify MCP servers
    verify_mcp_servers
    
    success "RalexOS integration with OpenCode is set up!"
    show_usage
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi