#!/usr/bin/env python3
"""
Test file for OpenCode.ai evaluation.
This file will be used to test YOLO functionality and compare with Ralex.
"""

def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def test_basic_functionality():
    """Test basic functionality that OpenCode.ai should be able to modify."""
    print("Testing basic functionality...")
    result = fibonacci(5)
    print(f"Fibonacci(5) = {result}")
    return result

if __name__ == "__main__":
    test_basic_functionality()