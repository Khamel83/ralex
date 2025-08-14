# RalexOS

# ⚠️ CRITICAL: NO ANTHROPIC API KEY AVAILABLE ⚠️

**IMPORTANT**: We do NOT have an Anthropic API key, so all Claude Code integration must use FREE alternatives via OpenRouter.

A complete, single-file setup for OpenCode with MCP (Model Context Protocol) support.

## What is this?

RalexOS is a minimal, self-contained bash script that sets up a complete AI-powered development environment with OpenCode and MCP servers. With just one script, you can get everything you need running on any platform (Linux, macOS, Raspberry Pi, VPS, etc.).

## Features

- Installs OpenCode automatically
- Sets up all popular MCP servers:
  - Context7 MCP (context management)
  - GitHub MCP Server (GitHub integration)
  - Puppeteer MCP Server (web browsing)
  - Sequential Thinking MCP (sequential reasoning)
  - Zen MCP Server (general tools)
  - Memory Bank MCP (memory management)
- Configures all models (Claude Pro, Qwen3, Gemini, Kimi)
- Sets up Git identity and SSH keys
- Creates helpful aliases and environment variables
- Works on macOS, Ubuntu, and other Linux distributions

## Quick Start

1. Download the script:
   ```bash
   curl -O https://raw.githubusercontent.com/yourusername/ralexos/main/ralexos-complete.sh
   ```

2. Edit the configuration values at the top of the script:
   ```bash
   nano ralexos-complete.sh
   ```
   Update these variables:
   - `OPENROUTER_API_KEY` - Your OpenRouter API key
   - `GITHUB_TOKEN` - Your GitHub personal access token
   - `GIT_USER_NAME` - Your Git username
   - `GIT_USER_EMAIL` - Your Git email

3. Make it executable and run it:
   ```bash
   chmod +x ralexos-complete.sh
   ./ralexos-complete.sh
   ```

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