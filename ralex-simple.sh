#!/bin/bash

# Simple Ralex - Direct OpenRouter fallback when Claude fails
# Load API key from .env (check current dir and ralex project dir)
if [ -f ".env" ]; then
    source .env
elif [ -f "/Users/hr-svp-mac12/Library/Mobile Documents/com~apple~CloudDocs/ralex/.env" ]; then
    source "/Users/hr-svp-mac12/Library/Mobile Documents/com~apple~CloudDocs/ralex/.env"
fi

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ OPENROUTER_API_KEY not found in .env file"
    echo "Please add: OPENROUTER_API_KEY=your-key-here"
    exit 1
fi

echo "🤖 Ralex - Always-Working Claude"
echo "Trying Claude first..."

# Try Claude first
if claude "$@" 2>&1 | grep -q "usage limit"; then
    echo "⚠️ Claude limit reached, switching to OpenRouter..."
    
    # Simple OpenRouter API call
    if [ $# -eq 0 ]; then
        echo "Interactive mode not supported with OpenRouter fallback"
        echo "Please use: ralex-simple \"your prompt here\""
        exit 1
    fi
    
    # Combine all arguments into one prompt
    PROMPT="$*"
    
    curl -X POST \
        "https://openrouter.ai/api/v1/chat/completions" \
        -H "Authorization: Bearer $OPENROUTER_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"meta-llama/llama-3.1-8b-instruct:free\",
            \"messages\": [
                {\"role\": \"user\", \"content\": \"$PROMPT\"}
            ]
        }" | jq -r '.choices[0].message.content'
else
    echo "✅ Claude worked normally"
fi