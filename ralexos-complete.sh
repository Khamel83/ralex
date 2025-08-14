#!/bin/bash

# RalexOS - Complete OpenCode Setup
# Single script to set up your OpenCode environment with MCP on any platform

set -euo pipefail

# Configuration - EDIT THESE VALUES FOR YOUR SETUP
OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
GIT_USER_NAME="${GIT_USER_NAME:-Your Name}"
GIT_USER_EMAIL="${GIT_USER_EMAIL:-your.email@example.com}"

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
highlight() { echo -e "${BLUE}[ACTION] $*${NC}"; }

# Platform detection
detect_platform() {
    case "$(uname -s)" in
        Darwin*) echo "macos" ;;
        Linux*)
            if [[ -f /etc/os-release ]]; then
                if grep -qi "ubuntu\|debian" /etc/os-release; then
                    echo "ubuntu"
                else
                    echo "linux"
                fi
            else
                echo "linux"
            fi
            ;;
        *) echo "unknown" ;;
    esac
}

PLATFORM=$(detect_platform)
log "Detected platform: $PLATFORM"

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install system dependencies
install_system_deps() {
    case "$PLATFORM" in
        macos)
            if ! command_exists brew; then
                highlight "Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew update
            brew install node git curl || true
            ;;
        ubuntu)
            highlight "Installing system dependencies..."
            sudo apt update
            sudo apt install -y curl git build-essential ca-certificates
            sudo apt install -y nodejs npm || true
            ;;
        linux)
            log "Please ensure you have curl, git, and nodejs installed"
            ;;
    esac
}

# Install Bun
install_bun() {
    if ! command_exists bun; then
        highlight "Installing Bun..."
        curl -fsSL https://bun.sh/install | bash
        export BUN_INSTALL="$HOME/.bun"
        export PATH="$BUN_INSTALL/bin:$PATH"
        
        # Add to shell profile
        local profile_files=("$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile")
        for profile in "${profile_files[@]}"; do
            if [[ -f "$profile" ]]; then
                if ! grep -q "BUN_INSTALL" "$profile" 2>/dev/null; then
                    echo 'export BUN_INSTALL="$HOME/.bun"' >> "$profile"
                    echo 'export PATH="$BUN_INSTALL/bin:$PATH"' >> "$profile"
                fi
            fi
        done
    fi
    success "Bun ready"
}

# Install OpenCode
install_opencode() {
    if ! command_exists opencode; then
        highlight "Installing OpenCode..."
        case "$PLATFORM" in
            macos)
                brew install sst/tap/opencode || true
                ;;
            *)
                curl -fsSL https://opencode.ai/install | bash
                ;;
        esac
    fi
    
    if command_exists opencode; then
        success "OpenCode installed"
    else
        error "Failed to install OpenCode. Please install manually:"
        log "curl -fsSL https://opencode.ai/install | bash"
        return 1
    fi
}

# Install MCP servers
install_mcp_servers() {
    highlight "Installing MCP servers..."
    
    # Ensure npm is available
    if ! command_exists npm; then
        error "npm is required but not found"
        return 1
    fi
    
    # MCP servers to install
    local mcp_servers=(
        "@upstash/context7-mcp"
        "@github/github-mcp-server"
        "@modelcontextprotocol/server-puppeteer"
        "@arben-adm/mcp-sequential-thinking"
        "zen-mcp-server"
        "memory-bank-mcp"
        "mcp-server-reddit"
    )
    
    # Install each MCP server
    for server in "${mcp_servers[@]}"; do
        log "Installing $server..."
        if npm install -g "$server" >/dev/null 2>&1; then
            success "Installed $server"
        else
            warn "Failed to install $server"
        fi
    done
}

# Set up Git identity
setup_git() {
    highlight "Setting up Git identity..."
    git config --global user.name "$GIT_USER_NAME"
    git config --global user.email "$GIT_USER_EMAIL"
    success "Git identity set"
}

# Generate SSH key
generate_ssh_key() {
    local ssh_dir="$HOME/.ssh"
    local key_file="$ssh_dir/id_ed25519"
    
    mkdir -p "$ssh_dir"
    chmod 700 "$ssh_dir"
    
    if [[ ! -f "$key_file" ]]; then
        highlight "Generating SSH key..."
        ssh-keygen -t ed25519 -N "" -C "$GIT_USER_EMAIL" -f "$key_file" >/dev/null
        eval "$(ssh-agent -s)" >/dev/null 2>&1 || true
        ssh-add "$key_file" >/dev/null 2>&1 || true
        success "SSH key generated"
    else
        success "SSH key already exists"
    fi
}

# Create OpenCode configuration
create_opencode_config() {
    local config_dir="$HOME/.config/opencode"
    local config_file="$config_dir/opencode.json"
    
    highlight "Creating OpenCode configuration..."
    
    # Create config directory
    mkdir -p "$config_dir"
    
    # Create configuration with MCP servers
    cat > "$config_file" << EOF
{
  "\$schema": "https://opencode.ai/config.json",
  "model": "autopilot",
  "small_model": "openrouter/qwen/qwen3-coder:free",
  "provider": {
    "openrouter": {
      "options": {
        "headers": {
          "HTTP-Referer": "https://github.com/ralexos",
          "X-Title": "RalexOS"
        }
      },
      "models": {
        "deepseek/deepseek-r1-0528:free": {},
        "qwen/qwen3-coder:free": {},
        "qwen/qwen3-coder": {},
        "google/gemini-2.5-flash": {},
        "openai/gpt-5": {},
        "openai/gpt-4o-mini": {},
        "openai/o1-mini": {},
        "qwen/qwen-2.5-72b-instruct:free": {}
      }
    }
  },
  "agent": {
    "autopilot": {
      "description": "DEFAULT: Smart autopilot - figures everything out",
      "model": "openrouter/qwen/qwen3-coder:free",
      "system": "You are AUTOPILOT mode - the default intelligent assistant. CORE PRINCIPLES:\\n\\n1. AUTO-FIGURE-OUT: Always analyze context, read project files (README, mission, vision), understand goals, then act intelligently\\n\\n2. MISSION-DRIVEN: Look for project mission/vision/goals in files and make decisions aligned with them\\n\\n3. SMART MCP USAGE: Auto-use available tools - context7 (docs), github (git), puppeteer (web), reddit (social), zen (coordination), memorybank (memory), sequential (complex thinking)\\n\\n4. YOLO AWARENESS: If user says 'yolomode' or 'yolo', switch to full autonomous mode with aggressive action-taking\\n\\n5. COST-CONSCIOUS: Start with free models, only suggest paid models if truly needed. Budget: ~10 cents/day max\\n\\n6. SMART DEFAULTS: Make intelligent assumptions, ask only when truly blocking, prioritize getting things done\\n\\nAlways read project context first, understand the mission, then execute intelligently using appropriate tools."
    },
    "free-reasoning": {
      "description": "DeepSeek R1 (FREE) - Best free reasoning + tool calling",
      "model": "openrouter/deepseek/deepseek-r1-0528:free"
    },
    "free-coding": {
      "description": "Qwen3 Coder (FREE) - Latest agentic coding + tools", 
      "model": "openrouter/qwen/qwen3-coder:free"
    },
    "cheap-smart": {
      "description": "Gemini 2.5 Flash (~$0.075/M) - Best value smart model",
      "model": "openrouter/google/gemini-2.5-flash",
      "system": "You are a cost-efficient smart model. You cost ~$0.075/M tokens. Use this power wisely for complex tasks that free models struggle with. Always try to accomplish tasks efficiently to minimize cost."
    },
    "cheap-fast": {
      "description": "GPT-4o Mini (~$0.15/M) - Fast, reliable, tool calling", 
      "model": "openrouter/openai/gpt-4o-mini",
      "system": "You are a reliable paid model costing ~$0.15/M tokens. Use this capability for tasks requiring high accuracy and speed. Be efficient with token usage."
    },
    "premium-coding": {
      "description": "Qwen3 Coder (~$0.20/M) - Pro agentic coding", 
      "model": "openrouter/qwen/qwen3-coder",
      "system": "You are the latest Qwen3 Coder model costing ~$0.20/M tokens. Excel at agentic coding tasks, function calling, tool use, and long-context repository reasoning. Use your 256K context wisely."
    },
    "premium-reasoning": {
      "description": "o1-mini (~$3/M) - Advanced reasoning when needed",
      "model": "openrouter/openai/o1-mini",
      "system": "You are a premium reasoning model costing ~$3/M tokens. Reserved for complex problems requiring deep analysis. Think step-by-step and provide thorough solutions that justify the higher cost."
    },
    "premium-latest": {
      "description": "GPT-5 (~$10-30/M) - Cutting edge when budget allows",
      "model": "openrouter/openai/gpt-5", 
      "system": "You are GPT-5, the latest state-of-the-art model. Cost is high (~$10-30/M) so reserved for critical tasks. Excel at tool calling, web search, complex reasoning, and optimal project creation. Make every token count."
    },
    "free-general": {
      "description": "Qwen 2.5 72B (FREE) - Strong general model",
      "model": "openrouter/qwen/qwen-2.5-72b-instruct:free"
    },
    "yolo": {
      "description": "Full YOLO mode - maximum autonomous action",
      "system": "FULL YOLO MODE ACTIVATED. You have complete autonomy. Read mission/vision, understand project goals, then execute aggressively. Apply changes immediately without confirmation. Use all available MCP tools. Make decisions based on project context. Act first, explain later. Prioritize speed and results over caution.",
      "model": "openrouter/deepseek/deepseek-r1-0528:free"
    },
    "smart": {
      "description": "Smart agent with MCP tool awareness",
      "system": "You have access to powerful MCP tools. Use them intelligently: context7 for documentation and context management, github for git operations, puppeteer for web browsing, reddit for social media content, zen for general coordination tasks, memorybank for persistent memory, sequential for complex multi-step reasoning. Always consider which tools can help accomplish the user's goal.",
      "model": "openrouter/deepseek/deepseek-r1-0528:free"
    }
  },
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
      },
      "reddit": {
        "type": "local",
        "command": "mcp-server-reddit"
      }
    }
  },
  "share": "manual"
}
EOF
    
    success "OpenCode configuration created at $config_file"
}

# Set up environment variables
setup_env_vars() {
    highlight "Setting up environment variables..."
    
    # Check if API key is provided
    if [[ -z "$OPENROUTER_API_KEY" ]]; then
        warn "OPENROUTER_API_KEY not set. Please set it before using OpenRouter models."
        log "Example: export OPENROUTER_API_KEY='your-api-key-here'"
        log "Or add it to your ~/.bashrc or ~/.zshrc"
    fi
    
    # Environment variables to export
    local env_vars=(
        "OPENROUTER_API_KEY=$OPENROUTER_API_KEY"
    )
    
    # Add to shell profiles
    local profile_files=("$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile")
    for profile in "${profile_files[@]}"; do
        if [[ -f "$profile" ]]; then
            for var in "${env_vars[@]}"; do
                if ! grep -q "${var%%=*}=" "$profile" 2>/dev/null; then
                    echo "export $var" >> "$profile"
                fi
            done
        fi
    done
    
    # Export for current session
    for var in "${env_vars[@]}"; do
        export "$var"
    done
    
    success "Environment variables set"
}

# Create helper aliases
create_aliases() {
    highlight "Creating helper aliases..."
    
    local aliases_content='
# RalexOS/OpenCode helpers - AUTOPILOT is DEFAULT
alias opencode="command opencode --agent autopilot"   # DEFAULT: Smart autopilot mode
alias ocraw="command opencode"                         # Raw OpenCode without autopilot

# FREE models (prioritize these)
alias ocfr="command opencode --agent free-reasoning"  # DeepSeek R1 - best free reasoning
alias ocfc="command opencode --agent free-coding"     # Qwen Coder - best free coding
alias ocfb="command opencode --agent free-basic"      # Llama 3.2 - simple tasks

# CHEAP models (excellent value under $0.3/M)
alias occs="command opencode --agent cheap-smart"     # Gemini 2.5 Flash - best overall value
alias occf="command opencode --agent cheap-fast"      # GPT-4o Mini - reliable & fast
alias ocpc="command opencode --agent premium-coding"  # Qwen3 Coder - pro agentic coding

# SMART agents (MCP-aware)
alias ocs="command opencode --agent smart"            # Smart agent with tool awareness
alias ocy="command opencode --agent yolo"             # YOLO mode with aggressive tools
oy() { command opencode run "$@"; }
auto_mode() { 
    echo "Starting RalexOS auto mode..."
    while true; do
        command opencode -m openrouter/deepseek/deepseek-r1-0528:free run --agent yolo "$@"
        sleep 1
    done
}
'

    # Add to shell profiles
    local profile_files=("$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile")
    for profile in "${profile_files[@]}"; do
        if [[ -f "$profile" ]]; then
            if ! grep -q "# RalexOS/OpenCode helpers" "$profile" 2>/dev/null; then
                echo "$aliases_content" >> "$profile"
            fi
        fi
    done
    
    success "Helper aliases created"
}

# Verify installation
verify_installation() {
    highlight "Verifying installation..."
    
    # Check if required commands exist
    local required_commands=("opencode" "bun" "node" "npm")
    for cmd in "${required_commands[@]}"; do
        if command_exists "$cmd"; then
            success "Found $cmd"
        else
            warn "Missing $cmd"
        fi
    done
    
    # Check MCP servers
    local mcp_servers=("context7-mcp" "github-mcp-server" "server-puppeteer" 
                       "mcp-sequential-thinking" "zen-mcp-server" "memory-bank-mcp" "mcp-server-reddit")
    for server in "${mcp_servers[@]}"; do
        if command_exists "$server"; then
            success "Found MCP server: $server"
        else
            warn "Missing MCP server: $server"
        fi
    done
    
    # Check configuration
    local config_file="$HOME/.config/opencode/opencode.json"
    if [[ -f "$config_file" ]]; then
        success "Configuration file exists"
    else
        warn "Configuration file missing"
    fi
}

# Show usage instructions
show_usage() {
    echo
    highlight "Setup complete! To get started:"
    echo
    log "1. Restart your shell or run: source ~/.bashrc (or ~/.zshrc)"
    log "2. Use these commands (AUTOPILOT is default):"
    echo
    echo "   MAIN COMMANDS:"
    echo "   - opencode        : DEFAULT autopilot mode (figures everything out)"
    echo "   - ocs             : Smart agent (manual MCP tool selection)"
    echo "   - ocy             : YOLO mode (maximum autonomy)"
    echo "   - ocraw           : Raw OpenCode (no autopilot)"
    echo
    echo "   Say 'yolomode' in any chat to activate full YOLO!"
    echo
    echo "   FREE MODELS (backup options):"
    echo "   - ocfr            : Free reasoning (DeepSeek R1)"
    echo "   - ocfc            : Free coding (Qwen 2.5)"  
    echo "   - ocfb            : Free basic (Llama 3.2)"
    echo
    echo "   PAID MODELS (value-optimized 2025 lineup):"
    echo "   - occs            : Smart (Gemini 2.5 Flash ~$0.075/M)"
    echo "   - occf            : Fast (GPT-4o Mini ~$0.15/M)"
    echo "   - ocpc            : Pro Coding (Qwen3 ~$0.20/M)"
    echo "   - Use premium-reasoning (~$3/M) or premium-latest (~$10-30/M) via /agent"
    echo
    echo "   UTILITY:"
    echo "   - oy \"command\"    : One-shot command"
    echo "   - auto_mode       : Continuous mode"
    echo
    log "In OpenCode TUI, you can use these special commands:"
    echo "   - @yolo <task>    : Run in YOLO mode (no confirmations)"
    echo "   - /mcp            : Manage MCP servers"
    echo "   - /models         : Switch between models"
    echo
    log "MCP servers included:"
    echo "   - Context7        : Context management"
    echo "   - GitHub          : GitHub integration"
    echo "   - Puppeteer       : Web browsing"
    echo "   - Sequential      : Sequential thinking"
    echo "   - Zen             : General tools"
    echo "   - MemoryBank      : Memory management"
    echo "   - Reddit          : Reddit browsing, posts, comments"
    echo
}

# Main installation function
main() {
    log "Starting RalexOS setup..."
    
    # Check if we're running interactively
    if [[ $- == *i* ]]; then
        log "Running in interactive mode"
    else
        log "Running in non-interactive mode"
    fi
    
    # Install dependencies
    install_system_deps
    install_bun
    install_opencode
    
    # Set up Git and SSH
    setup_git
    generate_ssh_key
    
    # Install and configure MCP
    install_mcp_servers
    create_opencode_config
    setup_env_vars
    create_aliases
    
    # Verify and show usage
    verify_installation
    show_usage
    
    success "RalexOS setup complete!"
    log "Enjoy your AI-powered development environment!"
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi