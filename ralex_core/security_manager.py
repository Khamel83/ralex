"""
Security Manager - Stub Implementation

This is a stub implementation that will be fully developed in Task 3.3.
For now, it provides the interface needed by the orchestrator.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class SecurityResult:
    """Result of security validation"""
    is_safe: bool
    reason: str = ""
    issues: List[str] = None
    
    def __post_init__(self):
        if self.issues is None:
            self.issues = []


class SecurityManager:
    """Stub implementation of security manager"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.logger = logging.getLogger(__name__)
        
        # Basic dangerous command patterns
        self.dangerous_patterns = [
            "rm -rf", "sudo rm", "format", "fdisk", "dd if=", 
            "shutdown", "reboot", "chmod 777"
        ]
        
    async def initialize(self):
        """Initialize security manager"""
        self.logger.info("Security manager initialized (stub)")
        
    async def validate_command(self, parsed_command, user_context: Dict[str, Any]) -> SecurityResult:
        """Validate command security - stub implementation"""
        command_text = parsed_command.original_text.lower()
        
        # Check for dangerous patterns
        for pattern in self.dangerous_patterns:
            if pattern in command_text:
                return SecurityResult(
                    is_safe=False,
                    reason=f"Command contains dangerous pattern: {pattern}",
                    issues=[f"Blocked pattern: {pattern}"]
                )
        
        return SecurityResult(is_safe=True, reason="Command passed basic security check")
        
    async def health_check(self) -> Dict[str, Any]:
        """Health check for security manager"""
        return {"status": "healthy", "message": "Security manager operational (stub)"}
        
    async def shutdown(self):
        """Shutdown security manager"""
        pass