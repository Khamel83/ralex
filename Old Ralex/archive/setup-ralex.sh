#!/bin/bash

echo "🚀 Setting up Ralex - Context-Aware Claude Code Fallback"
echo ""

# Check requirements
echo "📋 Checking requirements..."
for cmd in curl jq git npm; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ $cmd is required but not installed"
        echo "   Please install $cmd and run this script again"
        exit 1
    fi
done
echo "✅ All requirements found"
echo ""

# Check if Claude Code is installed
echo "🔍 Checking Claude Code installation..."
if ! command -v claude &> /dev/null; then
    echo "📦 Installing Claude Code..."
    npm install -g @anthropic-ai/claude-code
    if [ $? -eq 0 ]; then
        echo "✅ Claude Code installed successfully"
    else
        echo "❌ Failed to install Claude Code"
        exit 1
    fi
else
    echo "✅ Claude Code already installed"
fi
echo ""

# Create ~/bin directory if it doesn't exist
echo "📁 Setting up ~/bin directory..."
mkdir -p ~/bin

# Check if ~/bin is in PATH
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo "🔧 Adding ~/bin to PATH..."
    
    # Detect shell and add to appropriate file
    SHELL_NAME=$(basename "$SHELL")
    case "$SHELL_NAME" in
        "zsh")
            SHELL_RC="$HOME/.zshrc"
            ;;
        "bash")
            SHELL_RC="$HOME/.bashrc"
            ;;
        *)
            SHELL_RC="$HOME/.profile"
            ;;
    esac
    
    echo 'export PATH="$HOME/bin:$PATH"' >> "$SHELL_RC"
    export PATH="$HOME/bin:$PATH"
    echo "✅ Added ~/bin to PATH in $SHELL_RC"
else
    echo "✅ ~/bin already in PATH"
fi
echo ""

# Copy ralex script to ~/bin
echo "📝 Installing ralex command..."
if [ -f "./ralex-simple.sh" ]; then
    cp "./ralex-simple.sh" ~/bin/ralex
    chmod +x ~/bin/ralex
    echo "✅ ralex command installed to ~/bin/ralex"
else
    echo "❌ ralex-simple.sh not found in current directory"
    echo "   Make sure you're running this from the ralex project directory"
    exit 1
fi
echo ""

# Set up Claude Code hooks
echo "⚙️  Setting up Claude Code hooks for auto-context saving..."
mkdir -p ~/.claude

# Create or update settings.json
SETTINGS_FILE="$HOME/.claude/settings.json"
if [ -f "$SETTINGS_FILE" ]; then
    echo "📄 Updating existing Claude Code settings..."
    # Use jq to merge the hooks into existing settings
    tmp_file=$(mktemp)
    jq '. + {
        "hooks": {
            "PostToolUse": {
                "command": "cp \"$transcript_path\" .claude-context.md 2>/dev/null || true",
                "description": "Auto-save Claude conversation for ralex fallback"
            },
            "UserPromptSubmit": {
                "command": "cp \"$transcript_path\" .claude-context.md 2>/dev/null || true",
                "description": "Auto-save Claude conversation after user input"
            }
        }
    }' "$SETTINGS_FILE" > "$tmp_file" && mv "$tmp_file" "$SETTINGS_FILE"
else
    echo "📄 Creating new Claude Code settings..."
    cat > "$SETTINGS_FILE" << 'EOF'
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "PostToolUse": {
      "command": "cp \"$transcript_path\" .claude-context.md 2>/dev/null || true",
      "description": "Auto-save Claude conversation for ralex fallback"
    },
    "UserPromptSubmit": {
      "command": "cp \"$transcript_path\" .claude-context.md 2>/dev/null || true",
      "description": "Auto-save Claude conversation after user input"
    }
  }
}
EOF
fi
echo "✅ Claude Code hooks configured"
echo ""

# Check for .env file and OpenRouter API key
echo "🔑 Checking OpenRouter API key..."
if [ -f ".env" ] && grep -q "OPENROUTER_API_KEY" .env; then
    echo "✅ Found OpenRouter API key in .env file"
else
    echo "⚠️  No OpenRouter API key found"
    echo ""
    echo "To enable ralex fallback functionality:"
    echo "1. Get a free API key from https://openrouter.ai/"
    echo "2. Create a .env file with: OPENROUTER_API_KEY=your-key-here"
    echo ""
    read -p "Enter your OpenRouter API key now (or press Enter to skip): " api_key
    if [ ! -z "$api_key" ]; then
        echo "OPENROUTER_API_KEY=$api_key" > .env
        echo "✅ API key saved to .env file"
    else
        echo "⏭️  Skipped API key setup - you can add it later"
    fi
fi
echo ""

# Remove any existing ralex aliases that might conflict
echo "🧹 Cleaning up any conflicting aliases..."
for rc_file in ~/.zshrc ~/.bashrc ~/.profile; do
    if [ -f "$rc_file" ]; then
        sed -i.bak '/alias ralex=/d' "$rc_file" 2>/dev/null || true
    fi
done
echo "✅ Removed any conflicting ralex aliases"
echo ""

echo "🎉 Setup complete!"
echo ""
echo "📖 Quick Start:"
echo "1. Restart your terminal (or run: source ~/.zshrc)"
echo "2. Use Claude Code normally: claude"
echo "3. When Claude runs out of credits:"
echo "   - Exit Claude Code"
echo "   - Use: ralex --direct \"your prompt\""
echo "   - ralex will automatically know your conversation history!"
echo ""
echo "🔧 Test the installation:"
echo "   ralex --direct \"Hello, test message\""
echo ""
echo "📚 Full documentation: https://github.com/Khamel83/ralex"