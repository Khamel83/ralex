#!/bin/bash
# Ralex V2: Yolo Launcher (15 lines)

# Ensure OpenRouter API key is set
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ Please set OPENROUTER_API_KEY"
    exit 1
fi

echo "🚀 Starting Ralex V2: OpenCode + LiteLLM + OpenRouter"

# Start LiteLLM proxy in background
litellm --config litellm_config.yaml --port 4000 --num_workers 1 &
PROXY_PID=$!

# Wait for proxy to start
sleep 3

# Launch OpenCode.ai in yolo mode 
export PATH=/home/RPI3/.opencode/bin:$PATH
echo "💰 Cost-optimized routing: cheap→smart fallback"
echo "🧠 AgentOS workflows available"
echo "⚡ Yolo mode: Fast execution, minimal prompts"
echo ""

# Start OpenCode with the proxy
opencode --mode auto || {
    echo "❌ OpenCode failed to start"
    kill $PROXY_PID
    exit 1
}

# Cleanup on exit
trap "kill $PROXY_PID" EXIT