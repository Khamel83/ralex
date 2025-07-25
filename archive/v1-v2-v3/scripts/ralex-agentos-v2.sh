#!/bin/bash
#
# Ralex V2 with AgentOS Integration
# Cost-optimized AI coding with smart prompt structuring
#

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if API key is set
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo -e "${RED}❌ Error: OPENROUTER_API_KEY not set${NC}"
    echo "Get your key from https://openrouter.ai/ and set it:"
    echo "export OPENROUTER_API_KEY='your-key-here'"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".ralex-env" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Setting up...${NC}"
    python3 -m venv .ralex-env
    source .ralex-env/bin/activate
    pip install -r requirements.txt
else
    source .ralex-env/bin/activate
fi

# Banner
echo -e "${PURPLE}🚀 Ralex V2 with AgentOS Integration${NC}"
echo -e "${CYAN}💡 Smart prompt structuring: Expensive analysis + Cheap execution${NC}"
echo -e "${GREEN}📊 AgentOS standards automatically applied${NC}"
echo ""

# Check if running in interactive mode or with arguments
if [ $# -eq 0 ]; then
    # Interactive mode
    echo -e "${BLUE}🎯 Starting interactive mode with AgentOS...${NC}"
    echo ""
    python -m ralex_core.launcher run
else
    # Direct execution mode
    PROMPT="$*"
    echo -e "${GREEN}🤖 Processing: ${PROMPT}${NC}"
    echo ""
    
    # Create a temporary Python script for direct execution
    cat > /tmp/ralex_direct.py << EOF
#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from ralex_core.agentos_integration import AgentOSIntegration

# Initialize AgentOS
agentos = AgentOSIntegration()

# Analyze the prompt
prompt = "${PROMPT}"
file_context = {}  # Would need file context for full execution

# Show breakdown preview
breakdown = agentos.structure_smart_prompt(prompt, file_context)

print("🧠 AgentOS Analysis:")
print(f"   Task: {prompt}")
print(f"   Complexity: {breakdown.complexity}")
print(f"   Estimated cost: \${breakdown.estimated_cost:.4f}")

if breakdown.complexity == "low":
    print("   Strategy: Direct execution (cheap model)")
    print("   💡 This task can be executed immediately with a cheap model")
else:
    print("   Strategy: Analysis first (smart model), then execution (cheap models)")
    print("   💡 Complex task - will use smart model for analysis, then cheap models for execution")
    print(f"   Expected: {len(breakdown.execution_tasks) if breakdown.execution_tasks else '3-7'} execution tasks")

print()
print("🎯 To execute this task:")
print("   1. Add files to context: ralex-agentos-v2.sh (then use /add command)")
print("   2. Or use interactive mode: ralex-agentos-v2.sh")
print("   3. Or use breakdown command: /breakdown ${PROMPT}")
EOF
    
    python3 /tmp/ralex_direct.py
    rm /tmp/ralex_direct.py
fi