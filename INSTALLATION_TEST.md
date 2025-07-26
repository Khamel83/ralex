# Ralex V4 Installation Test

## Quick Verification Script

Run this to verify your Ralex V4 installation is working correctly:

```bash
#!/bin/bash
echo "🧪 Testing Ralex V4 Installation..."

# Test 1: Check if repository is cloned
if [ ! -f "ralex_bridge.py" ]; then
    echo "❌ ralex_bridge.py not found. Make sure you're in the ralex directory."
    exit 1
fi
echo "✅ Repository files found"

# Test 2: Check Python environment
if ! python --version &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi
echo "✅ Python found: $(python --version)"

# Test 3: Check required packages
if ! python -c "import litellm" &> /dev/null; then
    echo "❌ LiteLLM not installed. Run: pip install -r requirements.txt"
    exit 1
fi
echo "✅ Required packages installed"

# Test 4: Check API key
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ OPENROUTER_API_KEY not set. Run: export OPENROUTER_API_KEY='your-key'"
    exit 1
fi
echo "✅ API key configured"

# Test 5: Test basic functionality
echo "🚀 Testing basic file creation..."
output=$(python ralex_bridge.py "create a test_installation.py with print('Installation successful')" 2>&1)

if [ -f "test_installation.py" ]; then
    echo "✅ File creation works"
    python test_installation.py
    rm test_installation.py
else
    echo "❌ File creation failed. Output:"
    echo "$output"
    exit 1
fi

# Test 6: Check session logging
if [ -d ".ralex" ] && [ "$(ls -A .ralex)" ]; then
    echo "✅ Session logging works"
else
    echo "❌ Session logging not working"
    exit 1
fi

echo ""
echo "🎉 Ralex V4 installation test PASSED!"
echo "📖 Next steps:"
echo "   - Try: python ralex_bridge.py 'create a simple calculator'"
echo "   - Read: QUICKSTART.md for more examples"
echo "   - Web UI: python start_ralex_v4.py (then open http://localhost:3000)"
```

## Expected Test Output

```
🧪 Testing Ralex V4 Installation...
✅ Repository files found
✅ Python found: Python 3.11.2
✅ Required packages installed
✅ API key configured
🚀 Testing basic file creation...
✅ File creation works
Installation successful
✅ Session logging works

🎉 Ralex V4 installation test PASSED!
📖 Next steps:
   - Try: python ralex_bridge.py 'create a simple calculator'
   - Read: QUICKSTART.md for more examples
   - Web UI: python start_ralex_v4.py (then open http://localhost:3000)
```

## If Tests Fail

### ❌ Repository files not found
```bash
cd /path/to/ralex  # Make sure you're in the right directory
ls ralex_bridge.py  # Should exist
```

### ❌ Python not found
```bash
# Install Python 3.8+ from python.org
python3 --version  # Try python3 instead of python
```

### ❌ Required packages not installed
```bash
pip install -r requirements.txt
# Or if using virtual environment:
source .venv/bin/activate
pip install -r requirements.txt
```

### ❌ API key not set
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-actual-key-here"
echo $OPENROUTER_API_KEY  # Should show your key
```

### ❌ File creation failed
- Check your internet connection (API calls required)
- Verify API key is correct
- Check permissions in current directory
- Look at error message for specific issue

### ❌ Session logging not working
- Check if `.ralex/` directory exists
- Verify write permissions
- Check git configuration (sessions are auto-committed)

## Manual Test Commands

If the script doesn't work, test manually:

```bash
# Test 1: Basic file creation
python ralex_bridge.py "create a hello.py with print('hello world')"
ls hello.py  # Should exist
python hello.py  # Should print "hello world"

# Test 2: Session logging
ls .ralex/  # Should contain session_*.md files
cat .ralex/session_*.md | tail -20  # Should show session details

# Test 3: Different file types
python ralex_bridge.py "create a config.json with basic settings"
python ralex_bridge.py "create a README.md explaining this project"

# Test 4: Complex requests  
python ralex_bridge.py "create a web scraper that gets news headlines"
```

All of these should work without errors and create actual files.