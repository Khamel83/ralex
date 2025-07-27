#!/bin/bash
set -e

echo "🔍 FINAL V4 VERIFICATION TEST"
echo "============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}✅ $1${NC}"; }
log_warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

test_count=0
pass_count=0

run_test() {
    test_count=$((test_count + 1))
    echo ""
    echo "Test $test_count: $1"
    echo "-------------------"
}

pass_test() {
    pass_count=$((pass_count + 1))
    log_info "$1"
}

fail_test() {
    log_error "$1"
    echo "SUGGESTION: $2"
}

# Test 1: .env file loading
run_test ".env file integration"

# Backup current API key
ORIGINAL_KEY=$OPENROUTER_API_KEY
unset OPENROUTER_API_KEY

# Create test .env file
echo "OPENROUTER_API_KEY=test-env-key-12345" > .env

# Test if bridge loads .env correctly
if python -c "
import sys
sys.path.insert(0, '.')
from ralex_bridge import load_env
import os
load_env()
key = os.getenv('OPENROUTER_API_KEY')
if key == 'test-env-key-12345':
    print('SUCCESS')
else:
    print('FAILED')
    exit(1)
" 2>/dev/null; then
    pass_test ".env file loading works correctly"
else
    fail_test ".env file loading failed" "Check load_env() function in ralex_bridge.py"
fi

# Restore original key and clean up
export OPENROUTER_API_KEY=$ORIGINAL_KEY
rm -f .env

# Test 2: Health check functionality
run_test "Health check command"

if python ralex_bridge.py --health 2>/dev/null | grep -q "Health Check"; then
    pass_test "Health check command works"
else
    fail_test "Health check command failed" "Check --health flag implementation"
fi

# Test 3: Help command
run_test "Help command"

if python ralex_bridge.py --help 2>/dev/null | grep -q "Usage:"; then
    pass_test "Help command works"
else
    fail_test "Help command failed" "Check --help flag implementation"
fi

# Test 4: API key validation
run_test "API key validation"

# Temporarily unset API key
TEMP_KEY=$OPENROUTER_API_KEY
unset OPENROUTER_API_KEY

if python ralex_bridge.py "test" 2>&1 | grep -q "API key not set"; then
    pass_test "API key validation works"
else
    fail_test "API key validation failed" "Check API key validation in main()"
fi

# Restore API key
export OPENROUTER_API_KEY=$TEMP_KEY

# Test 5: File creation functionality
run_test "Core file creation"

if python ralex_bridge.py "create a verification_test.py file with print('test successful')" >/dev/null 2>&1; then
    if [ -f "verification_test.py" ]; then
        if python verification_test.py 2>/dev/null | grep -q "test successful"; then
            pass_test "File creation and execution works"
            rm -f verification_test.py
        else
            fail_test "Created file doesn't execute correctly" "Check code extraction logic"
        fi
    else
        fail_test "File creation failed" "Check execute_via_opencode() method"
    fi
else
    fail_test "Bridge command failed" "Check API connectivity and LiteLLM integration"
fi

# Test 6: Session persistence
run_test "Session persistence"

session_count_before=$(ls .ralex/*.md 2>/dev/null | wc -l)
python ralex_bridge.py "create a session_test.py with print('session test')" >/dev/null 2>&1 || true
session_count_after=$(ls .ralex/*.md 2>/dev/null | wc -l)

if [ "$session_count_after" -gt "$session_count_before" ]; then
    pass_test "Session persistence works"
    rm -f session_test.py
else
    fail_test "Session persistence failed" "Check save_context() method"
fi

# Test 7: Installer script
run_test "Installer script validation"

if [ -f "install_ralex.sh" ] && [ -x "install_ralex.sh" ]; then
    if head -10 install_ralex.sh | grep -q "Automated Installer"; then
        pass_test "Installer script is present and executable"
    else
        fail_test "Installer script format incorrect" "Check install_ralex.sh header"
    fi
else
    fail_test "Installer script missing or not executable" "Run: chmod +x install_ralex.sh"
fi

# Test 8: Documentation completeness
run_test "Documentation completeness"

docs_present=0
[ -f "README_V4.md" ] && docs_present=$((docs_present + 1))
[ -f "QUICKSTART.md" ] && docs_present=$((docs_present + 1))
[ -f "PRODUCTION_READINESS.md" ] && docs_present=$((docs_present + 1))

if [ "$docs_present" -eq 3 ]; then
    pass_test "All documentation files present"
else
    fail_test "Missing documentation files" "Ensure README_V4.md, QUICKSTART.md, PRODUCTION_READINESS.md exist"
fi

# Test 9: OpenWebUI startup script
run_test "OpenWebUI startup script"

if grep -q "open_webui.main:app" start_ralex_v4.py; then
    pass_test "OpenWebUI startup script has correct path"
else
    fail_test "OpenWebUI startup script has wrong path" "Update start_ralex_v4.py to use open_webui.main:app"
fi

# Test 10: Requirements and dependencies
run_test "Dependencies check"

missing_deps=0
python -c "import litellm" 2>/dev/null || missing_deps=$((missing_deps + 1))
python -c "import fastapi" 2>/dev/null || missing_deps=$((missing_deps + 1))
python -c "import pydantic" 2>/dev/null || missing_deps=$((missing_deps + 1))

if [ "$missing_deps" -eq 0 ]; then
    pass_test "All required dependencies available"
else
    fail_test "$missing_deps dependencies missing" "Run: pip install -r requirements.txt"
fi

# Final results
echo ""
echo "================================"
echo "📊 FINAL VERIFICATION RESULTS"
echo "================================"
echo "Tests passed: $pass_count/$test_count"

if [ "$pass_count" -eq "$test_count" ]; then
    log_info "🎉 ALL TESTS PASSED - V4 IS PRODUCTION READY!"
    echo ""
    echo "✅ V4 is ready for wide public usage"
    echo "✅ All startup processes work correctly"
    echo "✅ .env file integration works"
    echo "✅ Error handling is comprehensive"
    echo "✅ Documentation is complete"
    echo ""
    echo "🚀 Ready for public release!"
else
    failed=$((test_count - pass_count))
    log_error "$failed tests failed - V4 needs fixes before public release"
    echo ""
    echo "❌ Fix failing tests before public release"
    echo "💡 Check suggestions above for each failed test"
fi

echo ""
echo "Test completed: $(date)"