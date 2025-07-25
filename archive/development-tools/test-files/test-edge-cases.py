#!/usr/bin/env python3
"""Test edge cases and error handling"""
import os

def test_case(prompt, description):
    print(f"\n🧪 {description}")
    print(f"   Prompt: '{prompt}'")
    result = os.popen(f'python3 direct-openrouter-test.py "{prompt}" 2>&1 | head -n 8').read()
    print(f"   Result: {result.strip()}")

print("🧪 EDGE CASE TESTING")
print("=" * 50)

# Test empty/minimal prompts
test_case("", "Empty prompt")
test_case("?", "Single character")
test_case("help", "Generic help request")

# Test mixed patterns  
test_case("fix this complex refactoring task", "Mixed patterns (fix + complex)")
test_case("yolo refactor this architecture now", "Mixed patterns (yolo + refactor)")

# Test very long prompts
long_prompt = "This is a very long prompt " * 50 + "with a fix request at the end"
test_case(long_prompt[:100] + "...", "Very long prompt (truncated for display)")

# Test special characters
test_case("fix this 'code' with \"quotes\" and $variables", "Special characters")

# Test non-English (if it triggers patterns)
test_case("réparer ce bug rapidement", "Non-English")

print("\n✅ Edge case testing complete!")