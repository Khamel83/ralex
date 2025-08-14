#!/bin/bash

# Test all 5 AI models with the same complex prompt
# Load API key from .env
if [ -f ".env" ]; then
    source .env
elif [ -f "/Users/hr-svp-mac12/Library/Mobile Documents/com~apple~CloudDocs/ralex/.env" ]; then
    source "/Users/hr-svp-mac12/Library/Mobile Documents/com~apple~CloudDocs/ralex/.env"
fi

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ OPENROUTER_API_KEY not found in .env file"
    exit 1
fi

echo "🧪 Testing 5 AI Models with Complex JavaScript Refactoring Task"
echo "============================================================="

# Read the test prompt
PROMPT=$(cat test_prompt.txt)

# Define the models to test
declare -A MODELS=(
    ["gemini_flash"]="google/gemini-2.0-flash-001"
    ["deepseek_v3"]="deepseek/deepseek-chat-v3-0324:free" 
    ["qwen_coder"]="qwen/qwen3-coder:free"
    ["qwen_14b"]="qwen/qwen3-14b:free"
)

# Function to call OpenRouter API
call_openrouter() {
    local model=$1
    local output_file=$2
    
    echo "🔄 Testing $model..."
    
    curl -s -X POST \
        "https://openrouter.ai/api/v1/chat/completions" \
        -H "Authorization: Bearer $OPENROUTER_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$model\",
            \"messages\": [
                {\"role\": \"user\", \"content\": \"$PROMPT\"}
            ]
        }" | jq -r '.choices[0].message.content' > "$output_file"
    
    if [ $? -eq 0 ] && [ -s "$output_file" ]; then
        echo "✅ $model response saved to $output_file"
    else
        echo "❌ Failed to get response from $model"
        echo "Error details:" >> "$output_file"
        cat "$output_file"
    fi
    echo ""
}

# Test each model
for name in "${!MODELS[@]}"; do
    call_openrouter "${MODELS[$name]}" "${name}_response.txt"
    sleep 1  # Brief pause between requests
done

echo "📊 Comparison Files Created:"
echo "=========================="
echo "✅ claude_code_response.js (Claude Code/Sonnet 4 - already created)"
echo "✅ gemini_flash_response.txt (Google Gemini 2.0 Flash - \$0.25/1M tokens)"
echo "✅ deepseek_v3_response.txt (DeepSeek Chat v3 - FREE)"
echo "✅ qwen_coder_response.txt (Qwen3 Coder - FREE)"
echo "✅ qwen_14b_response.txt (Qwen3 14B - FREE)"
echo ""
echo "🎯 Ready for comparison! You can now analyze:"
echo "   • Code quality and modern patterns"
echo "   • Error handling sophistication"  
echo "   • Documentation detail"
echo "   • Performance considerations"
echo "   • Edge case handling"
echo ""
echo "💡 Tip: Use 'ls -la *response*' to see all response files"