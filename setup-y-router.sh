#!/bin/bash

# Y-Router Setup for Claude Code + OpenRouter Integration
# This provides FREE model access while keeping regular Claude Code Pro intact

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log() { echo -e "${NC}[INFO] $*${NC}"; }
success() { echo -e "${GREEN}[SUCCESS] $*${NC}"; }
warn() { echo -e "${YELLOW}[WARNING] $*${NC}"; }
error() { echo -e "${RED}[ERROR] $*${NC}"; }

# Check if we're in the right directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR"

log "Setting up Y-Router for Claude Code + OpenRouter integration..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    error "Docker is required but not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    error "Docker Compose is required but not installed. Please install Docker Compose first."
    exit 1
fi

# Check if y-router directory exists
if [ ! -d "y-router" ]; then
    log "Cloning y-router repository..."
    git clone https://github.com/luohy15/y-router.git
fi

cd y-router

# Create environment file
log "Creating y-router environment configuration..."
cat > .env << EOF
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
EOF

# Start y-router with Docker
log "Starting y-router with Docker..."
if command -v docker-compose &> /dev/null; then
    sudo docker-compose up -d
else
    sudo docker compose up -d
fi

# Wait a moment for startup
sleep 3

# Test if y-router is working
log "Testing y-router connection..."
if curl -f -s http://localhost:8787/ > /dev/null; then
    success "Y-router is running successfully on http://localhost:8787"
else
    error "Y-router failed to start properly"
    exit 1
fi

# Check for API key in .env file
ENV_FILE="../.env"
if [ -f "$ENV_FILE" ]; then
    log "Loading OpenRouter API key from $ENV_FILE..."
    OPENROUTER_API_KEY=$(grep "^OPENROUTER_API_KEY=" "$ENV_FILE" | cut -d'=' -f2)
    if [ -z "$OPENROUTER_API_KEY" ]; then
        error "OPENROUTER_API_KEY not found in $ENV_FILE"
        exit 1
    fi
    success "Found OpenRouter API key in $ENV_FILE"
else
    error "No .env file found at $ENV_FILE with OPENROUTER_API_KEY"
    exit 1
fi

# Add convenience functions to bashrc if they don't exist
BASHRC_FILE="$HOME/.bashrc"
if ! grep -q "source ~/dev/ralex/claude-functions.sh" "$BASHRC_FILE" 2>/dev/null; then
    log "Adding Y-Router function source to $BASHRC_FILE..."
    cat >> "$BASHRC_FILE" << EOF

# Y-Router Claude Code Functions
source ~/dev/ralex/claude-functions.sh
EOF
    success "Added Y-Router function source to $BASHRC_FILE"
else
    log "Y-Router functions already configured in $BASHRC_FILE"
fi

success "Y-Router setup complete!"

log "Testing the setup..."
if source "$SCRIPT_DIR/claude-functions.sh" 2>/dev/null && timeout 30 bash -i -c "claude-cheap '2+2'" >/dev/null 2>&1; then
    success "✅ Y-Router integration working!"
else
    warn "Setup complete but test failed. Functions may not load in non-interactive shells."
fi

echo
log "IMPORTANT: Functions only work in interactive shells (when you type commands manually)"
log "NEXT STEPS:"
log "1. Open a new terminal or run: source ~/dev/ralex/claude-functions.sh"
log "2. Test with: claude-cheap 'What is 2+2?'"
echo
log "USAGE:"
log "  claude                    # Your regular Claude Code Pro (unchanged)"
log "  claude-cheap 'prompt'     # GPT-5 Nano via OpenRouter"
log "  claude-gpt4 'prompt'      # GPT-4o Mini via OpenRouter"
log "  claude-flash 'prompt'     # Gemini Flash via OpenRouter"
log "  claude-kimi 'prompt'      # Kimi K2 via OpenRouter"
echo
log "Y-Router will auto-start with Docker. To stop:"
log "  sudo docker-compose -f $(pwd)/docker-compose.yml down"