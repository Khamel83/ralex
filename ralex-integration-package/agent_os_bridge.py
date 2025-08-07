#!/usr/bin/env python3
"""
Agent OS Bridge - Core integration between Ralex and Agent OS
This is the main interface that Ralex will use to interact with Agent OS projects.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from context_analyzer import AgentOSContextAnalyzer
from methodology_engine import MethodologyEngine
from pattern_manager import PatternManager
from state_manager import StateManager

@dataclass
class TaskRequest:
    """Represents a user's task request"""
    description: str
    context: Optional[Dict] = None
    preferences: Optional[Dict] = None

@dataclass
class TaskPlan:
    """Represents the planned approach for a task"""
    methodology: str  # "three-phase", "simple", "complex"
    phases: List[Dict]
    estimated_complexity: str  # "simple", "medium", "complex"
    patterns_available: List[str]
    model_recommendations: Dict[str, str]

class AgentOSBridge:
    """Main bridge between Ralex and Agent OS functionality"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.context_analyzer = AgentOSContextAnalyzer(project_root)
        self.methodology_engine = MethodologyEngine()
        self.pattern_manager = PatternManager(project_root)
        self.state_manager = StateManager(project_root)
        
    def is_agent_os_project(self) -> bool:
        """Check if current directory is an Agent OS project"""
        agent_os_dir = self.project_root / ".agent-os"
        project_dir = self.project_root / ".project"
        return agent_os_dir.exists() or project_dir.exists()
    
    def analyze_task_request(self, request: TaskRequest) -> TaskPlan:
        """Analyze a task request and create an optimized plan"""
        
        # Get project context
        context = self.context_analyzer.get_full_context()
        
        # Analyze task complexity
        complexity = self._analyze_task_complexity(request.description, context)
        
        # Check for applicable patterns
        patterns = self.pattern_manager.find_matching_patterns(request.description)
        
        # Choose methodology based on complexity and patterns
        methodology = self._choose_methodology(complexity, patterns, context)
        
        # Create phase breakdown
        phases = self._create_phase_breakdown(request.description, methodology, patterns)
        
        # Get model recommendations
        model_recs = self._get_model_recommendations(phases, complexity)
        
        return TaskPlan(
            methodology=methodology,
            phases=phases,
            estimated_complexity=complexity,
            patterns_available=[p["name"] for p in patterns],
            model_recommendations=model_recs
        )
    
    def execute_project_lifecycle_command(self, command: str) -> Dict[str, Any]:
        """Execute project lifecycle commands (start, resume, end) or our new save command"""
        
        if command == "start-project":
            return self._execute_start_project()
        elif command == "resume-project":
            return self._execute_resume_project()
        elif command == "end-project":
            return self._execute_end_project()
        elif command == "save":
            return self.save_context()
        elif command == "resume":
            return self.resume_context()
        else:
            raise ValueError(f"Unknown lifecycle command: {command}")

    def save_context(self) -> Dict[str, Any]:
        """
        Saves the current conversational context and commits it to git.
        This is the core of the `k83 save` command.
        """
        print("Attempting to save context...")
        success, message = self.state_manager.save_state()

        if not success:
            print(f"Failed to save state: {message}")
            return {"status": "failed", "message": message}

        print("Context saved. Proceeding with Git operations...")
        try:
            # Git add
            subprocess.run(["git", "add", "."], cwd=self.project_root, check=True)

            # Git commit
            commit_message = f"feat(k83): Save session context from active tool"
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.project_root, check=True)
            print(f"Committed changes with message: '{commit_message}'")

            # Git push
            subprocess.run(["git", "push"], cwd=self.project_root, check=True)
            print("Pushed changes to remote repository.")
            
            return {"status": "success", "message": "Context saved, committed, and pushed successfully."}

        except subprocess.CalledProcessError as e:
            error_message = f"A Git error occurred: {e}"
            print(error_message)
            return {"status": "git-error", "message": error_message}
        except FileNotFoundError:
            error_message = "Git command not found. Is Git installed and in your PATH?"
            print(error_message)
            return {"status": "git-error", "message": error_message}

    def resume_context(self) -> Dict[str, Any]:
        """
        Resumes a session by launching ccr with the appropriate model and context.
        This is the core of the `k83 resume` command.
        """
        print("Attempting to resume session...")
        context_file = self.project_root / "claude_context.md"
        if not context_file.exists():
            return {"status": "failed", "message": "claude_context.md not found. Please run 'k83 save' first."}

        # Model rotation logic
        model_list = [
            "qwen/qwen3-coder",
            "deepseek/deepseek-chat-v3-0324",
            "google/gemini-2.5-flash-lite",
            "openai/gpt-oss-120b",
            "moonshotai/kimi-k2"
        ]
        state_file = self.project_root / ".ralex_state"
        last_model_index = -1

        if state_file.exists():
            try:
                with open(state_file, "r") as f:
                    last_model = f.read().strip()
                    if last_model in model_list:
                        last_model_index = model_list.index(last_model)
            except Exception as e:
                print(f"Could not read state file: {e}")

        # Get the next model in the list
        next_model_index = (last_model_index + 1) % len(model_list)
        next_model = model_list[next_model_index]

        # Save the new model state
        try:
            with open(state_file, "w") as f:
                f.write(next_model)
        except Exception as e:
            print(f"Could not write to state file: {e}")

        # Launch ccr
        config_file = self.project_root / "ralex-integration-package" / "ccr_config.yaml"
        command = [
            "ccr", "code",
            "--model", f"openrouter/{next_model}",
            "--file", str(context_file),
            "--config", str(config_file)
        ]

        print(f"Launching CCR with model: {next_model}")
        print(f"Command: {' '.join(command)}")

        try:
            # Using os.execvp to replace the current process with ccr
            os.execvp(command[0], command)
            # This part will only be reached if execvp fails
            return {"status": "success", "message": f"Launched ccr with model {next_model}."} 
        except FileNotFoundError:
            error_message = "'ccr' command not found. Is claude-code-router installed and in your PATH?"
            print(error_message)
            return {"status": "ccr-error", "message": error_message}
        except Exception as e:
            error_message = f"Failed to launch ccr: {e}"
            print(error_message)
            return {"status": "ccr-error", "message": error_message}

    def _analyze_task_complexity(self, description: str, context: Dict) -> str:
        """Analyze task complexity based on description and context"""
        
        # Simple heuristics for now - can be enhanced with ML later
        complexity_indicators = {
            "simple": ["fix", "update", "change", "add", "remove", "single"],
            "medium": ["implement", "create", "build", "integrate", "system"],
            "complex": ["architecture", "design", "multiple", "complete", "entire", "comprehensive"]
        }
        
        description_lower = description.lower()
        
        # Check for complex indicators first
        for indicator in complexity_indicators["complex"]:
            if indicator in description_lower:
                return "complex"
        
        # Check for medium indicators
        for indicator in complexity_indicators["medium"]:
            if indicator in description_lower:
                return "medium"
        
        # Default to simple
        return "simple"
    
    def _choose_methodology(self, complexity: str, patterns: List[Dict], context: Dict) -> str:
        """Choose the best methodology for the task"""
        
        # If we have a strong pattern match, use simplified approach
        if patterns and any(p["confidence"] > 0.8 for p in patterns):
            return "pattern-reuse"
        
        # Use three-phase for complex tasks
        if complexity == "complex":
            return "three-phase"
        
        # Use simplified for simple tasks
        if complexity == "simple":
            return "simple"
        
        # Default to three-phase for medium complexity
        return "three-phase"
    
    def _create_phase_breakdown(self, description: str, methodology: str, patterns: List[Dict]) -> List[Dict]:
        """Creates phase breakdown based on methodology"""
        
        if methodology == "pattern-reuse":
            return self._create_pattern_reuse_phases(description, patterns[0])
        elif methodology == "three-phase":
            return self._create_three_phase_breakdown(description)
        elif methodology == "simple":
            return self._create_simple_breakdown(description)
        else:
            return self._create_three_phase_breakdown(description)  # default
    
    def _create_three_phase_breakdown(self, description: str) -> List[Dict]:
        """Create three-phase breakdown"""
        return [
            {
                "name": "planning",
                "description": f"Plan and design approach for: {description}",
                "focus": "architecture and strategy",
                "estimated_time": "15-30 minutes",
                "deliverables": ["detailed specification", "implementation roadmap"]
            },
            {
                "name": "implementation", 
                "description": f"Implement micro-tasks for: {description}",
                "focus": "systematic execution",
                "estimated_time": "varies by complexity",
                "deliverables": ["working code", "tests", "documentation"]
            },
            {
                "name": "review",
                "description": f"Review and integrate: {description}",
                "focus": "quality assurance and integration",
                "estimated_time": "10-20 minutes",
                "deliverables": ["integrated solution", "validation results"]
            }
        ]
    
    def _create_simple_breakdown(self, description: str) -> List[Dict]:
        """Create simple task breakdown"""
        return [
            {
                "name": "implementation",
                "description": f"Implement: {description}",
                "focus": "direct implementation",
                "estimated_time": "5-15 minutes",
                "deliverables": ["working solution"]
            }
        ]
    
    def _create_pattern_reuse_phases(self, description: str, pattern: Dict) -> List[Dict]:
        """Create phases based on pattern reuse"""
        return [
            {
                "name": "pattern-application",
                "description": f"Apply pattern '{pattern['name']}' to: {description}",
                "focus": "adapt existing solution",
                "estimated_time": "5-10 minutes",
                "deliverables": ["customized solution based on pattern"],
                "pattern_used": pattern["name"]
            }
        ]
    
    def _get_model_recommendations(self, phases: List[Dict], complexity: str) -> Dict[str, str]:
        """Get model recommendations for each phase"""
        
        recommendations = {}
        
        for phase in phases:
            phase_name = phase["name"]
            
            if phase_name == "planning":
                recommendations[phase_name] = "smart-model"  # Claude, GPT-4, etc.
            elif phase_name == "implementation":
                if complexity == "simple":
                    recommendations[phase_name] = "efficient-model"  # GPT-3.5, etc.
                else:
                    recommendations[phase_name] = "balanced-model"  # GPT-4 mini, etc.
            elif phase_name == "review":
                recommendations[phase_name] = "balanced-model"
            elif phase_name == "pattern-application":
                recommendations[phase_name] = "efficient-model"
            else:
                recommendations[phase_name] = "balanced-model"  # default
        
        return recommendations
    
    def _execute_start_project(self) -> Dict[str, Any]:
        """Execute start-project workflow"""
        
        context = self.context_analyzer.get_full_context()
        
        # Load start-project template and execute steps
        template_path = self.project_root / "templates/.khamel83/project-lifecycle/start-project.md"
        
        workflow_result = {
            "workflow": "start-project",
            "context_analyzed": True,
            "agent_os_detected": self.is_agent_os_project(),
            "handover_docs_found": bool(context.get("handover_docs")),
            "next_steps": [
                "Review project current state",
                "Set up development environment", 
                "Identify first tasks"
            ]
        }
        
        return workflow_result
    
    def _execute_resume_project(self) -> Dict[str, Any]:
        """Execute resume-project workflow"""
        
        context = self.context_analyzer.get_full_context()
        
        # Find current task status
        current_spec = context.get("current_spec")
        next_task = context.get("next_task", "No active tasks found")
        
        workflow_result = {
            "workflow": "resume-project",
            "current_spec": current_spec,
            "next_task": next_task,
            "git_status": context.get("git_status", {}),
            "environment_status": "needs_verification",
            "recommended_action": f"Continue with: {next_task}"
        }
        
        return workflow_result
    
    def _execute_end_project(self) -> Dict[str, Any]:
        """Execute end-project workflow"""
        
        context = self.context_analyzer.get_full_context()
        
        workflow_result = {
            "workflow": "end-project",
            "tasks_completed": context.get("completed_tasks", 0),
            "handover_docs_needed": True,
            "git_status": context.get("git_status", {}),
            "next_steps": [
                "Generate handover documentation",
                "Clean up repository",
                "Create final commit and push",
                "Archive project properly"
            ]
        }
        
        return workflow_result

# Example usage for Ralex integration
if __name__ == "__main__":
    import sys
    # Example of how Ralex would use this bridge
    bridge = AgentOSBridge()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command in ["start-project", "resume-project", "end-project", "save"]:
            print(f"Executing '{command}' command...")
            result = bridge.execute_project_lifecycle_command(command)
            print(json.dumps(result, indent=2))
        else:
            print(f"Unknown command: {command}")
    elif bridge.is_agent_os_project():
        print("Agent OS project detected! Running standard analysis.")
        # Example task analysis
        task = TaskRequest("implement user authentication system")
        plan = bridge.analyze_task_request(task)
        
        print(f"Methodology: {plan.methodology}")
        print(f"Complexity: {plan.estimated_complexity}")
        print(f"Phases: {len(plan.phases)}")
        print(f"Patterns available: {plan.patterns_available}")
    else:
        print("Not an Agent OS project - using standard Ralex functionality")
