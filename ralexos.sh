#!/bin/bash

# RalexOS - Simple MCP Implementation
# This script sets up MCP servers for OpenCode

set -euo pipefail

# Configuration
CONFIG_DIR="$HOME/.config/opencode"
MCP_CONFIG_FILE="$CONFIG_DIR/mcp-servers.json"

# MCP Servers to install
MCP_SERVERS=(
    "@upstash/context7-mcp"
    "@github/github-mcp-server"
    "@modelcontextprotocol/server-puppeteer"
    "@arben-adm/mcp-sequential-thinking"
    "zen-mcp-server"
    "memory-bank-mcp"
)

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

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Ensure bun is installed
ensure_bun() {
    if ! command_exists bun; then
        log "Installing bun..."
        curl -fsSL https://bun.sh/install | bash
        export BUN_INSTALL="$HOME/.bun"
        export PATH="$BUN_INSTALL/bin:$PATH"
        
        # Add to shell profile
        if [[ -f "$HOME/.bashrc" ]]; then
            echo 'export BUN_INSTALL="$HOME/.bun"' >> "$HOME/.bashrc"
            echo 'export PATH="$BUN_INSTALL/bin:$PATH"' >> "$HOME/.bashrc"
        fi
        
        success "Bun installed"
    else
        success "Bun already installed"
    fi
}

# Install MCP servers
install_mcp_servers() {
    log "Installing MCP servers..."
    
    # Ensure npm is available
    if ! command_exists npm; then
        error "npm is required but not found"
        return 1
    fi
    
    # Install each MCP server
    for server in "${MCP_SERVERS[@]}"; do
        log "Installing $server..."
        if npm install -g "$server" >/dev/null 2>&1; then
            success "Installed $server"
        else
            warn "Failed to install $server"
        fi
    done
}

# Generate MCP configuration
generate_mcp_config() {
    log "Generating MCP configuration..."
    
    # Create config directory if it doesn't exist
    mkdir -p "$CONFIG_DIR"
    
    # Create MCP servers configuration
    cat > "$MCP_CONFIG_FILE" << EOF
{
  "mcp": {
    "servers": {
      "context7": {
        "type": "local",
        "command": "context7-mcp"
      },
      "github": {
        "type": "local",
        "command": "github-mcp-server",
        "args": ["stdio"]
      },
      "puppeteer": {
        "type": "local",
        "command": "server-puppeteer"
      },
      "sequential": {
        "type": "local",
        "command": "mcp-sequential-thinking"
      },
      "zen": {
        "type": "local",
        "command": "zen-mcp-server"
      },
      "memorybank": {
        "type": "local",
        "command": "memory-bank-mcp"
      }
    }
  }
}
EOF
    
    success "MCP configuration generated at $MCP_CONFIG_FILE"
}

# Verify MCP servers are installed
verify_mcp_servers() {
    log "Verifying MCP server installations..."
    
    local all_installed=true
    
    for server in "${MCP_SERVERS[@]}"; do
        # Extract command name from package name
        case "$server" in
            "@upstash/context7-mcp")
                cmd="context7-mcp"
                ;;
            "@github/github-mcp-server")
                cmd="github-mcp-server"
                ;;
            "@modelcontextprotocol/server-puppeteer")
                cmd="server-puppeteer"
                ;;
            "@arben-adm/mcp-sequential-thinking")
                cmd="mcp-sequential-thinking"
                ;;
            "zen-mcp-server")
                cmd="zen-mcp-server"
                ;;
            "memory-bank-mcp")
                cmd="memory-bank-mcp"
                ;;
            *)
                cmd="$server"
                ;;
        esac
        
        if command_exists "$cmd"; then
            success "Found $cmd"
        else
            warn "Missing $cmd"
            all_installed=false
        fi
    done
    
    if $all_installed; then
        success "All MCP servers installed successfully"
    else
        warn "Some MCP servers failed to install"
    fi
}

# Main function
main() {
    log "Setting up MCP for RalexOS..."
    
    # Ensure prerequisites
    ensure_bun
    
    # Install MCP servers
    install_mcp_servers
    
    # Generate configuration
    generate_mcp_config
    
    # Verify installations
    verify_mcp_servers
    
    success "MCP setup completed!"
    log "To use with OpenCode, merge the configuration from $MCP_CONFIG_FILE"
    log "into your OpenCode configuration file."
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi