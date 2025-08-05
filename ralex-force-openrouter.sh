#!/bin/bash

# Force OpenRouter for testing (bypasses Claude entirely)
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

echo "🤖 Ralex - Forcing OpenRouter for testing..."

# Combine all arguments into one prompt
PROMPT="$*"

if [ -z "$PROMPT" ]; then
    echo "Usage: $0 \"your prompt here\""
    exit 1
fi

echo "🔄 Sending to OpenRouter..."
echo ""

curl -s -X POST \
    "https://openrouter.ai/api/v1/chat/completions" \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
        \"model\": \"meta-llama/llama-3.1-8b-instruct:free\",
        \"messages\": [
            {\"role\": \"user\", \"content\": \"$PROMPT\"}
        ]
    }" | jq -r '.choices[0].message.content'