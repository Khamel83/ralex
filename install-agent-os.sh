#!/bin/bash
# Agent-OS Universal Installer - Khamel83 Edition
# Installs Agent-OS structure for Claude Code, Cursor, and Gemini CLI
# Usage: curl -sSL https://raw.githubusercontent.com/Khamel83/agent-os/main/install.sh | bash

set -e

echo "🚀 Agent-OS Universal Installer - Khamel83 Edition"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Check if we're in a valid directory
check_directory() {
    if [[ ! -w . ]]; then
        log_error "Cannot write to current directory. Please run from a writable location."
        exit 1
    fi
    
    # Check if this looks like a project directory
    if [[ -f "package.json" ]] || [[ -f "pyproject.toml" ]] || [[ -f "Cargo.toml" ]] || [[ -f "go.mod" ]] || [[ -f "pom.xml" ]]; then
        log_info "Detected project directory"
    else
        log_warning "No project files detected. This installer works best in project directories."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Detect tools available
detect_tools() {
    local tools_found=()
    
    # Check for Claude Code
    if command -v claude &> /dev/null; then
        tools_found+=("claude-code")
        log_success "Claude Code detected"
    fi
    
    # Check for Cursor (look for cursor command or Cursor.app)
    if command -v cursor &> /dev/null || [[ -d "/Applications/Cursor.app" ]]; then
        tools_found+=("cursor")
        log_success "Cursor detected"
    fi
    
    # Check for Gemini CLI
    if command -v gemini &> /dev/null; then
        tools_found+=("gemini-cli")
        log_success "Gemini CLI detected"
    fi
    
    if [[ ${#tools_found[@]} -eq 0 ]]; then
        log_warning "No AI coding tools detected. Installing base Agent-OS structure."
        tools_found+=("base")
    fi
    
    echo "${tools_found[@]}"
}

# Download latest Agent-OS from buildermethods (upstream)
download_upstream_agent_os() {
    log_info "Downloading latest Agent-OS from buildermethods/agent-os..."
    
    if command -v git &> /dev/null; then
        # If git is available, clone to temp directory
        local temp_dir=$(mktemp -d)
        git clone --depth 1 https://github.com/buildermethods/agent-os.git "$temp_dir" 2>/dev/null
        
        if [[ -d "$temp_dir/.agent-os" ]]; then
            cp -r "$temp_dir/.agent-os" .
            log_success "Downloaded upstream Agent-OS structure"
        else
            log_warning "Upstream structure not found, creating minimal structure"
            create_minimal_agent_os
        fi
        
        rm -rf "$temp_dir"
    else
        log_warning "Git not available, creating minimal Agent-OS structure"
        create_minimal_agent_os
    fi
}

# Create minimal Agent-OS structure if download fails
create_minimal_agent_os() {
    mkdir -p .agent-os/{standards,workflows,task-specs,philosophy}
    
    cat > .agent-os/README.md << 'EOF'
# Agent-OS Installation

This directory contains the Agent-OS structure for improved AI coding assistance.

## Structure
- `standards/` - Coding standards and best practices
- `workflows/` - Development workflow specifications  
- `task-specs/` - Specific task instructions
- `philosophy/` - Core principles and methodologies

## Tools Supported
- Claude Code (via CLAUDE.md)
- Cursor (via .cursorrules)
- Gemini CLI (via GEMINI.md)

For more information: https://github.com/Khamel83/agent-os
EOF

    log_success "Created minimal Agent-OS structure"
}

# Create Khamel83 enhancement layer
create_khamel83_layer() {
    log_info "Creating Khamel83 enhancement layer..."
    
    mkdir -p .khamel83/{ralex-enhancements,cost-optimization,model-routing,cache}
    
    cat > .khamel83/README.md << 'EOF'
# Khamel83 Agent-OS Enhancements

This layer adds cost optimization and Ralex-specific enhancements to Agent-OS.

## Cost Optimization Strategy
- Use expensive models for planning/architecture
- Route implementation to cheap models via LiteLLM
- Cache solutions and patterns for reuse
- Break complex tasks into micro-tasks

## Components
- `ralex-enhancements/` - Ralex-specific integrations
- `cost-optimization/` - Cost-saving strategies and templates
- `model-routing/` - LiteLLM routing configurations
- `cache/` - Cached solutions and patterns

## Integration
Works with standard Agent-OS while adding intelligence for cost optimization.
EOF

    # Create cost optimization templates
    cat > .khamel83/cost-optimization/task-breakdown.md << 'EOF'
# Task Breakdown Template

Use this template to break expensive tasks into cheap micro-tasks.

## Original Task
[Describe the complex task that would normally cost $50]

## Breakdown Strategy
1. **Planning Phase (Expensive Model)**
   - Architecture decisions
   - High-level approach
   - Risk assessment

2. **Implementation Phases (Cheap Models)**
   - [ ] Micro-task 1: [specific, small task]
   - [ ] Micro-task 2: [specific, small task]
   - [ ] Micro-task 3: [specific, small task]

3. **Review Phase (Medium Model)**
   - Integration testing
   - Error handling
   - Performance optimization

## Cost Estimate
- Planning: $1-2 (expensive model, short session)
- Implementation: $0.10-0.50 (cheap models, multiple tasks)
- Review: $0.25-0.50 (medium model, focused review)
- **Total: ~$1.50 instead of $50**
EOF

    # Create LiteLLM routing config
    cat > .khamel83/model-routing/litellm-config.yaml << 'EOF'
# LiteLLM Configuration for Cost Optimization
# Place this in your project root as litellm_config.yaml

model_list:
  # Planning/Architecture - Expensive but smart
  - model_name: planning
    litellm_params:
      model: openrouter/anthropic/claude-3.5-sonnet
      api_key: os.environ/OPENROUTER_API_KEY
      
  # Implementation - Cheap and fast  
  - model_name: implementation
    litellm_params:
      model: openrouter/meta-llama/llama-3.1-8b-instruct
      api_key: os.environ/OPENROUTER_API_KEY
      
  # Review/Debug - Medium cost and capability
  - model_name: review
    litellm_params:
      model: openrouter/anthropic/claude-3-haiku
      api_key: os.environ/OPENROUTER_API_KEY

# Router settings for intelligent routing
router_settings:
  routing_strategy: "cost-optimization"
  fallback_models: ["planning"]
  retry_count: 2
EOF

    log_success "Created Khamel83 enhancement layer"
}

# Create Claude Code configuration
create_claude_config() {
    log_info "Creating CLAUDE.md configuration..."
    
    cat > CLAUDE.md << 'EOF'
# Claude Code Configuration - Khamel83 Edition

## Project Overview
This project uses Agent-OS for intelligent cost optimization and development workflow management.

## Cost Optimization Strategy
**Goal: Achieve $50 worth of results for $1 using smart model routing**

### Model Usage Pattern
1. **Planning Phase**: Use expensive models (Claude 3.5 Sonnet) for:
   - Architecture decisions
   - High-level problem solving
   - Complex reasoning tasks

2. **Implementation Phase**: Use cheap models (Llama 3.1 8B) for:
   - Code generation from detailed specs
   - Repetitive tasks
   - Simple modifications

3. **Review Phase**: Use medium models (Claude Haiku) for:
   - Code review and debugging
   - Integration testing
   - Performance optimization

### Task Breakdown Approach
- Break complex requests into micro-tasks
- Use cached solutions when possible
- Leverage Agent-OS templates and patterns
- Minimize expensive model usage

## Agent-OS Integration
- **Standards**: Follow `.agent-os/standards/` for coding practices
- **Workflows**: Use `.agent-os/workflows/` for development processes
- **Cost Templates**: Reference `.khamel83/cost-optimization/` for efficient task breakdown

## LiteLLM Routing
This project uses LiteLLM for intelligent model routing. Configuration in `.khamel83/model-routing/litellm-config.yaml`.

## Context Management
- Relevant files are in `.agent-os/` and `.khamel83/`
- Cache successful patterns in `.khamel83/cache/`
- Document cost savings in session logs

## Development Workflow
1. **Analyze task complexity** - determine if planning phase needed
2. **Break down into micro-tasks** - use cost optimization templates
3. **Route to appropriate models** - let LiteLLM handle routing
4. **Cache successful patterns** - for future reuse
5. **Track cost savings** - measure efficiency gains

Remember: The goal is maximum value with minimum cost through intelligent task decomposition and model routing.
EOF

    log_success "Created CLAUDE.md configuration"
}

# Create Gemini CLI configuration
create_gemini_config() {
    log_info "Creating GEMINI.md configuration..."
    
    cat > GEMINI.md << 'EOF'
# Gemini CLI Configuration - Khamel83 Edition

## Project Overview
This project uses Agent-OS for intelligent cost optimization and development workflow management.

## Gemini CLI Integration
Use Gemini CLI for "vibe coding" and quick iterations alongside the cost-optimized Ralex system.

### Usage Patterns
- **Quick Exploration**: Use Gemini for rapid codebase exploration
- **Multimodal Tasks**: Leverage Gemini's image/document understanding
- **Iterative Development**: Fast feedback loops for development

### Agent-OS Integration
- **Standards**: Follow `.agent-os/standards/` for coding practices
- **Workflows**: Use `.agent-os/workflows/` for development processes
- **Context**: Reference project structure in `.agent-os/` and `.khamel83/`

### Cost Optimization
While Gemini CLI is used for exploration, refer to the main Ralex system (via Claude Code/Cursor) for cost-optimized production work:

1. **Explore with Gemini** - understand problems and possibilities
2. **Plan with Ralex** - create cost-effective implementation strategy  
3. **Implement efficiently** - use Agent-OS breakdown templates
4. **Review and iterate** - combine both tools as needed

### Workflow Integration
- Use Gemini CLI for initial exploration and understanding
- Switch to Ralex/LiteLLM routing for cost-effective implementation
- Return to Gemini for complex multimodal tasks when needed

### Context Files
- **Agent-OS Structure**: `.agent-os/` directory
- **Cost Optimization**: `.khamel83/cost-optimization/`
- **Cached Patterns**: `.khamel83/cache/`
- **Model Routing**: `.khamel83/model-routing/`

The goal is to use each tool for its strengths while maintaining cost efficiency through Agent-OS structure.
EOF

    log_success "Created GEMINI.md configuration"
}

# Create Cursor configuration
create_cursor_config() {
    log_info "Creating .cursorrules configuration..."
    
    cat > .cursorrules << 'EOF'
# Cursor Rules - Khamel83 Agent-OS Edition

## Cost Optimization First
This project prioritizes cost efficiency through intelligent model routing and task decomposition.

### Development Strategy
- Break complex tasks into micro-tasks for cheaper execution
- Use cached solutions from `.khamel83/cache/` when available
- Follow Agent-OS standards in `.agent-os/standards/`
- Leverage LiteLLM routing for optimal model selection

### File Structure Awareness
Key directories:
- `.agent-os/` - Core Agent-OS structure (standards, workflows, task-specs)
- `.khamel83/` - Cost optimization enhancements and Ralex integration
- `.khamel83/cost-optimization/` - Templates for efficient task breakdown
- `.khamel83/model-routing/` - LiteLLM configuration

### Coding Standards
Follow standards defined in `.agent-os/standards/` and reference workflow patterns in `.agent-os/workflows/`.

### Task Approach
1. Check `.khamel83/cache/` for existing solutions
2. Break complex requests into smaller, focused tasks
3. Use cost optimization templates from `.khamel83/cost-optimization/`
4. Document successful patterns for future reuse

### Context Priority
When referencing files, prioritize:
1. Current task requirements
2. Agent-OS standards and workflows
3. Cached solutions and patterns
4. Cost optimization strategies

### Integration Notes
This project integrates with Ralex for intelligent model routing via LiteLLM. Cursor should work alongside this system, not replace it.

Goal: Maximum development efficiency with minimum cost through Agent-OS structure and intelligent tooling.
EOF

    log_success "Created .cursorrules configuration"
}

# Create installation status file
create_status_file() {
    local tools=("$@")
    
    cat > agent-os-status.json << EOF
{
    "installation_date": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "version": "khamel83-v1.0",
    "upstream_source": "buildermethods/agent-os",
    "detected_tools": [$(printf '"%s",' "${tools[@]}" | sed 's/,$//')],
    "structure": {
        "agent_os": ".agent-os/",
        "khamel83_layer": ".khamel83/",
        "claude_config": "CLAUDE.md",
        "gemini_config": "GEMINI.md", 
        "cursor_config": ".cursorrules"
    },
    "features": [
        "cost-optimization",
        "model-routing",
        "task-decomposition",
        "solution-caching",
        "multi-tool-support"
    ]
}
EOF

    log_success "Created installation status file"
}

# Show completion message and next steps
show_completion() {
    local tools=("$@")
    
    echo ""
    echo "🎉 Agent-OS Universal Installation Complete!"
    echo "==========================================="
    echo ""
    
    log_success "Installed Agent-OS structure for: ${tools[*]}"
    echo ""
    
    echo "📁 Created Structure:"
    echo "   .agent-os/          - Core Agent-OS (synced from upstream)"
    echo "   .khamel83/          - Your cost optimization enhancements"
    echo "   CLAUDE.md           - Claude Code configuration"
    echo "   GEMINI.md           - Gemini CLI configuration"
    echo "   .cursorrules        - Cursor configuration"
    echo "   agent-os-status.json - Installation tracking"
    echo ""
    
    echo "🚀 Next Steps:"
    if [[ " ${tools[@]} " =~ " claude-code " ]]; then
        echo "   • Claude Code: Ready to use! Context is in CLAUDE.md"
    fi
    if [[ " ${tools[@]} " =~ " cursor " ]]; then
        echo "   • Cursor: Ready to use! Rules are in .cursorrules"
    fi
    if [[ " ${tools[@]} " =~ " gemini-cli " ]]; then
        echo "   • Gemini CLI: Ready to use! Context is in GEMINI.md"
    fi
    echo ""
    
    echo "💰 Cost Optimization:"
    echo "   • Review templates in .khamel83/cost-optimization/"
    echo "   • Configure LiteLLM routing in .khamel83/model-routing/"
    echo "   • Start caching solutions in .khamel83/cache/"
    echo ""
    
    echo "📖 Documentation:"
    echo "   • cat .agent-os/README.md        - Core Agent-OS info"
    echo "   • cat .khamel83/README.md        - Cost optimization features"
    echo "   • cat agent-os-status.json       - Installation details"
    echo ""
    
    log_info "Repository: https://github.com/Khamel83/agent-os"
}

# Main installation flow
main() {
    echo "Starting installation in: $(pwd)"
    echo ""
    
    # Pre-flight checks
    check_directory
    
    # Detect available tools
    local tools=($(detect_tools))
    echo ""
    
    # Download and setup Agent-OS
    download_upstream_agent_os
    
    # Create enhancement layer
    create_khamel83_layer
    
    # Create tool-specific configurations
    if [[ " ${tools[@]} " =~ " claude-code " ]] || [[ " ${tools[@]} " =~ " base " ]]; then
        create_claude_config
    fi
    
    if [[ " ${tools[@]} " =~ " gemini-cli " ]] || [[ " ${tools[@]} " =~ " base " ]]; then
        create_gemini_config
    fi
    
    if [[ " ${tools[@]} " =~ " cursor " ]] || [[ " ${tools[@]} " =~ " base " ]]; then
        create_cursor_config
    fi
    
    # Create status tracking
    create_status_file "${tools[@]}"
    
    # Show completion message
    show_completion "${tools[@]}"
}

# Run main function
main "$@"