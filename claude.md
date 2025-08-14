# ⚠️ CRITICAL: NO ANTHROPIC API KEY AVAILABLE ⚠️

**IMPORTANT**: We do NOT have an Anthropic API key, so we need to use FREE alternatives via OpenRouter for Claude Code integration.

# 🎉 WORKING SOLUTION: Y-Router + OpenRouter

**Status: V1 COMPLETE - FULL MCP INTEGRATION** ✅

Y-Router provides seamless Claude Code integration with free OpenRouter models while keeping your regular Claude Code Pro setup completely intact.

## Quick Start

```bash
./setup-y-router.sh  # Automatically uses your .env API key
source ~/.bashrc
claude-cheap "What is 2+2?"  # Test it!
```

## V1 Status: COMPLETE! ✅

**FULLY WORKING INTEGRATION:**
- ✅ Y-router + 10 OpenRouter models with tool calling
- ✅ All 22 MCP servers working with y-router  
- ✅ Seamless model switching within sessions (`/model`)
- ✅ Cost-effective workflow (start cheap, scale up as needed)
- ✅ OpenRouter requests branded as "Ralex"

**Confirmed Working:**
- ✅ `claude-cheap` (GPT-5 Nano) + filesystem MCP ✅
- ✅ All model functions load and execute correctly
- ✅ MCP tool access working (filesystem, memory, sequential-thinking, etc.)
- ✅ Manual model switching: `/model kimi-k2`, `/model qwen3-coder`

**Ready to Use - 10 Models Available:**
```bash
source ~/.bashrc

# Entry points - start with any model:
claude-cheap "question"     # GPT-5 Nano (fast)
claude-flash "question"     # Gemini 2.5 Flash (coding)
claude-kimi "question"      # Kimi K2 (agentic, reasoning)
claude-gemini2 "question"   # Gemini 2.0 Flash 001
claude-qwen3 "question"     # Qwen3 Coder (specialist)
claude-qwen30b "question"   # Qwen3 30B (powerful)
claude-oss "question"       # GPT OSS 120B (huge)
claude-glm "question"       # GLM 4.5 (Chinese)
claude-gpt4 "question"      # GPT-4o Mini (reliable)
claude-sonnet "question"    # Claude 3.5 Sonnet (premium)

# Switch models mid-conversation:
/model moonshotai/kimi-k2
/model qwen/qwen3-coder
/model google/gemini-2.5-flash
```

See [CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md) for complete documentation.

---

# 🚀 Future Ideas (V2 and Beyond)

## V2: Automated Model Routing
- **Smart Task Detection**: Automatically route based on prompt complexity
  - Simple questions → nano (cost-effective)
  - Complex reasoning → kimi-k2 (reasoning expert) 
  - Code tasks → qwen3-coder (specialist)
  - Heavy analysis → qwen30b (powerful)
- **Cost Monitoring**: Track usage and suggest model optimizations
- **Context Handoffs**: Seamless context transfer between models

## V3: Advanced Agentic Workflows
- **Agent-OS Integration**: Multi-step autonomous execution
- **Enhanced Zen MCP**: Workflow orchestration via Zen server
- **Task Templates**: Pre-built patterns for common workflows
- **Multi-Agent Coordination**: Different models for different subtasks

## V4: Enterprise Features  
- **Team Sharing**: Shared MCP configurations
- **Usage Analytics**: Cost optimization across projects
- **Custom Model Training**: Fine-tune models for specific tasks
- **Advanced Security**: Role-based access, audit logging

## Quick Experiments to Try
- Test **mcp-orchestrator** for automated multi-agent workflows
- Explore **k83-framework** for Agent-OS integration
- Use **sequential-thinking** MCP for complex problem breakdown
- Try **memory-bank** MCP for persistent context across sessions

---

# Archive: `claude-code-router` - FAILED ❌

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