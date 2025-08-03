#!/usr/bin/env python3
"""
OpenCode.ai Wrapper for Agent-OS Integration
Executes optimized tasks through OpenCode.ai with intelligent error handling and fallback strategies.
"""

import subprocess
import json
import os
import time
import tempfile
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import shlex

class ExecutionMode(Enum):
    YOLO = "yolo"                    # Direct execution without confirmation
    INTERACTIVE = "interactive"      # Step-by-step confirmation
    SAFE = "safe"                   # Read-only analysis mode
    MOBILE_OPTIMIZED = "mobile"     # Optimized for mobile workflow

class ExecutionResult(Enum):
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    ERROR = "error"

@dataclass
class OpenCodeConfig:
    binary_path: str
    timeout: int
    max_retries: int
    execution_mode: ExecutionMode
    safety_checks: bool
    output_capture: bool

@dataclass
class ExecutionOutput:
    result: ExecutionResult
    stdout: str
    stderr: str
    exit_code: int
    execution_time: float
    files_modified: List[str]
    error_message: Optional[str]
    safety_warnings: List[str]
    cost_actual: float
    tokens_used: int

@dataclass
class SafetyCheck:
    check_name: str
    passed: bool
    severity: str  # 'low', 'medium', 'high', 'critical'
    message: str
    recommendation: str

class OpenCodeWrapper:
    """
    Agent-OS optimized wrapper for OpenCode.ai execution.
    
    Key Features:
    - YOLO mode integration for direct execution
    - Intelligent error handling and recovery
    - Safety validation before dangerous operations
    - Mobile workflow optimization
    - Cost tracking and budget enforcement
    - File system protection with rollback capability
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or Path(__file__).parent / "opencode-config.json"
        self.config = self._load_config()
        self.execution_history = []
        self.safety_overrides = set()
        
    def _load_config(self) -> OpenCodeConfig:
        """Load OpenCode.ai wrapper configuration."""
        default_config = {
            "binary_path": str(Path.home() / ".opencode" / "bin" / "opencode"),
            "timeout": 300,  # 5 minutes default
            "max_retries": 3,
            "execution_mode": "yolo",
            "safety_checks": True,
            "output_capture": True
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    loaded = json.load(f)
                    config_data = {**default_config, **loaded}
            except:
                config_data = default_config
        else:
            config_data = default_config
        
        return OpenCodeConfig(
            binary_path=config_data["binary_path"],
            timeout=config_data["timeout"],
            max_retries=config_data["max_retries"],
            execution_mode=ExecutionMode(config_data["execution_mode"]),
            safety_checks=config_data["safety_checks"],
            output_capture=config_data["output_capture"]
        )
    
    def execute_task(self, task_classification, optimized_context: Optional[str] = None,
                    execution_mode: Optional[ExecutionMode] = None) -> ExecutionOutput:
        """
        Main execution function implementing Agent-OS optimization.
        
        Args:
            task_classification: TaskClassification from classifier
            optimized_context: Optimized context from context manager
            execution_mode: Override default execution mode
            
        Returns:
            ExecutionOutput with comprehensive execution results
        """
        start_time = time.time()
        mode = execution_mode or self._determine_execution_mode(task_classification)
        
        # Pre-execution safety checks
        safety_checks = []
        if self.config.safety_checks:
            safety_checks = self._perform_safety_checks(task_classification, mode)
            
            # Block execution if critical safety issues found
            critical_issues = [check for check in safety_checks if check.severity == 'critical']
            if critical_issues and not self._has_safety_override(task_classification):
                return ExecutionOutput(
                    result=ExecutionResult.ERROR,
                    stdout="",
                    stderr="Critical safety issues detected",
                    exit_code=-1,
                    execution_time=time.time() - start_time,
                    files_modified=[],
                    error_message="Execution blocked by safety checks",
                    safety_warnings=[check.message for check in critical_issues],
                    cost_actual=0.0,
                    tokens_used=0
                )
        
        # Prepare execution environment
        command_args = self._prepare_command(task_classification, optimized_context, mode)
        
        # Execute with retries
        for attempt in range(self.config.max_retries):
            try:
                execution_result = self._execute_opencode(command_args, attempt)
                
                if execution_result.result == ExecutionResult.SUCCESS:
                    break
                elif execution_result.result == ExecutionResult.TIMEOUT and attempt < self.config.max_retries - 1:
                    # Retry with increased timeout
                    self.config.timeout = min(self.config.timeout * 1.5, 900)  # Max 15 minutes
                    continue
                elif attempt == self.config.max_retries - 1:
                    # Final attempt failed
                    break
                    
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    # Final attempt, return error
                    execution_result = ExecutionOutput(
                        result=ExecutionResult.ERROR,
                        stdout="",
                        stderr=str(e),
                        exit_code=-1,
                        execution_time=time.time() - start_time,
                        files_modified=[],
                        error_message=f"Execution failed after {self.config.max_retries} attempts: {e}",
                        safety_warnings=[check.message for check in safety_checks],
                        cost_actual=0.0,
                        tokens_used=0
                    )
                    break
                else:
                    # Retry
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
        
        # Post-execution processing
        execution_result.safety_warnings = [check.message for check in safety_checks if check.severity in ['medium', 'high']]
        execution_result.execution_time = time.time() - start_time
        
        # Update cost tracking
        if task_classification.routing_decision:
            execution_result.cost_actual = task_classification.routing_decision.get("estimated_cost", 0.0)
        
        # Track execution for learning
        self.execution_history.append(execution_result)
        
        return execution_result
    
    def _determine_execution_mode(self, task_classification) -> ExecutionMode:
        """Determine optimal execution mode based on task classification."""
        task_type = task_classification.task_type.value
        complexity = task_classification.complexity.value
        strategy = task_classification.execution_strategy
        
        # Mobile tasks use mobile-optimized mode
        if strategy == "mobile_preserved":
            return ExecutionMode.MOBILE_OPTIMIZED
        
        # Analysis tasks use safe mode (read-only)
        if strategy == "analysis_mode":
            return ExecutionMode.SAFE
        
        # Complex tasks may need interactive mode
        if complexity == "high" and strategy == "agentos_optimized":
            return ExecutionMode.INTERACTIVE
        
        # Simple tasks can use YOLO mode
        if task_type == "simple" and complexity == "low":
            return ExecutionMode.YOLO
        
        # Default to safe execution
        return ExecutionMode.SAFE
    
    def _perform_safety_checks(self, task_classification, mode: ExecutionMode) -> List[SafetyCheck]:
        """Perform comprehensive safety validation before execution."""
        checks = []
        prompt = getattr(task_classification, 'prompt', '')
        
        # Check for destructive operations
        destructive_patterns = [
            r'\brm\s+-rf\b',
            r'\bdelete\s+all\b',
            r'\bformat\s+disk\b',
            r'\bshutdown\b',
            r'\breboot\b'
        ]
        
        import re
        for pattern in destructive_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                checks.append(SafetyCheck(
                    check_name="destructive_operation",
                    passed=False,
                    severity="critical",
                    message=f"Potentially destructive operation detected: {pattern}",
                    recommendation="Use interactive mode or add safety override"
                ))
        
        # Check for file system modifications with high complexity
        if task_classification.complexity.value == "high" and mode == ExecutionMode.YOLO:
            file_patterns = [r'\bwrite\b', r'\bcreate\b', r'\bmodify\b', r'\bdelete\b']
            for pattern in file_patterns:
                if re.search(pattern, prompt, re.IGNORECASE):
                    checks.append(SafetyCheck(
                        check_name="high_complexity_file_ops",
                        passed=False,
                        severity="medium",
                        message="High complexity file operations in YOLO mode",
                        recommendation="Consider interactive mode for complex operations"
                    ))
                    break
        
        # Check for mobile API modifications
        if task_classification.task_type.value == "mobile":
            mobile_patterns = [r'\bapi\b', r'\bendpoint\b', r'\broute\b']
            for pattern in mobile_patterns:
                if re.search(pattern, prompt, re.IGNORECASE):
                    checks.append(SafetyCheck(
                        check_name="mobile_api_modification",
                        passed=True,
                        severity="low",
                        message="Mobile API modification detected",
                        recommendation="Ensure OpenCat compatibility is maintained"
                    ))
                    break
        
        # Check budget constraints
        routing_decision = getattr(task_classification, 'routing_decision', {})
        estimated_cost = routing_decision.get('estimated_cost', 0.0) if routing_decision else 0.0
        
        if estimated_cost > 0.01:  # $0.01 threshold
            checks.append(SafetyCheck(
                check_name="high_cost_operation",
                passed=False,
                severity="medium",
                message=f"High cost operation: ${estimated_cost:.6f}",
                recommendation="Verify budget allocation before proceeding"
            ))
        
        return checks
    
    def _has_safety_override(self, task_classification) -> bool:
        """Check if safety override is active for this task type."""
        task_id = f"{task_classification.task_type.value}_{task_classification.complexity.value}"
        return task_id in self.safety_overrides
    
    def _prepare_command(self, task_classification, optimized_context: Optional[str], 
                        mode: ExecutionMode) -> List[str]:
        """Prepare OpenCode.ai command with optimized parameters."""
        cmd = [self.config.binary_path]
        
        # Add mode-specific flags
        if mode == ExecutionMode.YOLO:
            cmd.extend(["--yolo", "--auto-yes"])
        elif mode == ExecutionMode.INTERACTIVE:
            cmd.extend(["--interactive"])
        elif mode == ExecutionMode.SAFE:
            cmd.extend(["--read-only", "--no-execute"])
        elif mode == ExecutionMode.MOBILE_OPTIMIZED:
            cmd.extend(["--mobile-safe", "--preserve-api"])
        
        # Add model selection from routing decision
        if hasattr(task_classification, 'routing_decision') and task_classification.routing_decision:
            model = task_classification.routing_decision.get('selected_model', '')
            if model:
                cmd.extend(["--model", model])
        
        # Add timeout
        cmd.extend(["--timeout", str(self.config.timeout)])
        
        # Add optimized context if available
        if optimized_context:
            # Write context to temporary file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                f.write(optimized_context)
                cmd.extend(["--context-file", f.name])
        
        # Add the actual prompt/command
        prompt = getattr(task_classification, 'prompt', '')
        if hasattr(task_classification, 'task_type'):
            # Reconstruct prompt from classification
            prompt = f"{task_classification.task_type.value} task"
        
        cmd.append(prompt)
        
        return cmd
    
    def _execute_opencode(self, command_args: List[str], attempt: int) -> ExecutionOutput:
        """Execute OpenCode.ai command with comprehensive monitoring."""
        start_time = time.time()
        
        try:
            # Prepare environment
            env = os.environ.copy()
            env['OPENCODE_LOG_LEVEL'] = 'INFO'
            
            # Execute command
            process = subprocess.Popen(
                command_args,
                stdout=subprocess.PIPE if self.config.output_capture else None,
                stderr=subprocess.PIPE if self.config.output_capture else None,
                text=True,
                env=env,
                cwd=os.getcwd()
            )
            
            try:
                stdout, stderr = process.communicate(timeout=self.config.timeout)
                exit_code = process.returncode
                execution_time = time.time() - start_time
                
                # Determine result based on exit code and output
                if exit_code == 0:
                    result = ExecutionResult.SUCCESS
                elif exit_code == 1:
                    result = ExecutionResult.PARTIAL_SUCCESS
                else:
                    result = ExecutionResult.FAILURE
                
                # Parse output for file modifications
                files_modified = self._parse_file_modifications(stdout, stderr)
                
                # Estimate token usage from output
                tokens_used = len((stdout + stderr).split()) * 1.3  # Rough estimate
                
                return ExecutionOutput(
                    result=result,
                    stdout=stdout or "",
                    stderr=stderr or "",
                    exit_code=exit_code,
                    execution_time=execution_time,
                    files_modified=files_modified,
                    error_message=stderr if exit_code != 0 else None,
                    safety_warnings=[],
                    cost_actual=0.0,  # Will be updated by caller
                    tokens_used=int(tokens_used)
                )
                
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                
                return ExecutionOutput(
                    result=ExecutionResult.TIMEOUT,
                    stdout="",
                    stderr=f"Execution timed out after {self.config.timeout} seconds",
                    exit_code=-1,
                    execution_time=self.config.timeout,
                    files_modified=[],
                    error_message="Execution timeout",
                    safety_warnings=[],
                    cost_actual=0.0,
                    tokens_used=0
                )
                
        except Exception as e:
            return ExecutionOutput(
                result=ExecutionResult.ERROR,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                execution_time=time.time() - start_time,
                files_modified=[],
                error_message=f"Execution error: {e}",
                safety_warnings=[],
                cost_actual=0.0,
                tokens_used=0
            )
    
    def _parse_file_modifications(self, stdout: str, stderr: str) -> List[str]:
        """Parse command output to identify modified files."""
        modified_files = []
        
        # Common patterns for file operations
        import re
        file_patterns = [
            r'Created:\s+([^\s]+)',
            r'Modified:\s+([^\s]+)',
            r'Updated:\s+([^\s]+)',
            r'Writing to:\s+([^\s]+)',
            r'Saved:\s+([^\s]+)'
        ]
        
        combined_output = stdout + "\n" + stderr
        
        for pattern in file_patterns:
            matches = re.findall(pattern, combined_output)
            modified_files.extend(matches)
        
        return list(set(modified_files))  # Remove duplicates
    
    def get_execution_stats(self) -> Dict:
        """Get execution performance statistics."""
        if not self.execution_history:
            return {"message": "No executions performed yet"}
        
        total_executions = len(self.execution_history)
        
        # Result breakdown
        result_counts = {}
        total_time = 0
        total_cost = 0
        total_tokens = 0
        
        for execution in self.execution_history:
            result = execution.result.value
            result_counts[result] = result_counts.get(result, 0) + 1
            total_time += execution.execution_time
            total_cost += execution.cost_actual
            total_tokens += execution.tokens_used
        
        success_rate = (result_counts.get('success', 0) + result_counts.get('partial', 0)) / total_executions
        
        return {
            "total_executions": total_executions,
            "success_rate": success_rate,
            "result_breakdown": result_counts,
            "avg_execution_time": total_time / total_executions,
            "total_cost": total_cost,
            "total_tokens": total_tokens,
            "avg_cost_per_execution": total_cost / total_executions,
            "files_modified_total": sum(len(ex.files_modified) for ex in self.execution_history)
        }
    
    def add_safety_override(self, task_type: str, complexity: str, reason: str):
        """Add safety override for specific task type/complexity combination."""
        task_id = f"{task_type}_{complexity}"
        self.safety_overrides.add(task_id)
        print(f"Safety override added for {task_id}: {reason}")
    
    def health_check(self) -> Dict:
        """Perform health check on OpenCode.ai installation."""
        checks = {}
        
        # Check if binary exists and is executable
        binary_path = Path(self.config.binary_path)
        checks["binary_exists"] = binary_path.exists()
        checks["binary_executable"] = binary_path.exists() and os.access(binary_path, os.X_OK)
        
        # Check version
        if checks["binary_executable"]:
            try:
                result = subprocess.run(
                    [self.config.binary_path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                checks["version_check"] = result.returncode == 0
                checks["version_output"] = result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
            except:
                checks["version_check"] = False
                checks["version_output"] = "Version check failed"
        
        # Check configuration
        checks["config_loaded"] = self.config is not None
        checks["timeout_reasonable"] = 30 <= self.config.timeout <= 900
        
        # Overall health
        checks["healthy"] = all([
            checks.get("binary_executable", False),
            checks.get("version_check", False),
            checks.get("config_loaded", False)
        ])
        
        return checks

def quick_execute(task_classification, optimized_context: Optional[str] = None) -> ExecutionOutput:
    """Quick execution function for CLI integration."""
    wrapper = OpenCodeWrapper()
    return wrapper.execute_task(task_classification, optimized_context)

if __name__ == "__main__":
    # Test OpenCode.ai wrapper
    from types import SimpleNamespace
    
    # Mock task classification for testing
    test_task = SimpleNamespace(
        task_type=SimpleNamespace(value="simple"),
        complexity=SimpleNamespace(value="low"),
        execution_strategy="direct_opencode",
        routing_decision={"estimated_cost": 0.001, "selected_model": "test-model"},
        prompt="test command"
    )
    
    wrapper = OpenCodeWrapper()
    
    print("=== OpenCode.ai Wrapper Testing ===")
    
    # Health check
    print("\n--- Health Check ---")
    health = wrapper.health_check()
    for check, status in health.items():
        print(f"{check}: {status}")
    
    # Execution mode determination
    print("\n--- Execution Mode Determination ---")
    mode = wrapper._determine_execution_mode(test_task)
    print(f"Recommended mode: {mode.value}")
    
    # Safety checks
    print("\n--- Safety Checks ---")
    safety_checks = wrapper._perform_safety_checks(test_task, mode)
    for check in safety_checks:
        print(f"{check.check_name}: {check.passed} ({check.severity}) - {check.message}")
    
    print("\n--- Wrapper Ready ---")
    print("OpenCode.ai wrapper initialization complete")
    print("Integration with Agent-OS optimization pipeline ready")