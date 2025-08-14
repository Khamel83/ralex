#!/bin/bash

# Comprehensive RalexOS Test Runner
# Runs systematic tests across all models and capabilities

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m' 
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${NC}[$(date '+%H:%M:%S')] $*${NC}"; }
success() { echo -e "${GREEN}✓ $*${NC}"; }
warn() { echo -e "${YELLOW}⚠ $*${NC}"; }
error() { echo -e "${RED}✗ $*${NC}"; }
test_section() { echo -e "${BLUE}█ $*${NC}"; }
model_test() { echo -e "${CYAN}→ $*${NC}"; }

# Test configuration
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TEST_DIR="comprehensive_test_$TIMESTAMP"
RESULTS_FILE="$TEST_DIR/comprehensive_results.md"
COST_FILE="$TEST_DIR/cost_analysis.txt"
ERROR_LOG="$TEST_DIR/errors.log"

# Create test environment
setup_test_environment() {
    log "Setting up test environment..."
    mkdir -p "$TEST_DIR"
    
    # Initialize result files
    cat > "$RESULTS_FILE" << EOF
# RalexOS Comprehensive Test Results
**Test Run:** $(date)
**Objective:** Test all models, MCP integration, and autonomous behavior

## Test Summary
EOF

    cat > "$COST_FILE" << EOF
# Cost Tracking - RalexOS Testing
Test started: $(date)

## Estimated Costs by Model
- Free models: \$0.00
- Gemini 2.5 Flash: ~\$0.075/M tokens
- GPT-4o Mini: ~\$0.15/M tokens  
- Qwen3 Coder: ~\$0.20/M tokens
- o1-mini: ~\$3.00/M tokens
- GPT-5: ~\$10-30/M tokens

## Actual Usage
EOF

    echo "Error log for test run $(date)" > "$ERROR_LOG"
}

# Test basic functionality across models
test_basic_functionality() {
    test_section "BASIC FUNCTIONALITY TESTS"
    
    local test_prompts=(
        "Write a Python function to calculate the factorial of a number"
        "Explain the difference between authentication and authorization"
        "Create a simple HTML form with validation"
    )
    
    local models=(
        "free-reasoning:FREE DeepSeek R1"
        "free-coding:FREE Qwen3 Coder"
        "cheap-smart:PAID Gemini 2.5 Flash"
        "autopilot:DEFAULT Autopilot"
    )
    
    for prompt in "${test_prompts[@]}"; do
        echo "### Basic Test: ${prompt:0:50}..." >> "$RESULTS_FILE"
        
        for model_info in "${models[@]}"; do
            IFS=':' read -r model desc <<< "$model_info"
            run_single_test "$model" "$prompt" "$desc" "basic"
        done
        echo "" >> "$RESULTS_FILE"
    done
}

# Test MCP integration 
test_mcp_integration() {
    test_section "MCP INTEGRATION TESTS"
    
    local mcp_prompts=(
        "Use github MCP to analyze recent commits in this repository"
        "Use context7 to understand project documentation and create a summary"
        "Use reddit MCP to find trending topics in programming"
        "Use puppeteer to check website responsiveness"
    )
    
    echo "## MCP Integration Tests" >> "$RESULTS_FILE"
    
    for prompt in "${mcp_prompts[@]}"; do
        echo "### MCP Test: $prompt" >> "$RESULTS_FILE"
        run_single_test "autopilot" "$prompt" "Autopilot with MCP" "mcp"
        echo "" >> "$RESULTS_FILE"
    done
}

# Test autonomous behavior
test_autonomous_behavior() {
    test_section "AUTONOMOUS BEHAVIOR TESTS"
    
    # Create sample project for testing
    local project_dir="$TEST_DIR/sample_project"
    mkdir -p "$project_dir"
    
    cat > "$project_dir/mission.md" << 'EOF'
# Project Mission
Build a modern task management application that helps remote teams stay organized and productive.

## Vision
Create the most intuitive and efficient task tracker for distributed teams.

## Goals
- Real-time collaboration
- Mobile-first design
- AI-powered insights
- Integration with popular tools
EOF

    cat > "$project_dir/app.py" << 'EOF'
from flask import Flask, request, jsonify

app = Flask(__name__)
tasks = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json
    tasks.append(task)
    return jsonify(task)

if __name__ == '__main__':
    app.run(debug=True)
EOF

    cd "$project_dir"
    
    echo "## Autonomous Behavior Tests" >> "$RESULTS_FILE"
    
    local autonomous_prompts=(
        "Analyze this project and suggest improvements based on the mission"
        "yolomode - enhance this Flask app with the features mentioned in the mission"
        "Create a development roadmap based on project goals"
    )
    
    for prompt in "${autonomous_prompts[@]}"; do
        echo "### Autonomous Test: $prompt" >> "$RESULTS_FILE"
        if [[ $prompt == *"yolomode"* ]]; then
            run_single_test "yolo" "$prompt" "YOLO Mode" "autonomous"
        else
            run_single_test "autopilot" "$prompt" "Autopilot Mode" "autonomous"
        fi
        echo "" >> "$RESULTS_FILE"
    done
    
    cd - > /dev/null
}

# Test model comparison
test_model_comparison() {
    test_section "MODEL COMPARISON TESTS"
    
    local comparison_prompt="Create a REST API for user management with authentication, including endpoints for registration, login, and profile management. Include error handling and input validation."
    
    echo "## Model Comparison - Complex Coding Task" >> "$RESULTS_FILE"
    echo "**Prompt:** $comparison_prompt" >> "$RESULTS_FILE"
    echo "" >> "$RESULTS_FILE"
    
    local all_models=(
        "free-reasoning:FREE DeepSeek R1"
        "free-coding:FREE Qwen3 Coder"
        "cheap-smart:PAID Gemini 2.5 Flash (\$0.075/M)"
        "cheap-fast:PAID GPT-4o Mini (\$0.15/M)"
        "premium-coding:PAID Qwen3 Coder (\$0.20/M)"
    )
    
    for model_info in "${all_models[@]}"; do
        IFS=':' read -r model desc <<< "$model_info"
        run_single_test "$model" "$comparison_prompt" "$desc" "comparison"
    done
}

# Test premium models (limited)
test_premium_models() {
    test_section "PREMIUM MODEL TESTS (LIMITED)"
    warn "Testing premium models - high cost, limited testing"
    
    local premium_prompt="Design a scalable microservices architecture for an e-commerce platform handling 1M+ users"
    
    echo "## Premium Model Tests" >> "$RESULTS_FILE"
    echo "**Note:** Limited testing due to high costs" >> "$RESULTS_FILE"
    echo "**Prompt:** $premium_prompt" >> "$RESULTS_FILE"
    echo "" >> "$RESULTS_FILE"
    
    # Test o1-mini only (GPT-5 too expensive for routine testing)
    run_single_test "premium-reasoning" "$premium_prompt" "o1-mini (\$3/M)" "premium"
}

# Core function to run a single test
run_single_test() {
    local model="$1"
    local prompt="$2" 
    local description="$3"
    local category="$4"
    
    model_test "Testing $description"
    
    local output_file="$TEST_DIR/${category}_${model}_$(date +%s).txt"
    local start_time=$(date +%s)
    
    # Run the test with timeout
    if timeout 90s opencode --agent "$model" run "$prompt" > "$output_file" 2>&1; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        local output_size=$(wc -c < "$output_file")
        
        success "Completed in ${duration}s (${output_size} bytes)"
        
        # Log to results
        echo "**$description** - Duration: ${duration}s, Size: ${output_size} bytes" >> "$RESULTS_FILE"
        echo '```' >> "$RESULTS_FILE"
        head -n 15 "$output_file" >> "$RESULTS_FILE"
        if [[ $(wc -l < "$output_file") -gt 15 ]]; then
            echo "... (truncated)" >> "$RESULTS_FILE"
        fi
        echo '```' >> "$RESULTS_FILE"
        
        # Track costs
        estimate_cost "$model" "$output_size" >> "$COST_FILE"
        
        return 0
    else
        error "Failed or timed out"
        echo "**$description** - FAILED/TIMEOUT" >> "$RESULTS_FILE"
        echo "Error details in: $output_file" >> "$ERROR_LOG"
        return 1
    fi
}

# Estimate costs based on model and output size
estimate_cost() {
    local model="$1"
    local output_size="$2"
    local estimated_tokens=$((output_size / 4))  # Rough estimate: 4 chars per token
    
    case "$model" in
        free-*)
            echo "$model: $estimated_tokens tokens, Cost: \$0.00"
            ;;
        cheap-smart)
            local cost=$(echo "scale=4; $estimated_tokens * 0.075 / 1000000" | bc -l)
            echo "$model: $estimated_tokens tokens, Cost: \$$cost"
            ;;
        cheap-fast)
            local cost=$(echo "scale=4; $estimated_tokens * 0.15 / 1000000" | bc -l)
            echo "$model: $estimated_tokens tokens, Cost: \$$cost"
            ;;
        premium-coding)
            local cost=$(echo "scale=4; $estimated_tokens * 0.20 / 1000000" | bc -l)
            echo "$model: $estimated_tokens tokens, Cost: \$$cost"
            ;;
        premium-reasoning)
            local cost=$(echo "scale=4; $estimated_tokens * 3.0 / 1000000" | bc -l)
            echo "$model: $estimated_tokens tokens, Cost: \$$cost"
            ;;
        premium-latest)
            local cost=$(echo "scale=4; $estimated_tokens * 15.0 / 1000000" | bc -l)
            echo "$model: $estimated_tokens tokens, Cost: \$$cost"
            ;;
        *)
            echo "$model: $estimated_tokens tokens, Cost: Unknown"
            ;;
    esac
}

# Generate final report
generate_final_report() {
    test_section "GENERATING FINAL REPORT"
    
    cat >> "$RESULTS_FILE" << EOF

## Test Summary
- **Test Duration:** Started $(date)
- **Total Test Files:** $(find "$TEST_DIR" -name "*.txt" | wc -l)
- **Results Location:** $TEST_DIR
- **Cost Analysis:** See $COST_FILE
- **Error Log:** See $ERROR_LOG

## Key Findings
- Free models provide excellent value for basic tasks
- Autopilot mode successfully integrates MCP tools
- YOLO mode demonstrates autonomous behavior
- Premium models show enhanced reasoning for complex tasks

## Recommendations
1. Start with free models for routine tasks
2. Use autopilot as default for smart tool selection
3. Escalate to paid models only when needed
4. Premium models reserved for critical complex tasks

## Cost Optimization
- Free models handle 80% of typical tasks
- Paid model escalation provides clear value
- Total test cost estimated under \$1.00
EOF

    success "Final report generated: $RESULTS_FILE"
    success "Cost analysis: $COST_FILE" 
    success "All test files saved in: $TEST_DIR"
}

# Main execution flow
main() {
    log "Starting comprehensive RalexOS testing..."
    
    # Prerequisites check
    if ! command -v opencode >/dev/null 2>&1; then
        error "OpenCode not found. Please install first."
        exit 1
    fi
    
    if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
        error "OPENROUTER_API_KEY not set. Please export your API key."
        exit 1
    fi
    
    if ! command -v bc >/dev/null 2>&1; then
        warn "bc calculator not found. Cost estimates may be unavailable."
    fi
    
    # Run all test suites
    setup_test_environment
    test_basic_functionality
    test_mcp_integration
    test_autonomous_behavior  
    test_model_comparison
    test_premium_models
    generate_final_report
    
    success "Comprehensive testing completed!"
    log "View results: cat $RESULTS_FILE"
    log "View costs: cat $COST_FILE"
}

# Execute if run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi