# Ralex - Context-Aware Claude Code Fallback

**Simple, reliable fallback system for when Claude Code runs out of credits**

Ralex provides a context-aware fallback to OpenRouter's free models when Claude Code reaches its usage limits, preserving conversation history for seamless transitions.

## What This Actually Does

- 🔄 **Manual Fallback**: When Claude Code fails, switch to `ralex` command
- 💾 **Context Preservation**: Automatically saves Claude conversations for continuity  
- 🆓 **Free Models**: Uses OpenRouter's free models (no cost)
- 📝 **Conversation History**: Maintains context across tool switches
- 🚀 **Simple Setup**: No complex routing or servers required

## Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/Khamel83/ralex.git
cd ralex

# Get your OpenRouter API key from https://openrouter.ai/
echo "OPENROUTER_API_KEY=your-key-here" > .env

# Run the setup script
./setup-ralex.sh
```

### 2. Your Daily Workflow
```bash
# Morning - Use Claude Code normally
claude

# When Claude runs out of credits:
# Exit Claude Code, then use:
ralex --direct "your prompt here"

# ralex automatically knows your conversation history!
```

## How It Works

### Context Preservation System
1. **Claude Code Hooks**: Auto-save every conversation to `.claude-context.md`
2. **Smart ralex**: Reads conversation history before making requests
3. **Seamless Continuity**: Your conversation continues where Claude left off

### Example Workflow
```bash
# Start with Claude Code
claude
# > "Help me build a login form"
# > [Claude helps with the form]
# > "Add validation to it"  
# > [Claude limit reached - exit]

# Switch to ralex
ralex --direct "Now add error handling"
# > ralex reads the entire conversation about the login form
# > continues helping with error handling in context
```

## Installation Details

The setup script:
1. **Checks requirements** (curl, jq, git, npm)
2. **Installs Claude Code** via npm (if not already installed)
3. **Creates ralex command** in `~/bin/ralex` and adds to PATH
4. **Sets up Claude Code hooks** to auto-save conversations
5. **Configures OpenRouter** with your API key
6. **Removes conflicting aliases** for clean installation

## Files Created

```
~/.claude/settings.json          # Claude Code hooks for auto-saving
~/bin/ralex                      # Context-aware fallback script
/path/to/project/.claude-context.md  # Auto-saved conversations
```

## Configuration

### OpenRouter API Key
1. Get free API key from [OpenRouter.ai](https://openrouter.ai/)
2. Add to `.env` file:
   ```bash
   OPENROUTER_API_KEY=your-key-here
   ```

### Supported Free Models
The system automatically uses the best available free model:
- `z-ai/glm-4.5-air:free` (default)
- Other free models as available

## Commands

### ralex Options
```bash
# Try Claude first, fallback to OpenRouter if needed
ralex "your prompt"

# Skip Claude, go directly to OpenRouter  
ralex --direct "your prompt"

# Interactive mode not supported - use one-shot prompts
```

## Cross-Platform Support

**Tested on:**
- ✅ macOS (primary development)
- 🔄 Ubuntu/Raspberry Pi (should work with standard bash/curl/jq)

**Requirements:**
- bash
- curl  
- jq
- git
- npm (for Claude Code)

## Troubleshooting

### "No OPENROUTER_API_KEY found"
- Create `.env` file with your API key
- Or set environment variable: `export OPENROUTER_API_KEY="your-key"`

### "command not found: ralex"  
- Restart terminal (PATH may need refresh)
- Or run: `source ~/.zshrc` (or `~/.bashrc`)
- If still not working, use full path: `/Users/$(whoami)/bin/ralex`

### Context not preserved
- Check if `.claude-context.md` exists in your project directory
- Verify Claude Code hooks are working: check `~/.claude/settings.json`

### ralex returns null/errors
- Test OpenRouter API key: `curl -H "Authorization: Bearer $OPENROUTER_API_KEY" https://openrouter.ai/api/v1/models`
- Check if free models are available

## What's Different From Other Solutions

**Not a router or proxy** - Simple script that switches tools manually  
**Not automatic** - You choose when to switch from Claude to ralex  
**Context-aware** - Conversation history preserved across switches  
**Free models only** - Uses OpenRouter's free tier, no additional costs  

## Development

### Project Structure
```
ralex/
├── README.md              # This file
├── setup-ralex.sh         # Simple, reliable setup script
├── setup-ultimate-claude.sh  # Legacy setup (ignore)
├── ralex-simple.sh        # The actual ralex script
├── .gitignore            # Protects .env and context files
└── .env                  # Your API key (not in git)
```

### Testing
```bash
# Test OpenRouter connection
ralex --direct "what is 2+2"

# Test context preservation  
# 1. Use Claude Code for a conversation
# 2. Exit and run: ralex --direct "continue our conversation"
# 3. Verify it knows the previous context
```

## Contributing

This is a simple, focused solution. PRs welcome for:
- Cross-platform compatibility fixes
- Better error handling  
- Documentation improvements
- Additional free model support

## License

MIT License. Individual components (Claude Code, OpenRouter) maintain their own licenses.