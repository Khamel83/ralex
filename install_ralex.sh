#!/bin/bash
set -e

echo "🚀 Ralex V4 Automated Installer"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() { echo -e "${GREEN}✅ $1${NC}"; }
log_warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Check if running on supported OS
check_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        log_info "Linux detected"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        log_info "macOS detected"
    else
        log_warn "Unsupported OS: $OSTYPE (continuing anyway)"
    fi
}

# Check Python version
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        PYTHON_VERSION=$(python --version | cut -d' ' -f2)
    else
        log_error "Python not found. Please install Python 3.8+ from https://python.org"
        exit 1
    fi

    # Check version is 3.8+
    if [[ $(echo "$PYTHON_VERSION" | cut -d'.' -f1) -ge 3 ]] && [[ $(echo "$PYTHON_VERSION" | cut -d'.' -f2) -ge 8 ]]; then
        log_info "Python $PYTHON_VERSION found"
    else
        log_error "Python 3.8+ required, found $PYTHON_VERSION"
        exit 1
    fi
}

# Create virtual environment
setup_venv() {
    log_info "Creating virtual environment..."
    
    if [ -d ".venv" ]; then
        log_warn "Virtual environment already exists, using existing one"
    else
        $PYTHON_CMD -m venv .venv
        log_info "Virtual environment created"
    fi
    
    # Activate virtual environment
    source .venv/bin/activate || {
        log_error "Failed to activate virtual environment"
        exit 1
    }
    
    log_info "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    log_info "Installing dependencies..."
    
    if [ ! -f "requirements.txt" ]; then
        log_error "requirements.txt not found"
        exit 1
    fi
    
    pip install --upgrade pip
    pip install -r requirements.txt

    log_info "Verifying dependencies..."
    python scripts/verify_dependencies.py
    
    log_info "Dependencies installed successfully"
}

# Setup API key
setup_api_key() {
    echo ""
    echo "🔑 API Key Setup"
    echo "==============="
    echo "Ralex needs an OpenRouter API key to access AI models."
    echo "1. Go to https://openrouter.ai"
    echo "2. Sign up for a free account"
    echo "3. Go to 'Keys' section and copy your API key"
    echo ""
    
    read -p "Do you have an OpenRouter API key? (y/n): " has_key
    
    if [[ $has_key == "y" || $has_key == "Y" ]]; then
        read -p "Enter your OpenRouter API key: " api_key
        
        # Create .env file
        echo "OPENROUTER_API_KEY=$api_key" > .env
        log_info "API key saved to .env file"
        
        # Also export for current session
        export OPENROUTER_API_KEY="$api_key"
        
    else
        log_warn "Skipping API key setup"
        log_warn "You'll need to set OPENROUTER_API_KEY before using Ralex"
        log_warn "Run: export OPENROUTER_API_KEY='your-key-here'"
    fi
}

# Test basic functionality
test_installation() {
    log_info "Testing installation..."
    
    # Check if API key is set
    if [ -z "$OPENROUTER_API_KEY" ] && [ ! -f ".env" ]; then
        log_warn "API key not set, skipping functionality test"
        return
    fi
    
    # Source .env if it exists
    if [ -f ".env" ]; then
        source .env
    fi
    
    # Test basic bridge functionality
    echo "Testing: python ralex_bridge.py 'test installation'"
    
    if timeout 30 python ralex_bridge.py "test installation" &>/dev/null; then
        log_info "Basic functionality test passed"
    else
        log_warn "Functionality test failed (might be network/API issue)"
        log_warn "Try running manually: python ralex_bridge.py 'create a test.py file'"
    fi
}

# Create helper scripts
create_helpers() {
    # Create activation script
    cat > activate_ralex.sh << 'EOF'
#!/bin/bash
source .venv/bin/activate
if [ -f ".env" ]; then
    source .env
fi
echo "🎯 Ralex V4 environment activated"
echo "Try: python ralex_bridge.py 'create a hello.py file'"
EOF
    chmod +x activate_ralex.sh
    
    # Create health check script
    cat > health_check.sh << 'EOF'
#!/bin/bash
source .venv/bin/activate 2>/dev/null || true
if [ -f ".env" ]; then
    source .env
fi

echo "🔍 Ralex V4 Health Check"
echo "========================"

# Check Python
python --version && echo "✅ Python OK" || echo "❌ Python issue"

# Check dependencies
python -c "import litellm; print('✅ LiteLLM OK')" 2>/dev/null || echo "❌ LiteLLM missing"
python -c "import fastapi; print('✅ FastAPI OK')" 2>/dev/null || echo "❌ FastAPI missing"

# Check API key
if [ -n "$OPENROUTER_API_KEY" ]; then
    echo "✅ API key configured"
else
    echo "❌ API key not set"
fi

# Check file permissions
if [ -w "." ]; then
    echo "✅ Write permissions OK"
else
    echo "❌ No write permissions"
fi

echo ""
echo "Run 'python ralex_bridge.py --help' for usage info"
EOF
    chmod +x health_check.sh
    
    log_info "Helper scripts created: activate_ralex.sh, health_check.sh"
}

# Main installation process
main() {
    echo ""
    check_os
    check_python
    setup_venv
    install_dependencies
    setup_api_key
    test_installation
    create_helpers
    
    echo ""
    echo "🎉 Ralex V4 Installation Complete!"
    echo "================================="
    echo ""
    echo "📖 Next Steps:"
    echo "1. Activate environment: source activate_ralex.sh"
    echo "2. Test basic usage: python ralex_bridge.py 'create a hello.py file'"
    echo "3. Start full interface: python start_ralex_v4.py"
    echo "4. Read documentation: cat QUICKSTART.md"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "- Health check: ./health_check.sh"
    echo "- View logs: ls .ralex/"
    echo "- Get help: python ralex_bridge.py --help"
    echo ""
    echo "🎯 Ready to start voice-coding!"
}

# Run installation
main "$@"