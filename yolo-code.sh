#!/bin/bash
# Production wrapper for Ralex V2 - Budget-Aware AI Coding

# Set colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
    echo -e "${BLUE}🚀 Ralex V2 - Budget-Aware AI Coding Assistant${NC}"
    echo ""
    echo "Usage: $0 \"your coding request\""
    echo ""
    echo "Examples:"
    echo "  $0 \"fix this syntax error\"           # → Cheap model"
    echo "  $0 \"refactor this architecture\"      # → Smart model"  
    echo "  $0 \"yolo fix this bug now\"           # → Ultra-fast mode"
    echo ""
    echo "Options:"
    echo "  $0 --budget                            # Show budget status"
    echo "  $0 \"request\" --model model-name       # Force specific model"
    exit 0
fi

# Show budget if requested  
if [ "$1" = "--budget" ]; then
    python3 direct-openrouter-test.py "test" --budget
    exit 0
fi

# Run the request
echo -e "${GREEN}🤖 Processing your request...${NC}"
python3 $(dirname "$0")/direct-openrouter-test.py "$@"