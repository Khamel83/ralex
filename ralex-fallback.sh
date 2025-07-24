#!/bin/bash
# Emergency fallback for Ralex V2
echo "⚠️  Ralex V2 fallback mode activated"
echo "Using direct OpenRouter implementation..."
exec python3 "$(dirname "$0")/direct-openrouter-test.py" "$@"
