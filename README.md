# RalexOS

# ⚠️ CRITICAL: NO ANTHROPIC API KEY AVAILABLE ⚠️

**IMPORTANT**: We do NOT have an Anthropic API key, so all Claude Code integration must use FREE alternatives via OpenRouter.

**V1 COMPLETE**: Y-Router + OpenRouter integration with 10 models and 22 MCP servers.

## What is this?

RalexOS is a minimal, self-contained bash script that sets up a complete AI-powered development environment with OpenCode and MCP servers. With just one script, you can get everything you need running on any platform (Linux, macOS, Raspberry Pi, VPS, etc.).

## V1 Features ✅

**10-Model OpenRouter Integration:**
- GPT-5 Nano (fast/cheap), Kimi K2 (reasoning), Qwen3 Coder (specialist)
- Gemini 2.5/2.0 Flash, GPT-4o Mini, Claude 3.5 Sonnet, and more
- Seamless model switching: `/model kimi-k2`, `/model qwen3-coder`

**22 MCP Servers Working:**
- filesystem, memory-bank, sequential-thinking, github-integration
- playwright-testing, sentry-monitoring, k83-framework, mcp-orchestrator
- And 14 more specialized servers for complete development ecosystem

**Cost-Effective Workflow:**
- Start with `claude-cheap` (GPT-5 Nano) for basic tasks
- Scale up to specialized models as needed
- Manual control = perfect cost optimization

**Production Ready:**
- Y-router Docker integration
- Secure API key management (.env)
- OpenRouter requests branded as "Ralex"

## Quick Start (V1)

1. **Setup Y-Router + OpenRouter:**
   ```bash
   # Add your OpenRouter API key to .env
   echo "OPENROUTER_API_KEY=your-key-here" > .env
   
   # Run setup script
   ./setup-y-router.sh
   ```

2. **Start using 10 models:**
   ```bash
   source ~/.bashrc
   
   # Entry points:
   claude-cheap "question"     # GPT-5 Nano (fast/cheap)
   claude-kimi "complex task"  # Kimi K2 (reasoning expert)
   claude-qwen3 "code task"    # Qwen3 Coder (specialist)
   
   # Switch models mid-conversation:
   /model moonshotai/kimi-k2
   /model qwen/qwen3-coder
   ```

3. **Access 22 MCP servers:**
   - All MCP tools work with any model
   - Filesystem, GitHub, Playwright, Memory, and more
   - Full development ecosystem ready

4. Restart your shell or source your profile:
   ```bash
   source ~/.bashrc
   # or
   source ~/.zshrc
   ```

5. Start using OpenCode:
   ```bash
   opencode
   ```

## Usage

After installation, you have these commands:

- `opencode` - Start OpenCode TUI
- `ocp` - Force Claude Pro model
- `ocq` - Use Qwen3 Coder (free)
- `ocg` - Use Gemini Flash
- `ock` - Use Kimi K2 (free)
- `oy "command"` - Run one-shot command

In the OpenCode TUI, you can use:

- `@yolo <task>` - Run in YOLO mode (no confirmations)
- `/mcp` - Manage MCP servers
- `/models` - Switch between models

## Supported Platforms

- macOS (Intel and Apple Silicon)
- Ubuntu/Debian
- Other Linux distributions (manual dependency installation may be required)
- Raspberry Pi
- VPS servers

## Customization

You can easily modify the script to:

1. Add or remove MCP servers
2. Change the default models
3. Add more aliases
4. Modify the configuration

Just edit the `ralexos-complete.sh` file and re-run it.

## What's Included

### Models
- Claude Pro (via OAuth)
- Qwen3 Coder (free via OpenRouter)
- Gemini Flash (via OpenRouter)
- Kimi K2 (free via OpenRouter)

### MCP Servers
1. **Context7** - Advanced context management
2. **GitHub** - Direct GitHub repository access
3. **Puppeteer** - Web browsing and scraping
4. **Sequential** - Multi-step reasoning tasks
5. **Zen** - General purpose tools and utilities
6. **MemoryBank** - Persistent memory storage

## Troubleshooting

If you encounter any issues:

1. Check that all dependencies are installed:
   ```bash
   node --version
   npm --version
   bun --version
   ```

2. Verify MCP servers are installed:
   ```bash
   which context7-mcp
   which github-mcp-server
   # etc.
   ```

3. Check the configuration file:
   ```bash
   cat ~/.config/opencode/opencode.json
   ```

## Updating

To update, simply download the latest version of the script and run it again:

```bash
curl -O https://raw.githubusercontent.com/yourusername/ralexos/main/ralexos-complete.sh
chmod +x ralexos-complete.sh
./ralexos-complete.sh
```

The script is designed to be idempotent - running it multiple times is safe and will update your installation.