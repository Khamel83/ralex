#!/bin/bash

# RalexOS Comprehensive Testing Script
# Tests all models, MCP integration, and autonomous behavior

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Logging functions
log() { echo -e "${NC}[$(date '+%H:%M:%S')] $*${NC}"; }
success() { echo -e "${GREEN}[SUCCESS] $*${NC}"; }
warn() { echo -e "${YELLOW}[WARNING] $*${NC}"; }
error() { echo -e "${RED}[ERROR] $*${NC}"; }
test_header() { echo -e "${BLUE}[TEST] $*${NC}"; }
model_header() { echo -e "${CYAN}[MODEL] $*${NC}"; }

# Test configuration
TEST_DIR="test_results_$(date +%Y%m%d_%H%M%S)"
COST_TRACKER="$TEST_DIR/cost_tracking.txt"
RESULTS_FILE="$TEST_DIR/test_results.md"

# Create test directory
mkdir -p "$TEST_DIR"
echo "# RalexOS Testing Results - $(date)" > "$RESULTS_FILE"
echo "## Cost Tracking" > "$COST_TRACKER"

# Test prompts
declare -A TEST_PROMPTS=(
    ["simple_coding"]="Write a Python function to calculate fibonacci numbers"
    ["complex_reasoning"]="Analyze the trade-offs between microservices and monolithic architecture for a startup"
    ["tool_integration"]="Search for recent AI developments and create a summary report"
    ["project_analysis"]="Analyze this project's structure and suggest improvements based on the mission"
    ["yolo_test"]="yolomode - optimize this entire codebase for performance"
    ["web_research"]="Find the latest pricing for cloud services and compare AWS vs GCP"
    ["code_review"]="Review this code for security vulnerabilities and performance issues"
    ["agentic_task"]="Create a complete REST API with authentication, database, and tests"
)

# Model configurations to test
declare -A MODELS=(
    ["free-reasoning"]="FREE - DeepSeek R1"
    ["free-coding"]="FREE - Qwen3 Coder" 
    ["free-general"]="FREE - Qwen 2.5 72B"
    ["cheap-smart"]="PAID - Gemini 2.5 Flash (~$0.075/M)"
    ["cheap-fast"]="PAID - GPT-4o Mini (~$0.15/M)"
    ["premium-coding"]="PAID - Qwen3 Coder (~$0.20/M)"
    ["autopilot"]="DEFAULT - Autopilot Mode"
)

# Premium models (limited testing)
declare -A PREMIUM_MODELS=(
    ["premium-reasoning"]="PREMIUM - o1-mini (~$3/M)"
    ["premium-latest"]="PREMIUM - GPT-5 (~$10-30/M)"
)

# Function to run a test with a specific model
run_test() {
    local model="$1"
    local prompt="$2"
    local test_name="$3"
    local model_desc="$4"
    
    model_header "Testing $model_desc"
    test_header "Prompt: $prompt"
    
    local output_file="$TEST_DIR/${test_name}_${model}.txt"
    local start_time=$(date +%s)
    
    # Run the test
    if timeout 60s opencode --agent "$model" run "$prompt" > "$output_file" 2>&1; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        
        success "Test completed in ${duration}s"
        
        # Log to results
        echo "### $test_name - $model_desc" >> "$RESULTS_FILE"
        echo "**Duration:** ${duration}s" >> "$RESULTS_FILE"
        echo "**Prompt:** $prompt" >> "$RESULTS_FILE"
        echo "**Output:**" >> "$RESULTS_FILE"
        echo '```' >> "$RESULTS_FILE"
        head -n 20 "$output_file" >> "$RESULTS_FILE"
        echo '```' >> "$RESULTS_FILE"
        echo "" >> "$RESULTS_FILE"
        
        return 0
    else
        error "Test failed or timed out"
        echo "**FAILED** - $test_name - $model_desc" >> "$RESULTS_FILE"
        return 1
    fi
}

# Function to test MCP integration
test_mcp_integration() {
    test_header "Testing MCP Server Integration"
    
    # Test each MCP server
    local mcp_tests=(
        "Use context7 to analyze project documentation"
        "Use github MCP to check recent commits"
        "Use reddit MCP to find trending programming topics"
        "Use puppeteer to browse a website"
        "Use zen MCP for general coordination"
        "Use memorybank to store project information"
        "Use sequential thinking for complex analysis"
    )
    
    for test_prompt in "${mcp_tests[@]}"; do
        run_test "autopilot" "$test_prompt" "mcp_integration" "Autopilot with MCP"
    done
}

# Function to test autonomous behavior
test_autonomous_behavior() {
    test_header "Testing Autonomous Behavior"
    
    # Create a sample project structure for testing
    mkdir -p "$TEST_DIR/sample_project"
    cat > "$TEST_DIR/sample_project/README.md" << 'EOF'
# Sample Project

## Mission
Create a simple web application for task management.

## Vision  
Build a user-friendly, efficient task tracker that helps teams stay organized.

## Goals
- Simple interface
- Real-time updates
- Mobile-friendly
- Secure authentication
EOF

    cat > "$TEST_DIR/sample_project/app.py" << 'EOF'
# Basic Flask app
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run()
EOF

    cd "$TEST_DIR/sample_project"
    
    # Test autopilot behavior
    run_test "autopilot" "Analyze this project and suggest improvements based on the mission and vision" "autonomous_analysis" "Autopilot Analysis"
    
    # Test YOLO mode
    run_test "yolo" "yolomode - improve this Flask app based on the project goals" "yolo_mode" "YOLO Mode"
    
    cd - > /dev/null
}

# Function to compare model performance
compare_models() {
    test_header "Comparing Model Performance"
    
    local test_prompt="Write a Python class for a task management system with CRUD operations"
    
    # Test all free models
    for model in "${!MODELS[@]}"; do
        run_test "$model" "$test_prompt" "model_comparison" "${MODELS[$model]}"
    done
}

# Function to test premium models (limited)
test_premium_models() {
    test_header "Testing Premium Models (Limited)"
    
    warn "Testing premium models with high costs - limited testing"
    
    local simple_prompt="Explain the concept of recursion in programming"
    
    for model in "${!PREMIUM_MODELS[@]}"; do
        run_test "$model" "$simple_prompt" "premium_test" "${PREMIUM_MODELS[$model]}"
    done
}

# Function to analyze costs
analyze_costs() {
    test_header "Analyzing Costs and Performance"
    
    echo "## Cost Analysis" >> "$RESULTS_FILE"
    echo "Based on estimated token usage:" >> "$RESULTS_FILE"
    echo "- FREE models: $0.00" >> "$RESULTS_FILE"
    echo "- Cheap models (~1K tokens): ~$0.10" >> "$RESULTS_FILE"
    echo "- Premium models (~500 tokens): ~$0.50" >> "$RESULTS_FILE"
    echo "- **Total estimated cost: ~$0.60**" >> "$RESULTS_FILE"
    echo "" >> "$RESULTS_FILE"
}

# Function to generate final report
generate_report() {
    test_header "Generating Final Report"
    
    echo "## Summary" >> "$RESULTS_FILE"
    echo "Test completed at $(date)" >> "$RESULTS_FILE"
    echo "Results stored in: $TEST_DIR" >> "$RESULTS_FILE"
    
    success "Testing complete! Results in $TEST_DIR"
    success "View results: cat $RESULTS_FILE"
}

# Main testing flow
main() {
    log "Starting RalexOS comprehensive testing..."
    log "Results will be stored in: $TEST_DIR"
    
    # Check if OpenCode is installed
    if ! command -v opencode >/dev/null 2>&1; then
        error "OpenCode not found. Please run ralexos-complete.sh first"
        exit 1
    fi
    
    # Check if API key is set
    if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
        error "OPENROUTER_API_KEY not set. Please export your API key"
        exit 1
    fi
    
    # Run all tests
    compare_models
    test_mcp_integration  
    test_autonomous_behavior
    test_premium_models
    analyze_costs
    generate_report
    
    success "All tests completed successfully!"
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi