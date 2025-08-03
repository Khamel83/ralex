#!/usr/bin/env python3
"""
Universal Logger for AI Operations
Works with any tool: Ralex, OpenCode.ai, Claude Code, etc.
Logs everything with unique IDs and metadata for future analysis.
"""

import json
import uuid
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import os

class UniversalLogger:
    """
    Lightweight logger that tracks all AI operations with unique IDs.
    Designed to be cheap, fast, and work regardless of tool choice.
    """
    
    def __init__(self, log_dir: str = ".ai-logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.session_id = str(uuid.uuid4())[:8]
        self.operation_counter = 0
        
    def log_operation(self, 
                     operation_type: str,
                     prompt: str = "",
                     response: str = "",
                     model: str = "",
                     cost: float = 0.0,
                     metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Log any AI operation with unique ID and full metadata.
        Returns the unique operation ID for reference.
        """
        
        # Generate unique operation ID
        self.operation_counter += 1
        operation_id = f"{self.session_id}-{self.operation_counter:04d}"
        
        # Create comprehensive log entry
        log_entry = {
            "operation_id": operation_id,
            "session_id": self.session_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "unix_timestamp": int(time.time()),
            "operation_type": operation_type,  # "chat", "edit", "execute", "search", etc.
            "model": model,
            "cost": cost,
            "prompt_length": len(prompt),
            "response_length": len(response),
            "project_path": os.getcwd(),
            "metadata": metadata or {}
        }
        
        # Add tool detection
        log_entry["detected_tool"] = self._detect_current_tool()
        
        # Save main log entry (cheap, just metadata)
        log_file = self.log_dir / f"operations-{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Save full content separately (expensive, but detailed)
        if prompt or response:
            content_file = self.log_dir / f"content-{operation_id}.json"
            content_data = {
                "operation_id": operation_id,
                "prompt": prompt,
                "response": response,
                "created_at": log_entry["timestamp"]
            }
            with open(content_file, "w") as f:
                json.dump(content_data, f, indent=2)
        
        return operation_id
    
    def log_cost(self, operation_id: str, actual_cost: float, estimated_cost: float = None):
        """Update cost information for an operation."""
        cost_file = self.log_dir / "costs.jsonl"
        cost_entry = {
            "operation_id": operation_id,
            "actual_cost": actual_cost,
            "estimated_cost": estimated_cost,
            "updated_at": datetime.utcnow().isoformat() + "Z"
        }
        with open(cost_file, "a") as f:
            f.write(json.dumps(cost_entry) + "\n")
    
    def log_pattern(self, pattern_type: str, pattern_data: Dict[str, Any], success: bool = True):
        """Log successful patterns for future reuse."""
        pattern_id = str(uuid.uuid4())[:8]
        pattern_file = self.log_dir / "patterns.jsonl"
        pattern_entry = {
            "pattern_id": pattern_id,
            "pattern_type": pattern_type,  # "code_generation", "bug_fix", "architecture", etc.
            "success": success,
            "pattern_data": pattern_data,
            "logged_at": datetime.utcnow().isoformat() + "Z"
        }
        with open(pattern_file, "a") as f:
            f.write(json.dumps(pattern_entry) + "\n")
        return pattern_id
    
    def _detect_current_tool(self) -> str:
        """Detect which AI tool is currently being used."""
        # Check environment variables and process names
        if os.getenv("OPENCODE_SESSION"):
            return "opencode"
        elif os.getenv("CLAUDE_CODE_SESSION"):
            return "claude-code"
        elif "cursor" in os.getenv("TERM_PROGRAM", "").lower():
            return "cursor"
        elif "ralex" in os.getcwd().lower():
            return "ralex"
        else:
            return "unknown"
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of current session for analysis."""
        log_files = list(self.log_dir.glob(f"operations-*.jsonl"))
        total_operations = 0
        total_cost = 0.0
        
        for log_file in log_files:
            with open(log_file) as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        if entry.get("session_id") == self.session_id:
                            total_operations += 1
                            total_cost += entry.get("cost", 0.0)
        
        return {
            "session_id": self.session_id,
            "total_operations": total_operations,
            "total_cost": total_cost,
            "log_directory": str(self.log_dir)
        }

# Global logger instance
_logger = None

def get_logger() -> UniversalLogger:
    """Get or create global logger instance."""
    global _logger
    if _logger is None:
        _logger = UniversalLogger()
    return _logger

def log_ai_operation(operation_type: str, prompt: str = "", response: str = "", 
                    model: str = "", cost: float = 0.0, **metadata) -> str:
    """Convenience function for logging AI operations."""
    return get_logger().log_operation(operation_type, prompt, response, model, cost, metadata)

def log_pattern(pattern_type: str, **pattern_data) -> str:
    """Convenience function for logging successful patterns."""
    return get_logger().log_pattern(pattern_type, pattern_data)

# Usage examples:
if __name__ == "__main__":
    # Example usage
    logger = UniversalLogger()
    
    # Log a chat operation
    op_id = logger.log_operation(
        operation_type="chat",
        prompt="Create a Python function that calculates fibonacci",
        response="def fibonacci(n): ...",
        model="claude-3.5-sonnet",
        cost=0.05,
        metadata={"file_context": True, "complexity": "simple"}
    )
    
    # Log a pattern for reuse
    pattern_id = logger.log_pattern(
        pattern_type="fibonacci_implementation",
        language="python",
        complexity="simple",
        tokens_used=150,
        success=True
    )
    
    print(f"Logged operation: {op_id}")
    print(f"Logged pattern: {pattern_id}")
    print(f"Session summary: {logger.get_session_summary()}")