#!/bin/bash

echo "🧪 Testing OpenRouter fallback..."
echo ""

# Read the test prompt
echo "📄 Using test prompt from test_prompt.txt"
PROMPT=$(cat test_prompt.txt)

echo ""
echo "🔄 Running OpenRouter directly for testing..."
echo ""

# Run our force-openrouter script with the prompt and save output
./ralex-force-openrouter.sh "$PROMPT" > openrouter_response.txt 2>&1

echo "✅ OpenRouter response saved to openrouter_response.txt"
echo ""
echo "📊 Files created for comparison:"
echo "  - test_prompt.txt (the prompt)"
echo "  - claude_code_response.js (Claude Code's response)"  
echo "  - openrouter_response.txt (OpenRouter's response)"
echo ""
echo "You can now compare the two responses!"