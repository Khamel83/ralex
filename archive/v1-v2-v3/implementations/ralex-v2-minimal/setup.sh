#!/bin/bash
# Ralex V2: Complete Setup Script (30 lines)

echo "🚀 Ralex V2 Setup: The 96% Code Reduction Edition"
echo "================================================="

# Install AgentOS standards
echo "📥 Installing AgentOS standards..."
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/setup.sh | bash

# Install OpenCode.ai
echo "📥 Installing OpenCode.ai..."
curl -fsSL https://opencode.ai/install | bash

# Install LiteLLM in virtual environment
echo "📥 Installing LiteLLM..."
python3 -m venv .venv-ralex-v2
source .venv-ralex-v2/bin/activate
pip install 'litellm[proxy]'

# Make scripts executable
chmod +x yolo-ralex.sh
chmod +x cost-tracker.py

echo ""
echo "✅ Ralex V2 Setup Complete!"
echo ""
echo "📋 Next steps:"
echo "1. Set your API key: export OPENROUTER_API_KEY='your_key'"
echo "2. Launch: ./yolo-ralex.sh"
echo "3. Code with yolo mode: 'fix this bug quickly'"
echo ""
echo "📊 Comparison:"
echo "   V1: 3,737 lines of custom code to maintain" 
echo "   V2: 85 lines of config files"
echo "   Reduction: 96% less code!"