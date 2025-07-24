#!/bin/bash
# Ralex V2 - Final Production Version with LiteLLM

# Set colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Check if API key is set
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo -e "${RED}❌ OPENROUTER_API_KEY not set${NC}"
    echo "Get your free API key from https://openrouter.ai/"
    echo "Then run: export OPENROUTER_API_KEY='your-key-here'"
    exit 1
fi

# Check if prompt provided
if [ $# -eq 0 ]; then
    echo -e "${BLUE}🚀 Ralex V2 - LiteLLM Budget-Aware AI Coding Assistant${NC}"
    echo ""
    echo -e "${PURPLE}✨ Now with REAL LiteLLM model selection!${NC}"
    echo ""
    echo "Usage: $0 \"your coding request\""
    echo ""
    echo "Examples:"
    echo -e "  $0 \"${GREEN}fix this syntax error${NC}\"           # → LiteLLM chooses cheap model"
    echo -e "  $0 \"${YELLOW}refactor this architecture${NC}\"      # → LiteLLM chooses smart model"  
    echo -e "  $0 \"${RED}yolo fix this bug now${NC}\"           # → LiteLLM ultra-fast mode"
    echo ""
    echo "Options:"
    echo "  $0 --budget                            # Show budget status"
    echo "  $0 \"request\" --model model-name       # Force specific model"
    echo ""
    echo -e "${PURPLE}🎯 LiteLLM automatically selects the best model for your request!${NC}"
    exit 0
fi

# Show budget if requested  
if [ "$1" = "--budget" ]; then
    python3 $(dirname "$0")/litellm-ralex.py "test" --budget
    exit 0
fi

# Run the request with LiteLLM
echo -e "${GREEN}🤖 LiteLLM processing your request...${NC}"
python3 $(dirname "$0")/litellm-ralex.py "$@"