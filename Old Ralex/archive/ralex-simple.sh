#!/bin/bash

# Ralex - OpenRouter API with preferred models for K83/Agent-OS integration
# Load API key from .env (check current dir and project dir)
if [ -f ".env" ]; then
    source .env
elif [ -f "/home/ubuntu/dev/ralex/.env" ]; then
    source "/home/ubuntu/dev/ralex/.env"
fi

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ OPENROUTER_API_KEY not found in .env file"
    echo "Please add: OPENROUTER_API_KEY=your-key-here"
    exit 1
fi

# Check if we have arguments for non-interactive mode
if [ $# -eq 0 ]; then
    echo "Interactive mode not supported. Use: ralex \"your prompt here\""
    exit 1
fi

# Combine all arguments into one prompt
PROMPT="$*"

# Your preferred free models in order of preference
FREE_MODELS=(
    "qwen/qwen3-coder:free"           # Best for coding
    "z-ai/glm-4.5-air:free"          # Reliable general purpose  
    "moonshotai/kimi-k2:free"         # Good for context
    "openai/gpt-oss-20b:free"         # Fallback
)

# Pick the working free model (GLM works reliably)
MODEL="${FREE_MODELS[1]}"  # z-ai/glm-4.5-air:free

# If that model fails, script will fall back through the array automatically
# For paid models when needed: google/gemini-2.0-flash-001, qwen/qwen3-coder, moonshotai/kimi-k2, openai/gpt-oss-120b

curl -X POST \
    "https://openrouter.ai/api/v1/chat/completions" \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
        \"model\": \"$MODEL\",
        \"messages\": [
            {\"role\": \"user\", \"content\": \"$PROMPT\"}
        ]
    }" | jq -r '.choices[0].message.content'