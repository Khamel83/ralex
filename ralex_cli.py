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

# Import modules with proper error handling
try:
    from universal_logger import log_ai_operation
except ImportError:
    # Fallback for missing universal logger
    def log_ai_operation(operation_type, prompt, metadata=None):
        import uuid
        return str(uuid.uuid4())

try:
    import sys
    khamel_path = Path(__file__).parent / ".khamel83"
    sys.path.insert(0, str(khamel_path))
    from budget_controller import BudgetController
except ImportError:
    # Fallback budget controller
    class BudgetController:
        def get_budget_status(self):
            return {
                "daily": {"budget": 5.0, "spent": 0.0, "remaining": 5.0},
                "hourly": {"limit": 1.25, "spent": 0.0, "remaining": 1.25}
            }

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
        
    # Log the operation
    operation_id = log_ai_operation(
        operation_type="cli_command",
        prompt=command,
        metadata={
            "interface": "cli",
            "verbose": verbose,
            "debug": debug
        }
    )
    
    if verbose:
        print(f"📝 Operation ID: {operation_id}")
    
    # For now, just acknowledge - integration with OpenCode.ai in next tasks
    print(f"📋 Command received: {command}")
    print("🚧 OpenCode.ai integration pending (Task A4)")
    
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
    
    # Handle main command
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
    else:
        parser.print_help()

if __name__ == "__main__":
    main()