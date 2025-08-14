# Ralex - Actually Working Setup

## What This Does
- Uses regular `claude` command when it works
- Automatically falls back to free OpenRouter models when Claude hits usage limits
- Simple, reliable, actually works

## Quick Setup

1. **Get OpenRouter API Key** (required for fallback):
   - Visit [OpenRouter.ai](https://openrouter.ai)
   - Sign up and get your free API key
   - Add it to `.env` file:
   ```bash
   echo "OPENROUTER_API_KEY=your-key-here" > .env
   ```

2. **The setup is already done!** Just use:
   ```bash
   ralex "your prompt here"
   ```

## How It Works

- First tries `claude` command normally
- If Claude says "usage limit reached", automatically switches to OpenRouter's free models
- Uses Llama 3.1 8B (free) as the fallback model

## Usage

```bash
# Interactive mode - use claude directly
claude

# When you hit limits, use ralex for non-interactive prompts
ralex "help me debug this code"
ralex "write a Python function to sort a list"
```

## Files

- `ralex-simple.sh` - The actual working script (40 lines, easy to understand)
- `.env` - Your OpenRouter API key
- `~/bin/ralex` - Symlink so you can use `ralex` command anywhere

## Testing

To test the fallback manually:
```bash
# This will show fallback behavior
ralex "hello world"
```

## Troubleshooting

**Command not found**: Restart your terminal to pick up the new PATH

**API key error**: Make sure `.env` file has your OpenRouter key:
```bash
cat .env  # Should show OPENROUTER_API_KEY=sk-or-v1-...
```

**No fallback**: The script only switches to OpenRouter when Claude specifically says "usage limit reached"

---

This is a 40-line working solution instead of the complex router system that doesn't actually work as advertised.