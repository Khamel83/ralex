# ⚠️ CRITICAL: NO ANTHROPIC API KEY AVAILABLE ⚠️

**IMPORTANT**: We do NOT have an Anthropic API key, so all Claude Code integration with free models uses Y-Router + OpenRouter.

# Claude Code + Free Models Setup

This setup gives you **two ways** to use Claude Code:

1. **Regular Claude Code Pro** (your existing subscription) - unchanged
2. **Free models via OpenRouter** (new capability) - using y-router

## Quick Setup

```bash
# 1. Run the setup script (automatically uses your .env API key)
./setup-y-router.sh

# 2. Reload shell
source ~/.bashrc
```

## Usage

### Regular Claude Code (Unchanged)
```bash
claude  # Uses your Pro subscription exactly as before
```

### Free Models via Y-Router
```bash
claude-free "What is 2+2?"              # Free Gemini 2.5 Flash
claude-qwen "Write a Python function"   # Free Qwen Coder
```

## What's Running

- **Y-Router**: Docker container on port 8787 (translates Anthropic → OpenRouter API)
- **Regular Claude**: Your normal Pro subscription (untouched)

## Management

```bash
# Check if y-router is running
curl http://localhost:8787/

# Stop y-router
cd ~/dev/ralex/y-router && sudo docker-compose down

# Start y-router
cd ~/dev/ralex/y-router && sudo docker-compose up -d

# View y-router logs
sudo docker logs y-router-y-router-1
```

## Available Free Models

- `google/gemini-2.5-flash` - Fast, supports tool calling
- `qwen/qwen-2.5-coder-32b-instruct` - Great for coding
- `microsoft/phi-4` - Good general model
- Many more on [OpenRouter](https://openrouter.ai/models)

## Benefits

✅ **Keep your existing Claude Code Pro setup intact**  
✅ **Add free model capability when needed**  
✅ **Full tool calling support on free models**  
✅ **No interference between the two modes**  
✅ **Simple Docker-based setup**  

## Troubleshooting

**Y-router not responding:**
```bash
cd ~/dev/ralex/y-router
sudo docker-compose down
sudo docker-compose up -d
```

**Functions not found:**
```bash
source ~/.bashrc
```

**OpenRouter API errors:**
- Check your API key in .env file
- Verify you have credits on OpenRouter
- Try a different model