"""
Enhanced Approval Manager for Frontloading Execution Approvals

This module implements batch approval modes to minimize user interruption
while maintaining security for dangerous operations.
"""

from enum import Enum
from typing import Dict, List, Set
import time


class ApprovalMode(Enum):
    """Different modes for handling execution approvals."""
    INTERACTIVE = "interactive"  # Ask for each dangerous operation (default)
    BATCH_SESSION = "batch_session"  # Approve all operations for current session
    BATCH_SAFE = "batch_safe"  # Auto-approve safe operations, ask for dangerous ones
    BATCH_ALL = "batch_all"  # Approve everything (high trust mode)
    PATTERN_BASED = "pattern_based"  # Pre-approved patterns


class ApprovalManager:
    def __init__(self):
        self.mode = ApprovalMode.INTERACTIVE
        self.session_approvals: Set[str] = set()
        self.approved_patterns: Set[str] = set() 
        self.session_start_time = time.time()
        self.session_timeout = 3600  # 1 hour default
        
        # Trust levels for different operation types
        self.trust_levels = {
            "read_operations": ["read_file", "list_directory", "explain_code"],
            "safe_write_operations": ["write_file", "create_component", "run_tests"],
            "code_operations": ["fix_bug", "review_code", "refactor_code"],
            "dangerous_operations": ["delete_all", "rm -rf", "sudo", "chmod 777"]
        }
    
    def set_approval_mode(self, mode: ApprovalMode, session_timeout: int = 3600):
        """Set the approval mode for the current session."""
        self.mode = mode
        self.session_timeout = session_timeout
        self.session_start_time = time.time()
        
        # Auto-approve safe operations in batch modes
        if mode in [ApprovalMode.BATCH_SESSION, ApprovalMode.BATCH_SAFE, ApprovalMode.BATCH_ALL]:
            self.session_approvals.update(
                self.trust_levels["read_operations"] + 
                self.trust_levels["safe_write_operations"] +
                self.trust_levels["code_operations"]
            )
            
        # Auto-approve dangerous operations in full batch mode
        if mode == ApprovalMode.BATCH_ALL:
            self.session_approvals.update(self.trust_levels["dangerous_operations"])
    
    def add_approved_pattern(self, pattern: str):
        """Add a pre-approved operation pattern."""
        self.approved_patterns.add(pattern)
    
    def is_session_expired(self) -> bool:
        """Check if the current approval session has expired."""
        return (time.time() - self.session_start_time) > self.session_timeout
    
    def needs_approval(self, parsed_command: dict) -> tuple[bool, str]:
        """
        Check if a command needs user approval.
        
        Returns:
            tuple: (needs_approval, reason)
        """
        intent = parsed_command.get("intent", "unknown")
        
        # Session expired - reset to interactive mode
        if self.is_session_expired():
            self.mode = ApprovalMode.INTERACTIVE
            self.session_approvals.clear()
        
        # Check approval mode
        if self.mode == ApprovalMode.INTERACTIVE:
            if self._is_dangerous_operation(intent):
                return True, f"Dangerous operation '{intent}' requires confirmation"
                
        elif self.mode == ApprovalMode.BATCH_SAFE:
            if self._is_dangerous_operation(intent):
                return True, f"Dangerous operation '{intent}' requires confirmation even in batch-safe mode"
                
        elif self.mode == ApprovalMode.BATCH_SESSION:
            if intent not in self.session_approvals:
                return True, f"Operation '{intent}' not in session approvals"
                
        elif self.mode == ApprovalMode.BATCH_ALL:
            return False, "All operations approved in batch-all mode"
            
        elif self.mode == ApprovalMode.PATTERN_BASED:
            if not self._matches_approved_pattern(intent):
                return True, f"Operation '{intent}' doesn't match approved patterns"
        
        return False, "Operation approved"
    
    def approve_operation(self, intent: str):
        """Approve a specific operation for the current session."""
        self.session_approvals.add(intent)
    
    def get_approval_summary(self) -> dict:
        """Get a summary of current approval settings."""
        return {
            "mode": self.mode.value,
            "session_approvals": list(self.session_approvals),
            "approved_patterns": list(self.approved_patterns),
            "session_age": time.time() - self.session_start_time,
            "session_timeout": self.session_timeout,
            "session_expired": self.is_session_expired()
        }
    
    def _is_dangerous_operation(self, intent: str) -> bool:
        """Check if an operation is considered dangerous."""
        return intent in self.trust_levels["dangerous_operations"]
    
    def _matches_approved_pattern(self, intent: str) -> bool:
        """Check if an operation matches any approved patterns."""
        return any(pattern in intent for pattern in self.approved_patterns)


def demo_batch_approval():
    """Demonstrate batch approval functionality."""
    manager = ApprovalManager()
    
    # Example: User wants to do a coding session
    print("=== Demo: Batch Approval for Coding Session ===")
    
    # Set batch mode for safe operations
    manager.set_approval_mode(ApprovalMode.BATCH_SAFE, session_timeout=1800)  # 30 minutes
    
    test_commands = [
        {"intent": "read_file", "params": {"file": "main.py"}},
        {"intent": "write_file", "params": {"file": "new_feature.py"}},
        {"intent": "run_tests", "params": {}},
        {"intent": "delete_all", "params": {}},  # This should still require approval
        {"intent": "fix_bug", "params": {"issue": "null pointer"}},
    ]
    
    for cmd in test_commands:
        needs_approval, reason = manager.needs_approval(cmd)
        status = "❌ NEEDS APPROVAL" if needs_approval else "✅ AUTO-APPROVED"
        print(f"{status}: {cmd['intent']} - {reason}")
    
    print(f"\nApproval Summary: {manager.get_approval_summary()}")


if __name__ == "__main__":
    demo_batch_approval()