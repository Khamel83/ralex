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

### 10 Models via Y-Router + OpenRouter
```bash
# Start with any model:
claude-cheap "question"     # GPT-5 Nano (fast, efficient)
claude-flash "question"     # Gemini 2.5 Flash (great for coding)
claude-kimi "question"      # Kimi K2 (1T params, agentic specialist)
claude-gemini2 "question"   # Gemini 2.0 Flash 001 (newest)
claude-qwen3 "question"     # Qwen3 Coder (coding specialist)
claude-qwen30b "question"   # Qwen3 30B (powerful reasoning)
claude-oss "question"       # GPT OSS 120B (huge context)
claude-glm "question"       # GLM 4.5 (Chinese language model)
claude-gpt4 "question"      # GPT-4o Mini (reliable, tested)
claude-sonnet "question"    # Claude 3.5 Sonnet (premium)

# Switch models mid-conversation:
/model moonshotai/kimi-k2
/model qwen/qwen3-coder
/model google/gemini-2.5-flash
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

## Available Models (All Support Tool Calling)

**Coding Specialists:**
- `qwen/qwen3-coder` - Qwen3 Coder specialist
- `google/gemini-2.5-flash` - Excellent for coding tasks

**Reasoning & Agentic:**
- `moonshotai/kimi-k2` - 1T params MoE, agentic specialist, 128K context
- `qwen/qwen3-30b-a3b` - Powerful 30B reasoning model

**General Purpose:**
- `openai/gpt-5-nano` - Fast and efficient
- `openai/gpt-4o-mini` - Reliable, well-tested
- `google/gemini-2.0-flash-001` - Newest Gemini
- `openai/gpt-oss-120b` - Huge 120B parameter model
- `z-ai/glm-4.5` - Chinese language model
- `anthropic/claude-3.5-sonnet` - Premium quality

Explore more models on [OpenRouter](https://openrouter.ai/models)

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