# Ralex Quick Start Guide

**5-minute setup for context-aware Claude Code fallback**

## Step 1: Get Your API Key
1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Get your API key from the dashboard

## Step 2: Install
```bash
git clone https://github.com/Khamel83/ralex.git
cd ralex
echo "OPENROUTER_API_KEY=your-key-here" > .env
./setup-ralex.sh
```

## Step 3: Test
```bash
# Restart terminal, then test:
ralex --direct "Hello world"
```

## Daily Usage

### Normal Day (Claude has credits)
```bash
claude
# Use Claude Code normally for interactive work
```

### When Claude Runs Out
```bash
# Exit Claude Code, then:
ralex --direct "continue helping with my project"
# ralex automatically knows your conversation history!
```

## That's It!

- ✅ Context preserved across switches
- ✅ Free OpenRouter models 
- ✅ No servers or complex setup
- ✅ Works on Mac/Linux

**Full docs:** [README.md](README.md)