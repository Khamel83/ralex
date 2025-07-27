# Ralex V4 Quickstart Guide

## What is Ralex?
Ralex is a voice-controlled AI coding assistant that helps you write, edit, and manage code by talking to it. Say "create a Python calculator" and it will write the actual code files for you automatically.

**Key difference**: Instead of just getting code suggestions, Ralex actually creates the files on your computer.

## Why Use Ralex?
- **Voice control**: Code by speaking instead of typing
- **Cost-effective**: Uses cheap AI models intelligently 
- **Strategic**: Thinks before acting (won't break your code)
- **Complete workflow**: From idea to working code in one command
- **Cross-device**: Save your coding sessions and access from anywhere

## 5-Minute Setup

### 1. Get the Code
```bash
git clone https://github.com/Khamel83/ralex.git
cd ralex
```

### 2. Install Dependencies  
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Get API Key (Free tier available)
- Go to [OpenRouter.ai](https://openrouter.ai)
- Sign up for free account (required for API access)
- Go to "Keys" section in dashboard  
- Copy your API key
- **Option 1**: Set in terminal: `export OPENROUTER_API_KEY="your-key-here"`
- **Option 2**: Create `.env` file: `echo "OPENROUTER_API_KEY=your-key-here" > .env`
- **Note**: Without this API key, Ralex cannot access AI models

### 4. Test It Works
```bash
python ralex_bridge.py "create a hello.py file with a print statement"
```

**Expected results** (this confirms everything is working):
- ✅ A new `hello.py` file appears in your current directory
- ✅ A session log appears in `.ralex/session_TIMESTAMP.md`
- ✅ Success message in terminal with model used and execution details
- ✅ You can run `python hello.py` and see "Hello, World!" output

**If this doesn't work**, check the troubleshooting section below.

### 5. Run Full Interface (Optional)
```bash
python start_ralex_v4.py
```
Then open http://localhost:3000 for web interface with voice input.

## How to Use Ralex

### Basic Commands
```bash
# Create files
python ralex_bridge.py "create a calculator.py with add and subtract functions"

# Edit existing code  
python ralex_bridge.py "add error handling to my calculator"

# Explain code
python ralex_bridge.py "explain what this function does in main.py"

# Debug issues
python ralex_bridge.py "fix the syntax error in my script"
```

### Voice Commands (Web Interface)
1. Open http://localhost:3000 after running `python start_ralex_v4.py`
2. Click the microphone button
3. Say: "Create a web scraper in Python"
4. Watch as it writes the code automatically

### What Happens Behind the Scenes
1. **AgentOS** analyzes your request for safety and complexity
2. **LiteLLM** picks the cheapest appropriate AI model  
3. **OpenRouter** calls the AI model via API
4. **OpenCode** executes the AI's coding instructions
5. **Context** gets saved to `.ralex/` folder and synced to git

## Example Workflows

### Create a Simple Web App
```bash
python ralex_bridge.py "create a Flask web app with a home page that says hello world"
```

### Build a Data Script
```bash
python ralex_bridge.py "create a script that reads a CSV file and shows basic statistics"
```

### Add Tests
```bash
python ralex_bridge.py "create unit tests for my calculator.py file"
```

## Understanding Your Sessions

Every interaction creates a session file in `.ralex/session_TIMESTAMP.md` containing:
- Your original request
- How AgentOS analyzed it
- Which AI model was selected
- The AI's response  
- What code was created/modified

These files are automatically committed to git so you can:
- Track your coding history
- Sync across devices
- Learn from past solutions

## Troubleshooting

### "ModuleNotFoundError"
```bash
# Make sure virtual environment is activated
source .venv/bin/activate
pip install -r requirements.txt
```

### "API Key Error"  
```bash
# Check your OpenRouter API key is set
echo $OPENROUTER_API_KEY
# If empty, set it:
export OPENROUTER_API_KEY="your-key-here"
```

### "No files created"
- Check if you have write permissions in the current directory
- Look at the session log in `.ralex/` for error details
- Try a simpler command first

### Web Interface Won't Start
- Make sure no other service is using port 3000
- Check the terminal output for error messages
- Try the command-line version first

## Next Steps

### Customize Model Selection
Edit `ralex_bridge.py` to change which AI models are used for different complexity levels.

### Add Your Own Commands  
The bridge is designed to be extended. Add new command patterns in the `execute_via_opencode` method.

### Integration with Your Editor
- Use the command-line version from within VS Code terminal
- Set up keyboard shortcuts to call common Ralex commands
- Pipe Ralex output to your clipboard for easy copying

### Team Usage
- Share your `.ralex/` session logs with teammates
- Use git to collaborate on Ralex-generated code
- Set up shared API keys for team projects

## Cost Management

Ralex is designed to be cost-effective:
- Uses cheaper models for simple tasks
- Only uses expensive models for complex coding
- Tracks usage in session logs
- Free tier on OpenRouter covers most personal use

Typical costs:
- Simple file creation: $0.001
- Complex web app: $0.01-0.05  
- Most users spend <$5/month

## Support

- **Issues**: Report bugs at [GitHub Issues](https://github.com/Khamel83/ralex/issues)
- **Documentation**: Check `docs/` folder for detailed guides
- **Examples**: Look at `.ralex/` session files for inspiration

## What Makes Ralex Different

Unlike other AI coding tools:
- **Strategic thinking**: AgentOS prevents rushed decisions
- **Cost optimization**: Smart model selection saves money
- **Voice-first**: Designed for hands-free coding
- **Complete pipeline**: From voice to working code
- **Session history**: Never lose your coding conversations

Ready to start voice-coding? Try: `python ralex_bridge.py "create a simple game"`