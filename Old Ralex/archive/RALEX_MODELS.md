# Ralex Model Configuration

## Paid Models (Cheap but High Quality)
- `google/gemini-2.0-flash-001` - Google's latest fast model
- `qwen/qwen3-coder` - Excellent for coding tasks
- `moonshotai/kimi-k2` - Great for high input token tasks
- `openai/gpt-oss-120b` - Large open source model via OpenAI

## Free Models
- `deepseek/deepseek-chat-v3-0324:free` - General purpose
- `deepseek/deepseek-r1-0528:free` - Reasoning tasks
- `qwen/qwen3-coder:free` - Free coding model
- `moonshotai/kimi-k2:free` - Free high-context model

## Usage Pattern
- Ralex should use Claude Code Router to route to OpenRouter
- Should coordinate with Agent-OS for complex multi-step tasks
- Should use MCP servers for agentic development workflows
- Should automatically select appropriate models based on task type

## Current Status
- Claude Code Router not yet configured
- Direct OpenRouter API calls working as fallback
- Need to set up proper CCR integration with these specific models