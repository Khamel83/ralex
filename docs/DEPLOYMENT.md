# Ralex V2 Deployment Guide

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (recommended: Python 3.11)
- **pip** package manager
- **OpenRouter API Key** ([Get one here](https://openrouter.ai/))
- **4GB+ RAM** (8GB recommended for optimal performance)
- **50MB+ disk space**

### Installation Options

#### Option 1: Direct Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/Khamel83/ralex.git
cd ralex

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Set your API key
export OPENROUTER_API_KEY="your-key-here"

# Run Ralex
python -m ralex_core.launcher
```

#### Option 2: Using direnv (Development)

```bash
git clone https://github.com/Khamel83/ralex.git
cd ralex
direnv allow  # Automatically sets up environment

# Run Ralex
python -m ralex_core.launcher
```

## 🔧 Configuration

### Environment Variables

```bash
export OPENROUTER_API_KEY="your-key-here"
export RALEX_ANALYTICS=false  # Optional: disable analytics
```

### Configuration Files

- `config/model_tiers.json` - Model tier definitions
- `config/intent_routes.json` - Intent routing rules
- `config/pattern_rules.json` - Pattern matching rules

## 🐳 Docker Deployment

```bash
# Build image
docker build -t ralex .

# Run container
docker run -e OPENROUTER_API_KEY="your-key" ralex "write a hello world program"
```

## 🖥️ Server Deployment

### systemd Service

Create `/etc/systemd/system/ralex.service`:

```ini
[Unit]
Description=Ralex V2 Service
After=network.target

[Service]
Type=simple
User=ralex
WorkingDirectory=/opt/ralex
ExecStart=/opt/ralex/.venv/bin/python -m ralex_core.launcher --interactive
Restart=always
Environment=OPENROUTER_API_KEY=your-key-here

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ralex
sudo systemctl start ralex
sudo systemctl status ralex
```

## 🚀 Usage Examples

### Basic Usage
```bash
python -m ralex_core.launcher "write hello world in python"
```

### Interactive Mode
```bash
python -m ralex_core.launcher --interactive
```

### File-specific Operations
```bash
python -m ralex_core.launcher --file test.py "fix this syntax error"
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run linting
ruff check .

# Run formatting
black .
```

## 🔧 Troubleshooting

### Common Issues

**Permission Error**
```bash
chmod +x ralex
```

**API Key Issues**
```bash
export OPENROUTER_API_KEY="your-actual-key"
```

**Python Path Issues**
```bash
pip install -e .
```

## 📊 Monitoring

### Health Check
```bash
python -m ralex_core.launcher --health-check
```

### Budget Status
```bash
python -m ralex_core.launcher --budget-status
```

## 🎉 Success!

Ralex V2 is now deployed and ready to assist with your coding workflow.