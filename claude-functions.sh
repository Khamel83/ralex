#!/bin/bash

# Y-Router Claude Code Functions - Using models that support tool calling
claude-cheap() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_API_KEY="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"
    claude --model "openai/gpt-5-nano" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY
}

claude-gpt4() {
    export ANTHROPIC_BASE_URL="http://localhost:8787"
    export ANTHROPIC_API_KEY="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"
    claude --model "openai/gpt-4o-mini" "$@"
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
    export ANTHROPIC_API_KEY="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"
    claude --model "$model" "$@"
    unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY
}