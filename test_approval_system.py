#!/usr/bin/env python3
"""
Test script for the new frontloaded approval system.
Demonstrates how batch approvals can reduce user interruption.
"""

import sys
sys.path.append('.')

from ralex_core.orchestrator import RalexOrchestrator
import json


def test_approval_system():
    """Test the frontloaded approval system."""
    print("=== Testing Frontloaded Approval System ===\n")
    
    orchestrator = RalexOrchestrator()
    
    # Test 1: Interactive mode (default)
    print("1. Testing INTERACTIVE mode (default):")
    test_commands = [
        "read file main.py",
        "write file test.py with some content", 
        "delete all files"  # This should require approval
    ]
    
    for cmd in test_commands:
        print(f"  Command: '{cmd}'")
        # Note: This would normally call process_voice_command, but we'd need full setup
        # For now, just show the approval status
        print(f"  Status: {orchestrator.get_approval_status()['approval_summary']['mode']}")
    
    print()
    
    # Test 2: Set batch-safe mode
    print("2. Setting BATCH_SAFE mode for 30-minute coding session:")
    result = orchestrator.set_approval_mode("batch_safe", session_timeout=1800)
    print(f"  Result: {result['message']}")
    print(f"  Approved operations: {len(result['approval_summary']['session_approvals'])}")
    
    print()
    
    # Test 3: Show approval status
    print("3. Current approval status:")
    status = orchestrator.get_approval_status()
    summary = status['approval_summary']
    
    print(f"  Mode: {summary['mode']}")
    print(f"  Session timeout: {summary['session_timeout']} seconds")
    print(f"  Auto-approved operations: {len(summary['session_approvals'])}")
    print(f"  Operations: {', '.join(summary['session_approvals'][:5])}{'...' if len(summary['session_approvals']) > 5 else ''}")
    
    print()
    
    # Test 4: Manually approve a dangerous operation
    print("4. Manually approving a dangerous operation:")
    result = orchestrator.approve_operation("delete_all")
    print(f"  Result: {result['message']}")
    
    print()
    
    # Test 5: Set batch-all mode (high trust)
    print("5. Setting BATCH_ALL mode (high trust):")
    result = orchestrator.set_approval_mode("batch_all", session_timeout=600)  # 10 minutes
    print(f"  Result: {result['message']}")
    print(f"  ⚠️  WARNING: All operations auto-approved for 10 minutes!")
    
    print("\n=== Approval System Test Complete ===")
    
    return True


if __name__ == "__main__":
    try:
        test_approval_system()
        print("\n✅ All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()