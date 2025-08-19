#!/bin/bash

# Load API key from .env file
if [ -f "$(dirname "${BASH_SOURCE[0]}")/.env" ]; then
    source "$(dirname "${BASH_SOURCE[0]}")/.env"
elif [ -f "$HOME/dev/ralex/.env" ]; then
    source "$HOME/dev/ralex/.env"
fi

# Y-Router Claude Code Functions - Using models that support tool calling
claude-cheap() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_API_KEY="$OPENROUTER_API_KEY"
    claude --model "openai/gpt-5-nano" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY
}

claude-gpt4() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_API_KEY="$OPENROUTER_API_KEY"
    claude --model "openai/gpt-4o-mini" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY
}

claude-flash() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_API_KEY="$OPENROUTER_API_KEY"
    claude --model "google/gemini-2.5-flash" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY
}

claude-sonnet() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_API_KEY="$OPENROUTER_API_KEY"
    claude --model "anthropic/claude-3.5-sonnet" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY
}

claude-gemini2() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_API_KEY="$OPENROUTER_API_KEY"
    claude --model "google/gemini-2.0-flash-001" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY
}

claude-qwen3() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_API_KEY="$OPENROUTER_API_KEY"
    claude --model "qwen/qwen3-coder" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY
}

claude-kimi() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_API_KEY="$OPENROUTER_API_KEY"
    claude --model "moonshotai/kimi-k2" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY
}

claude-qwen30b() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_API_KEY="$OPENROUTER_API_KEY"
    claude --model "qwen/qwen3-30b-a3b" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY
}

claude-oss() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_API_KEY="$OPENROUTER_API_KEY"
    claude --model "openai/gpt-oss-120b" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY
}

claude-glm() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_API_KEY="$OPENROUTER_API_KEY"
    claude --model "z-ai/glm-4.5" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY
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
    export ANTHROPIC_API_KEY="$OPENROUTER_API_KEY"
    claude --model "$model" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY
}

ralex() {
    # Call the Python smart router CLI
    python3 /home/ubuntu/dev/ralex/src/smart_router/ralex_cli.py "$@"
}