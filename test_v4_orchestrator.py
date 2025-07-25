#!/usr/bin/env python3
"""
Test script for Ralex V4 Orchestrator

Tests the basic orchestration pipeline with stub implementations.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from ralex_core.v4_orchestrator import RalexV4Orchestrator, initialize_orchestrator, get_orchestrator


async def test_orchestrator_initialization():
    """Test orchestrator initialization"""
    print("🔧 Testing orchestrator initialization...")
    
    orchestrator = RalexV4Orchestrator(str(Path.cwd()))
    success = await orchestrator.initialize()
    
    if success:
        print("✅ Orchestrator initialized successfully")
        return orchestrator
    else:
        print("❌ Orchestrator initialization failed")
        return None


async def test_voice_command_processing(orchestrator):
    """Test voice command processing"""
    print("\n🎙️ Testing voice command processing...")
    
    test_commands = [
        "create a new python file called test.py",
        "fix the bug in authentication.py, execute",
        "refactor the user model for better performance, send it",
        "what is the purpose of this function?",
        "deploy this feature to staging, go ahead"
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n--- Test {i}: '{command}' ---")
        
        result = await orchestrator.process_voice_command(
            command=command,
            session_id="test_session_001"
        )
        
        print(f"Status: {result.status.value}")
        print(f"Message: {result.message}")
        print(f"Execution time: {result.execution_time:.3f}s")
        print(f"Cost: ${result.cost:.4f}")
        
        if result.data:
            print(f"Command type: {result.data.get('parsed_command', {}).get('command_type', 'unknown')}")
            print(f"Auto-submit: {result.data.get('parsed_command', {}).get('auto_submit', False)}")


async def test_workflow_execution(orchestrator):
    """Test workflow execution"""
    print("\n🔄 Testing workflow execution...")
    
    workflows = ["deploy", "feature", "bugfix"]
    
    for workflow in workflows:
        print(f"\n--- Testing workflow: {workflow} ---")
        
        result = await orchestrator.execute_workflow(
            workflow_name=workflow,
            session_id="test_session_001",
            parameters={"target": "staging"}
        )
        
        print(f"Status: {result.status.value}")
        print(f"Message: {result.message}")
        print(f"Execution time: {result.execution_time:.3f}s")
        print(f"Cost: ${result.cost:.4f}")


async def test_session_status(orchestrator):
    """Test session status retrieval"""
    print("\n📊 Testing session status...")
    
    status = await orchestrator.get_session_status("test_session_001")
    
    print(f"Session ID: {status['session_id']}")
    print(f"Status: {status['status']}")
    print(f"Context files: {status['context_files']}")
    print(f"Budget remaining: ${status['budget_remaining']:.2f}")


async def test_error_handling(orchestrator):
    """Test error handling"""
    print("\n🚨 Testing error handling...")
    
    # Test with invalid command
    result = await orchestrator.process_voice_command(
        command="",  # Empty command should trigger error
        session_id="test_session_001"
    )
    
    print(f"Empty command result: {result.status.value} - {result.message}")
    
    # Test with potentially dangerous command
    result = await orchestrator.process_voice_command(
        command="sudo rm -rf / --no-preserve-root",
        session_id="test_session_001"
    )
    
    print(f"Dangerous command result: {result.status.value} - {result.message}")


async def main():
    """Main test function"""
    print("🚀 Ralex V4 Orchestrator Test Suite")
    print("=" * 50)
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Test initialization
        orchestrator = await test_orchestrator_initialization()
        if not orchestrator:
            return
        
        # Run tests
        await test_voice_command_processing(orchestrator)
        await test_workflow_execution(orchestrator)
        await test_session_status(orchestrator)
        await test_error_handling(orchestrator)
        
        # Shutdown
        print("\n🔄 Shutting down orchestrator...")
        await orchestrator.shutdown()
        print("✅ Orchestrator shutdown complete")
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())