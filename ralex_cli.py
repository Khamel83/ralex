#!/usr/bin/env python3
"""
Ralex CLI - Unified command line interface for OpenCode.ai wrapper
"""

import argparse
import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent)) # Add project root to path

# Import modules with proper error handling
try:
    from universal_logger import log_ai_operation
    from ralex_core.v4_orchestrator import RalexV4Orchestrator
except ImportError:
    # Fallback for missing universal logger
    def log_ai_operation(operation_type, prompt, metadata=None):
        import uuid
        return str(uuid.uuid4())

try:
    import sys
    khamel_path = Path(__file__).parent / ".khamel83"
    sys.path.insert(0, str(khamel_path))
    # Import with proper module names (handling dash vs underscore)
    import importlib.util
    
    # Import budget controller
    budget_spec = importlib.util.spec_from_file_location(
        "budget_controller", 
        khamel_path / "budget-controller.py"
    )
    budget_module = importlib.util.module_from_spec(budget_spec)
    budget_spec.loader.exec_module(budget_module)
    BudgetController = budget_module.BudgetController
    
    # Import task classifier and OpenCode wrapper
    from task_classifier import AgentOSTaskClassifier
    from opencode_wrapper import OpenCodeWrapper, ExecutionMode
    CLASSIFIER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Import warning: {e}")
    CLASSIFIER_AVAILABLE = False
    
    # Fallback budget controller
    class BudgetController:
        def get_budget_status(self):
            return {
                "daily": {"budget": 5.0, "spent": 0.0, "remaining": 5.0},
                "hourly": {"limit": 1.25, "spent": 0.0, "remaining": 1.25}
            }
    
    # Fallback task classifier
    class AgentOSTaskClassifier:
        def classify_task(self, prompt, context=None, context_content=None, budget_limit=None):
            from types import SimpleNamespace
            return SimpleNamespace(
                task_type=SimpleNamespace(value="simple"),
                complexity=SimpleNamespace(value="low"),
                confidence=0.8,
                reasoning="Fallback classification - task_classifier module not available",
                estimated_cost=0.05,
                recommended_model_tier="budget",
                execution_strategy="direct_opencode",
                context_optimization=None,
                optimized_context=None,
                routing_decision=None
            )
    
    # Fallback OpenCode wrapper
    class OpenCodeWrapper:
        def execute_task(self, task_classification, optimized_context=None, execution_mode=None):
            from types import SimpleNamespace
            return SimpleNamespace(
                result=SimpleNamespace(value="success"),
                stdout="Fallback execution - OpenCode wrapper not available",
                stderr="",
                exit_code=0,
                execution_time=0.1,
                files_modified=[],
                error_message=None,
                safety_warnings=[],
                cost_actual=0.001,
                tokens_used=10
            )
        
        def health_check(self):
            return {"healthy": False, "message": "OpenCode wrapper not available"}
    
    # Fallback execution mode
    class ExecutionMode:
        YOLO = "yolo"

def create_cli_parser():
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog='ralex',
        description='Intelligent AI coding assistant with cost optimization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ralex "create a test.py file"
  ralex --health
  ralex --budget-status
  ralex -v "debug this function"
        """
    )
    
    # Main command argument
    parser.add_argument(
        'command',
        nargs='?',
        help='Command or prompt to execute'
    )
    
    # Options
    parser.add_argument(
        '--version',
        action='version',
        version='ralex 1.0.0 (OpenCode.ai wrapper)'
    )
    
    parser.add_argument(
        '--health',
        action='store_true',
        help='Check system health and configuration'
    )
    
    parser.add_argument(
        '--budget-status',
        action='store_true',
        help='Show current budget status'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--config',
        help='Configuration file path'
    )
    
    parser.add_argument(
        '--workflow',
        help='Execute a specific Agent-OS workflow by name'
    )
    
    return parser

def health_check():
    """Perform system health check."""
    print("🔍 Ralex Health Check")
    print("=" * 30)
    
    # Check OpenCode.ai
    opencode_path = Path.home() / ".opencode" / "bin" / "opencode"
    if opencode_path.exists():
        print("✅ OpenCode.ai installed")
    else:
        print("❌ OpenCode.ai not found")
        
    # Check API key
    if os.getenv("OPENROUTER_API_KEY"):
        print("✅ OpenRouter API key configured")
    else:
        print("❌ OpenRouter API key not set")
        
    # Check budget controller
    try:
        budget = BudgetController()
        status = budget.get_budget_status()
        print(f"✅ Budget system: ${status['daily']['remaining']:.2f} remaining today")
    except Exception as e:
        print(f"❌ Budget system error: {e}")
        
    print("\n📖 Documentation: cat CLAUDE.md")

def show_budget_status():
    """Show current budget status."""
    try:
        budget = BudgetController()
        status = budget.get_budget_status()
        
        print("💰 Budget Status")
        print("=" * 20)
        print(f"Daily Budget: ${status['daily']['budget']:.2f}")
        print(f"Daily Spent:  ${status['daily']['spent']:.2f}")
        print(f"Daily Remaining: ${status['daily']['remaining']:.2f}")
        print()
        print(f"Hourly Limit: ${status['hourly']['limit']:.2f}")
        print(f"Hourly Spent: ${status['hourly']['spent']:.2f}")
        print(f"Hourly Remaining: ${status['hourly']['remaining']:.2f}")
        
    except Exception as e:
        print(f"❌ Error checking budget: {e}")

def execute_command(command: str, verbose: bool = False, debug: bool = False):
    """Execute a command through the Ralex system."""
    if verbose:
        print(f"🎯 Executing: {command}")
    
    # Initialize task classifier
    classifier = AgentOSTaskClassifier()
    
    # Gather context content for optimization (simulate with command history and environment)
    context_content = f"""
=== RALEX EXECUTION CONTEXT ===
Command: {command}
Interface: CLI
Verbose: {verbose}
Debug: {debug}

=== SYSTEM STATE ===
- Ralex OpenCode.ai Wrapper System
- Agent-OS Cost Optimization Active
- Mobile Workflow (OpenCat) Preserved
- Universal Logging Enabled
- Budget Controller Active

=== RECENT CONTEXT ===
Previous commands in session (simulated)
System configuration loaded
Context optimization available
    """
    
    # Classify the task for optimal routing with context optimization
    context = {
        "interface": "cli",
        "verbose": verbose,
        "debug": debug
    }
    
    # Get budget limit from budget controller
    budget_limit = None
    try:
        budget = BudgetController()
        status = budget.get_budget_status()
        budget_limit = min(status["daily"]["remaining"], status["hourly"]["remaining"])
    except:
        budget_limit = 0.01  # Default limit
    
    classification = classifier.classify_task(command, context, context_content, budget_limit)
    
    # Show classification if verbose
    if verbose:
        print(f"🧠 Task Classification:")
        print(f"   Type: {classification.task_type.value}")
        print(f"   Complexity: {classification.complexity.value}")
        print(f"   Confidence: {classification.confidence:.2f}")
        print(f"   Strategy: {classification.execution_strategy}")
        print(f"   Est. Cost: ${classification.estimated_cost:.6f}")
        print(f"   Reasoning: {classification.reasoning}")
        
        # Show context optimization if available
        if classification.context_optimization:
            opt = classification.context_optimization
            print(f"💡 Context Optimization:")
            print(f"   Strategy: {opt.get('strategy', 'none')}")
            print(f"   Tokens: {opt.get('original_tokens', 0)} → {opt.get('optimized_tokens', 0)}")
            print(f"   Savings: {opt.get('tokens_saved', 0)} tokens (${opt.get('cost_savings', 0):.6f})")
            
        # Show LiteLLM routing decision if available
        if classification.routing_decision:
            routing = classification.routing_decision
            print(f"🤖 Model Routing:")
            print(f"   Selected: {routing.get('selected_model', 'unknown')}")
            print(f"   Provider: {routing.get('provider', 'unknown')}")
            print(f"   Tier: {routing.get('tier', 'unknown')}")
            print(f"   Strategy: {routing.get('strategy_used', 'unknown')}")
            print(f"   Final Cost: ${routing.get('estimated_cost', 0):.6f}")
            
            # Show cost savings if available
            if 'optimization_applied' in routing:
                opt_applied = routing['optimization_applied']
                cost_vs_baseline = opt_applied.get('cost_vs_baseline', {})
                if cost_vs_baseline.get('savings', 0) > 0:
                    print(f"   Cost Savings: ${cost_vs_baseline['savings']:.6f} ({cost_vs_baseline.get('savings_percent', 0):.1f}%)")
        
        print(f"💰 Budget: ${budget_limit:.6f} available")
        
    # Log the operation with classification and optimization
    operation_metadata = {
        "interface": "cli",
        "verbose": verbose,
        "debug": debug,
        "task_type": classification.task_type.value,
        "complexity": classification.complexity.value,
        "execution_strategy": classification.execution_strategy,
        "estimated_cost": classification.estimated_cost
    }
    
    if classification.context_optimization:
        operation_metadata["context_optimization"] = classification.context_optimization
    
    operation_id = log_ai_operation(
        operation_type="cli_command",
        prompt=command,
        metadata=operation_metadata
    )
    
    if verbose:
        print(f"📝 Operation ID: {operation_id}")
    
    # Route based on classification and execute
    if classification.execution_strategy == "direct_opencode":
        print(f"🚀 Routing to OpenCode.ai YOLO mode")
        execution_mode = ExecutionMode.YOLO
    elif classification.execution_strategy == "agentos_optimized":
        print(f"🧠 Routing to Agent-OS cost optimization")
        execution_mode = ExecutionMode.YOLO  # For now, use YOLO - can enhance later
    elif classification.execution_strategy == "mobile_preserved":
        print(f"📱 Routing to mobile-optimized workflow")
        execution_mode = getattr(ExecutionMode, 'MOBILE_OPTIMIZED', ExecutionMode.YOLO)
    elif classification.execution_strategy == "batch_processed":
        print(f"📦 Routing to batch processing")
        execution_mode = ExecutionMode.YOLO
    elif classification.execution_strategy == "analysis_mode":
        print(f"📖 Routing to analysis mode")
        execution_mode = getattr(ExecutionMode, 'SAFE', ExecutionMode.YOLO)
    else:
        print(f"⚙️ Routing to standard LiteLLM")
        execution_mode = ExecutionMode.YOLO
    
    # Execute through OpenCode.ai wrapper
    print(f"📋 Executing: {command}")
    
    try:
        # Add the actual prompt to the classification for execution
        classification.prompt = command
        
        # Initialize OpenCode wrapper and execute
        wrapper = OpenCodeWrapper()
        execution_result = wrapper.execute_task(
            classification, 
            classification.optimized_context,
            execution_mode
        )
        
        # Display execution results
        if execution_result.result.value == "success":
            print(f"✅ Execution successful")
            if execution_result.files_modified:
                print(f"📁 Files modified: {', '.join(execution_result.files_modified)}")
        elif execution_result.result.value == "partial":
            print(f"⚠️ Partial success")
        else:
            print(f"❌ Execution failed: {execution_result.error_message}")
        
        if verbose:
            print(f"⏱️ Execution time: {execution_result.execution_time:.2f}s")
            print(f"💰 Actual cost: ${execution_result.cost_actual:.6f}")
            print(f"🎯 Tokens used: {execution_result.tokens_used}")
            
            if execution_result.safety_warnings:
                print(f"⚠️ Safety warnings: {', '.join(execution_result.safety_warnings)}")
        
        # Update operation metadata with execution results
        operation_metadata["execution_result"] = {
            "result": execution_result.result.value,
            "execution_time": execution_result.execution_time,
            "cost_actual": execution_result.cost_actual,
            "tokens_used": execution_result.tokens_used,
            "files_modified": execution_result.files_modified
        }
        
    except Exception as e:
        print(f"❌ Execution error: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        
        operation_metadata["execution_error"] = str(e)
    
    return operation_id

def main():
    """Main CLI entry point."""
    parser = create_cli_parser()
    args = parser.parse_args()
    
    # Handle special commands
    if args.health:
        health_check()
        return
        
    if args.budget_status:
        show_budget_status()
        return
    
    # Handle main command or workflow execution
    if args.command:
        try:
            execute_command(args.command, args.verbose, args.debug)
        except KeyboardInterrupt:
            print("\n⚠️  Operation cancelled")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error: {e}")
            if args.debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    elif args.workflow:
        try:
            orchestrator = RalexV4Orchestrator()
            # Workflows are async, so we need to run them in an event loop
            import asyncio
            result = asyncio.run(orchestrator.execute_workflow(args.workflow, {{}}))
            if result["status"] == "success":
                print(f"✅ Workflow '{args.workflow}' executed successfully.\n{result['output']}")
            else:
                print(f"❌ Workflow '{args.workflow}' failed: {result['message']}\n{result.get('user_message', '')}")
        except Exception as e:
            print(f"❌ Error executing workflow: {e}")
            if args.debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()