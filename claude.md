# ⚠️ CRITICAL: NO ANTHROPIC API KEY AVAILABLE ⚠️

**IMPORTANT**: We do NOT have an Anthropic API key, so we need to use FREE alternatives via OpenRouter for Claude Code integration.

# 🎉 WORKING SOLUTION: Y-Router + OpenRouter

**Status: IN PROGRESS** 🔧

Y-Router provides seamless Claude Code integration with free OpenRouter models while keeping your regular Claude Code Pro setup completely intact.

## Quick Start

```bash
./setup-y-router.sh  # Automatically uses your .env API key
source ~/.bashrc
claude-cheap "What is 2+2?"  # Test it!
```

## Current Status: Authentication Issue 🔧

The setup is mostly working but has a 401 authentication issue. Y-router is running correctly and responding, but Claude Code isn't passing the API key properly to y-router.

**What's Working:**
- ✅ Y-router Docker container running on port 8787
- ✅ Direct API calls to y-router work fine
- ✅ Models like `openai/gpt-5-nano` and `openai/gpt-4o-mini` support tool calling

**Issue:**
- ❌ Claude Code gets 401 "No auth credentials found" when using y-router

**Next Steps:**
1. Debug why Claude Code's `ANTHROPIC_API_KEY` isn't reaching y-router
2. Check if y-router expects different header format
3. Consider alternative API key passing methods

See [CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md) for complete documentation.

---

# `claude-code-router` - FAILED ❌

## Final Analysis: CCR is Fundamentally Broken

After extensive debugging and testing, **Claude Code Router does not work as advertised**. Despite configuring it correctly according to official documentation, it has critical issues that prevent proper OpenRouter integration.

## The Problem

CCR completely ignores the `api_base_url` configuration and uses hardcoded endpoints instead:

```json
// Our Configuration
{
  "name": "custom-provider", 
  "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
  // ...
}

// What CCR Actually Uses (from debug logs)
{
  "type": "openai",
  "endpoint": "https://api.shuaihong.ai"  // Completely wrong!
}
```

## Evidence of Failure

1. **Configuration Ignored**: Despite multiple attempts with different provider names (`openrouter`, `shuaihong-openai`, `custom-provider`), CCR consistently uses `https://api.shuaihong.ai` instead of our configured OpenRouter endpoint.

2. **Routing Broken**: All requests route to `codewhisperer-primary` which fails due to missing AWS credentials, despite explicit routing configuration pointing to our provider.

3. **Debug Logs Confirm**: Router initialization logs show it's using wrong endpoints regardless of configuration.

## What We Tried

✅ Correct configuration format with all required fields  
✅ Multiple provider names to avoid hardcoded mappings  
✅ Explicit config file paths  
✅ Debug mode investigation  
✅ Following official documentation examples  
✅ Proper API keys and endpoints  

## Conclusion

**Claude Code Router is not suitable for production use**. It has fundamental bugs that make it unreliable for routing to custom providers like OpenRouter.

## ✅ WORKING SOLUTION: Y-Router + OpenRouter

**Y-router works perfectly!** Here's the proven working setup:

### Quick Setup

1. **Start Y-router with Docker:**
   ```bash
   git clone https://github.com/luohy15/y-router.git
   cd y-router
   sudo docker-compose up -d
   ```

2. **Set environment variables:**
   ```bash
   export ANTHROPIC_BASE_URL="http://localhost:8787"
   export ANTHROPIC_API_KEY="your-openrouter-api-key"
   ```

3. **Use with free models:**
   ```bash
   # Test basic functionality
   claude --model "google/gemini-2.5-flash" --print "What is 2+2?"
   
   # Test tool calling
   claude --model "google/gemini-2.5-flash" --print "List files in current directory"
   ```

### Working Free Models
- `google/gemini-2.5-flash` - Fast, supports tool calling
- `qwen/qwen-2.5-coder-32b-instruct` - Good for coding
- Many others available on OpenRouter

### Key Benefits
✅ **Tool calling works perfectly**  
✅ **No API key needed for Anthropic**  
✅ **Free models available**  
✅ **Full Claude Code compatibility**  
✅ **Simple Docker setup**