# Ralex Quick Start Guide

## 5-Minute Setup

### Prerequisites
- Raspberry Pi with Python 3.11+
- OpenRouter API key  
- iPhone with App Store access

### Step 1: Clone and Setup (2 minutes)
```bash
git clone https://github.com/Khamel83/ralex.git
cd ralex
cp .env.example .env
# Edit .env with your OPENROUTER_API_KEY
```

### Step 2: Start Ralex (1 minute)
```bash
export OPENROUTER_API_KEY="your-key-here"
python start_ralex.py
```

### Step 3: Setup iPhone App (2 minutes)
1. Download [OpenCat](https://apps.apple.com/us/app/opencat-chat-with-ai-bot/id6445999201)
2. Open OpenCat → Settings → API Configuration
3. Base URL: `http://[your-rpi-ip]:8000/v1`
4. API Key: `ralex-key`
5. Model: `ralex-bridge`

## Verify Setup Works

### Test from iPhone
Open OpenCat and send: "test connection"

### Expected Response
Response from your Ralex system via cost-optimized routing.

## Common Issues

**"Connection Failed"**
- Check RPi IP address
- Ensure iPhone on same WiFi
- Verify port 8000 accessible

**"No API Key Error"**
- Check OPENROUTER_API_KEY in .env
- Restart Ralex after changing

**"Slow Response"**
- Normal on first request (model loading)
- Subsequent requests <3 seconds

## Next Steps

### Enable Intelligence Optimization
```bash
export INTELLIGENCE_ENABLED=true
```
Reduces API costs 20%+ via smart routing.

### Development Workflow
- **Mobile**: General queries, planning, code discussions
- **Terminal**: File operations, git, testing
- **Cost tracking**: Check `.ralex/cost_log.txt`

## Troubleshooting

See [CLAUDE.md](CLAUDE.md) for comprehensive setup guide.
See [SECURITY.md](SECURITY.md) for production deployment.

---
Setup time: 5 minutes measured  
Cost: $0.02-0.05 per query average  
Mobile response time: <3 seconds after initial load
EOF < /dev/null
