# Ralex - Ultimate Claude Code Setup

**Always Free, Always Working Claude Code Environment**

Ralex automatically sets up an intelligent routing system that seamlessly transitions from Claude Pro to free models when your tokens are exhausted, ensuring uninterrupted AI assistance.

## Features

- 🔄 **Auto Router**: Intelligent routing between Claude Pro and free models
- 💰 **Cost Management**: Automatic fallback to free models when quota exceeded
- 🚀 **Yolo Mode**: Auto-approves everything for streamlined workflow
- 🔧 **Model Agnostic**: Works with GPT-4, Claude-3, Llama-3, Gemini, and other capable models
- 📊 **Token Management**: Monitors usage and switches models intelligently

## Quick Setup

1. **Clone this repository:**
   ```bash
   git clone https://github.com/Khamel83/ralex.git
   cd ralex
   ```

2. **Run the setup script:**
   ```bash
   ./setup-ultimate-claude.sh
   ```
   The script will automatically:
   - Load your OpenRouter API key from `.env` file (if present)
   - Prompt for manual input if no `.env` file exists
   - Install all required components
   - Configure intelligent routing

3. **Start using Claude:**
   ```bash
   claude
   ```

## What the Setup Does

The `setup-ultimate-claude.sh` script:

1. **Installs Claude Code** globally via npm
2. **Installs Claude Code Router** for intelligent request routing
3. **Clones Agent-OS** with ultimate enhancements from the `agent-os-ultimate` branch
4. **Links Khamel83 enhancements** including:
   - Claude Pro tracker with automatic fallback
   - Free model ranker for optimal free model selection
   - Integration configurations
5. **Configures workflows** for token management and model fallback
6. **Sets up OpenRouter integration** (optional API key for free models)

## Configuration

### OpenRouter API Key (Optional but Recommended)

For the best free model experience, get an OpenRouter API key:

1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Create an account and get your API key
3. **Option A - Use .env file (Recommended):**
   ```bash
   # Create or edit .env file in the ralex directory
   echo "OPENROUTER_API_KEY=your-api-key-here" > .env
   ```
4. **Option B - Manual entry:**
   The setup script will prompt you to enter the key during installation
5. **Option C - Environment variable:**
   ```bash
   export OPENROUTER_API_KEY="your-api-key-here"
   ```

### Environment Variables

The system uses these environment variables:
- `OPENROUTER_API_KEY`: Your OpenRouter API key for free model access
- Additional configuration is stored in `~/.claude-code-router/config.json`

## How It Works

1. **Primary Mode**: Uses your Claude Pro tokens normally
2. **Monitoring**: Tracks token usage in real-time
3. **Auto-Fallback**: When Claude Pro tokens are exhausted, automatically switches to free models via OpenRouter
4. **Model Selection**: Intelligent ranking system selects the best available free model
5. **Seamless Experience**: You continue using the `claude` command without interruption

## Project Structure

```
ralex/
├── setup-ultimate-claude.sh    # Main setup script
├── README.md                   # This file
└── .env                        # Your OpenRouter API key (created by you)
```

After setup, the following directories are created:
- `~/.agent-os/`: Agent-OS with ultimate enhancements
- `~/.claude-code-router/`: Router configuration and Khamel83 enhancements

## Troubleshooting

### "Free models may not work as expected"
- This means no OpenRouter API key was provided during setup
- **Solution**: Create a `.env` file with your OpenRouter API key:
  ```bash
  echo "OPENROUTER_API_KEY=your-api-key-here" > .env
  ```
- Then run the setup script again

### Setup fails during git operations
- Ensure you have git installed and configured
- Check internet connectivity
- The script will automatically handle existing directories and re-clone if needed

### Claude command not found
- Run `npm install -g @anthropic/claude-code` manually
- Ensure your npm global bin directory is in your PATH
- On macOS, you may need to restart your terminal

### Script says "No OpenRouter API Key provided" even with .env file
- Make sure the `.env` file is in the same directory as the setup script
- Check that the `.env` file contains: `OPENROUTER_API_KEY=your-actual-key`
- Ensure there are no extra spaces or quotes around the key

### Permission denied when running setup script
- Make the script executable: `chmod +x setup-ultimate-claude.sh`
- Or run with bash: `bash setup-ultimate-claude.sh`

## Development

To develop on a different machine:

1. Clone this repository
2. Run the setup script
3. Check your `.env` file for any local configurations
4. The system will automatically sync with the latest enhancements from the `agent-os-ultimate` branch

## Contributing

This project integrates several components:
- [Claude Code](https://github.com/anthropics/claude-code) - Official Claude CLI
- [Agent-OS](https://github.com/Khamel83/agent-os) - Enhanced workflow system
- [Claude Code Router](https://www.npmjs.com/package/@musistudio/claude-code-router) - Intelligent routing

## License

This setup script and configuration is provided as-is. Individual components maintain their respective licenses.