#!/bin/bash

# Load API key from .env file
if [ -f "$(dirname "${BASH_SOURCE[0]}")/.env" ]; then
    source "$(dirname "${BASH_SOURCE[0]}")/.env"
fi

# Y-Router Claude Code Functions - Using models that support tool calling
claude-cheap() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_CUSTOM_HEADERS="x-api-key: $OPENROUTER_API_KEY,HTTP-Referer: https://ralex.ai,X-Title: Ralex"
    claude --model "openai/gpt-5-nano" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_CUSTOM_HEADERS
}

claude-gpt4() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_CUSTOM_HEADERS="x-api-key: $OPENROUTER_API_KEY,HTTP-Referer: https://ralex.ai,X-Title: Ralex"
    claude --model "openai/gpt-4o-mini" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_CUSTOM_HEADERS
}

claude-flash() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_CUSTOM_HEADERS="x-api-key: $OPENROUTER_API_KEY,HTTP-Referer: https://ralex.ai,X-Title: Ralex"
    claude --model "google/gemini-2.5-flash" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_CUSTOM_HEADERS
}

claude-sonnet() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_CUSTOM_HEADERS="x-api-key: $OPENROUTER_API_KEY,HTTP-Referer: https://ralex.ai,X-Title: Ralex"
    claude --model "anthropic/claude-3.5-sonnet" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_CUSTOM_HEADERS
}

claude-gemini2() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_CUSTOM_HEADERS="x-api-key: $OPENROUTER_API_KEY,HTTP-Referer: https://ralex.ai,X-Title: Ralex"
    claude --model "google/gemini-2.0-flash-001" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_CUSTOM_HEADERS
}

claude-qwen3() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_CUSTOM_HEADERS="x-api-key: $OPENROUTER_API_KEY,HTTP-Referer: https://ralex.ai,X-Title: Ralex"
    claude --model "qwen/qwen3-coder" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_CUSTOM_HEADERS
}

claude-kimi() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_CUSTOM_HEADERS="x-api-key: $OPENROUTER_API_KEY,HTTP-Referer: https://ralex.ai,X-Title: Ralex"
    claude --model "moonshotai/kimi-k2" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_CUSTOM_HEADERS
}

claude-qwen30b() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_CUSTOM_HEADERS="x-api-key: $OPENROUTER_API_KEY,HTTP-Referer: https://ralex.ai,X-Title: Ralex"
    claude --model "qwen/qwen3-30b-a3b" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_CUSTOM_HEADERS
}

claude-oss() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_CUSTOM_HEADERS="x-api-key: $OPENROUTER_API_KEY,HTTP-Referer: https://ralex.ai,X-Title: Ralex"
    claude --model "openai/gpt-oss-120b" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_CUSTOM_HEADERS
}

claude-glm() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_CUSTOM_HEADERS="x-api-key: $OPENROUTER_API_KEY,HTTP-Referer: https://ralex.ai,X-Title: Ralex"
    claude --model "z-ai/glm-4.5" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_CUSTOM_HEADERS
}

claude-model() {
    if [ -z "$1" ]; then
        echo "Usage: claude-model <model-name> [prompt...]"
        echo "Examples:"
        echo "  claude-model 'openai/gpt-3.5-turbo' 'What is 2+2?'"
        echo "  claude-model 'openai/gpt-4o-mini' 'Write a function'"
        return 1
    fi
    local model="$1"
    shift
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_CUSTOM_HEADERS="x-api-key: $OPENROUTER_API_KEY,HTTP-Referer: https://ralex.ai,X-Title: Ralex"
    claude --model "$model" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_CUSTOM_HEADERS
}