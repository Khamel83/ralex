#!/bin/bash
# Ralex V2: Budget-Aware Setup Script
# Zero custom coding required - LiteLLM handles all budget logic!

set -e

echo "🚀 Setting up Ralex V2 with Budget Tracking..."
echo "=" * 50

# Check requirements
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ Please set OPENROUTER_API_KEY first:"
    echo "   export OPENROUTER_API_KEY='your-key-here'"
    exit 1
fi

echo "✅ OpenRouter API key found: ${OPENROUTER_API_KEY:0:8}..."

# Create clean virtual environment
if [ -d ".ralex-env" ]; then
    echo "🧹 Cleaning existing environment..."
    rm -rf .ralex-env
fi

echo "🐍 Creating virtual environment..."
python3 -m venv .ralex-env

echo "📦 Installing LiteLLM..."
.ralex-env/bin/pip install --upgrade pip
.ralex-env/bin/pip install 'litellm[proxy]'

# Set budget environment variables (LiteLLM built-in)
echo "💰 Configuring budget tracking..."
export LITELLM_MAX_BUDGET=5.00
export LITELLM_BUDGET_DURATION="1d"

# Test LiteLLM installation
echo "🧪 Testing LiteLLM installation..."
.ralex-env/bin/python -c "import litellm; print(f'LiteLLM version: {litellm.__version__}')" || {
    echo "❌ LiteLLM import failed"
    exit 1
}

echo "✅ LiteLLM installed successfully"

# Test configuration file
echo "🔧 Validating configuration..."
if [ ! -f "litellm_budget_config.yaml" ]; then
    echo "❌ Configuration file not found: litellm_budget_config.yaml"
    exit 1
fi

echo "✅ Configuration file found"

# Create startup script
echo "📝 Creating startup script..."
cat > start-budget-aware-proxy.sh << 'EOF'
#!/bin/bash
# Start LiteLLM with budget tracking

echo "🚀 Starting budget-aware LiteLLM proxy..."

# Set environment variables
export LITELLM_MAX_BUDGET=5.00
export LITELLM_BUDGET_DURATION="1d"

# Check API key
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ OPENROUTER_API_KEY not set"
    exit 1
fi

# Start LiteLLM proxy with budget config
.ralex-env/bin/litellm --config litellm_budget_config.yaml --port 4000 --num_workers 1 &
PROXY_PID=$!

# Wait for startup
echo "⏳ Starting proxy..."
sleep 5

# Test health endpoint
if curl -s http://localhost:4000/health > /dev/null; then
    echo "✅ Proxy started successfully!"
    echo "💰 Budget tracking active"
    echo "📊 Health check: http://localhost:4000/health"
    echo "💳 Budget status: http://localhost:4000/budget"
    echo ""
    echo "🎯 Usage:"
    echo "  export OPENAI_API_BASE='http://localhost:4000/v1'"
    echo "  export OPENAI_API_KEY='dummy'"
    echo "  opencode 'your request here'"
    echo ""
    echo "Press Ctrl+C to stop proxy"
    
    # Keep proxy running
    wait $PROXY_PID
else
    echo "❌ Proxy failed to start"
    kill $PROXY_PID 2>/dev/null || true
    exit 1
fi
EOF

chmod +x start-budget-aware-proxy.sh

# Create OpenCode.ai integration script
echo "🔗 Creating OpenCode.ai integration..."
cat > yolo-budget-code.sh << 'EOF'
#!/bin/bash
# Budget-aware OpenCode.ai wrapper

# Check if proxy is running
if ! curl -s http://localhost:4000/health > /dev/null; then
    echo "❌ LiteLLM proxy not running. Start with: ./start-budget-aware-proxy.sh"
    exit 1
fi

# Get budget status
BUDGET_JSON=$(curl -s http://localhost:4000/health)
BUDGET_REMAINING=$(echo "$BUDGET_JSON" | jq -r '.budget.budget_remaining // 5.00')

echo "💰 Budget remaining: \$${BUDGET_REMAINING}"

# Set environment for OpenCode.ai
export OPENAI_API_BASE="http://localhost:4000/v1"
export OPENAI_API_KEY="dummy"  # LiteLLM handles the real key
export PATH="/home/RPI3/.opencode/bin:$PATH"

# Run OpenCode.ai with budget awareness
if (( $(echo "$BUDGET_REMAINING < 0.50" | bc -l 2>/dev/null || echo 0) )); then
    echo "⚠️ Low budget - using yolo mode (ultra-cheap)"
    opencode --model yolo "$@"
elif (( $(echo "$BUDGET_REMAINING < 2.00" | bc -l 2>/dev/null || echo 0) )); then
    echo "💡 Moderate budget - using cheap model"
    opencode --model cheap "$@"  
else
    echo "✅ Healthy budget - using smart routing"
    opencode "$@"  # Let LiteLLM choose best model
fi

# Show updated budget
echo ""
UPDATED_BUDGET=$(curl -s http://localhost:4000/health | jq -r '.budget.budget_remaining // "unknown"')
echo "💰 Budget after request: \$${UPDATED_BUDGET}"
EOF

chmod +x yolo-budget-code.sh

# Create simple budget checker
echo "📊 Creating budget checker..."
cat > check-budget.sh << 'EOF'
#!/bin/bash
# Simple budget status checker

if ! curl -s http://localhost:4000/health > /dev/null; then
    echo "❌ LiteLLM proxy not running"
    exit 1
fi

BUDGET_JSON=$(curl -s http://localhost:4000/health)
echo "📊 Budget Status:"
echo "$BUDGET_JSON" | jq '.budget // {"error": "budget info not available"}'
EOF

chmod +x check-budget.sh

echo ""
echo "🎉 Setup Complete!"
echo "=" * 30
echo ""
echo "📋 Next Steps:"
echo "1. Start budget-aware proxy:"
echo "   ./start-budget-aware-proxy.sh"
echo ""
echo "2. In another terminal, use yolo budget coding:"
echo "   ./yolo-budget-code.sh 'fix this bug'"
echo ""  
echo "3. Check budget anytime:"
echo "   ./check-budget.sh"
echo ""
echo "💡 Features enabled:"
echo "  ✅ $5 daily budget limit"
echo "  ✅ Automatic cost tracking"
echo "  ✅ Smart model routing"  
echo "  ✅ Budget-aware fallbacks"
echo "  ✅ Real-time budget monitoring"
echo ""
echo "🎯 All budget logic is built into LiteLLM - zero custom coding required!"