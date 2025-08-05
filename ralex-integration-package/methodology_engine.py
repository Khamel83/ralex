#!/usr/bin/env python3
"""
Methodology Engine - Applies Agent OS task breakdown methodology
This module implements the systematic task breakdown approach from Agent OS.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import re

@dataclass
class TaskBreakdown:
    """Represents a broken-down task"""
    original_task: str
    methodology: str
    phases: List[Dict[str, Any]]
    micro_tasks: List[str]
    estimated_time: str
    success_criteria: List[str]

class MethodologyEngine:
    """Applies Agent OS methodology to task breakdown"""
    
    def __init__(self, templates_path: Optional[str] = None):
        self.templates_path = Path(templates_path) if templates_path else None
        
    def apply_three_phase_methodology(self, task_description: str, context: Dict[str, Any] = None) -> TaskBreakdown:
        """Apply the three-phase methodology to a task"""
        
        # Analyze task for complexity and components
        task_analysis = self._analyze_task(task_description, context)
        
        # Create three phases
        phases = [
            self._create_planning_phase(task_description, task_analysis),
            self._create_implementation_phase(task_description, task_analysis),
            self._create_review_phase(task_description, task_analysis)
        ]
        
        # Extract micro-tasks from implementation phase
        micro_tasks = phases[1].get("micro_tasks", [])
        
        # Estimate total time
        total_time = self._estimate_total_time(phases)
        
        # Define success criteria
        success_criteria = self._define_success_criteria(task_description, task_analysis)
        
        return TaskBreakdown(
            original_task=task_description,
            methodology="three-phase",
            phases=phases,
            micro_tasks=micro_tasks,
            estimated_time=total_time,
            success_criteria=success_criteria
        )
    
    def apply_simple_methodology(self, task_description: str, context: Dict[str, Any] = None) -> TaskBreakdown:
        """Apply simple methodology for straightforward tasks"""
        
        task_analysis = self._analyze_task(task_description, context)
        
        phases = [
            {
                "name": "implementation",
                "description": f"Implement: {task_description}",
                "focus": "direct implementation",
                "estimated_time": "15-30 minutes",
                "activities": [
                    "Understand requirements clearly",
                    "Implement solution directly",
                    "Test basic functionality",
                    "Verify meets requirements"
                ],
                "deliverables": ["working solution"],
                "success_criteria": ["solution works as expected", "requirements met"]
            }
        ]
        
        return TaskBreakdown(
            original_task=task_description,
            methodology="simple",
            phases=phases,
            micro_tasks=[task_description],
            estimated_time="15-30 minutes",
            success_criteria=["task completed successfully", "solution tested and working"]
        )
    
    def apply_pattern_reuse_methodology(self, task_description: str, pattern: Dict[str, Any], context: Dict[str, Any] = None) -> TaskBreakdown:
        """Apply pattern reuse methodology when similar work exists"""
        
        phases = [
            {
                "name": "pattern-adaptation",
                "description": f"Adapt pattern '{pattern.get('name', 'unknown')}' for: {task_description}",
                "focus": "customize existing solution",
                "estimated_time": "10-20 minutes",
                "activities": [
                    f"Review pattern: {pattern.get('name', 'unknown')}",
                    "Identify customization points",
                    "Adapt pattern to current requirements",
                    "Test adapted solution",
                    "Update pattern if improvements found"
                ],
                "deliverables": ["customized solution based on proven pattern"],
                "pattern_used": pattern.get("name", "unknown"),
                "pattern_confidence": pattern.get("confidence", 0.0)
            }
        ]
        
        return TaskBreakdown(
            original_task=task_description,
            methodology="pattern-reuse",
            phases=phases,
            micro_tasks=[f"Adapt {pattern.get('name', 'pattern')} for current use"],
            estimated_time="10-20 minutes",
            success_criteria=["pattern successfully adapted", "solution works as expected", "pattern updated if needed"]
        )
    
    def _analyze_task(self, task_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze task to understand its components and complexity"""
        
        analysis = {
            "complexity": "medium",
            "components": [],
            "task_type": "general",
            "integration_points": [],
            "dependencies": [],
            "risk_factors": []
        }
        
        # Basic task type detection
        task_lower = task_description.lower()
        
        # Detect task types
        if any(word in task_lower for word in ["api", "endpoint", "route"]):
            analysis["task_type"] = "api_development"
            analysis["components"] = ["endpoint", "validation", "response_format", "error_handling"]
        elif any(word in task_lower for word in ["database", "schema", "model", "table"]):
            analysis["task_type"] = "database_work"
            analysis["components"] = ["schema_design", "migrations", "relationships", "constraints"]
        elif any(word in task_lower for word in ["auth", "login", "user", "authentication"]):
            analysis["task_type"] = "authentication"
            analysis["components"] = ["user_model", "password_handling", "session_management", "security"]
        elif any(word in task_lower for word in ["ui", "component", "interface", "frontend"]):
            analysis["task_type"] = "frontend_development"
            analysis["components"] = ["component_structure", "styling", "interactivity", "responsiveness"]
        elif any(word in task_lower for word in ["test", "testing", "spec"]):
            analysis["task_type"] = "testing"
            analysis["components"] = ["test_cases", "test_data", "assertions", "coverage"]
        
        # Detect complexity indicators
        complexity_indicators = {
            "simple": ["fix", "update", "change", "add single", "remove", "small"],
            "complex": ["complete", "entire", "system", "multiple", "integrate", "comprehensive", "full"]
        }
        
        for complexity, indicators in complexity_indicators.items():
            if any(indicator in task_lower for indicator in indicators):
                analysis["complexity"] = complexity
                break
        
        # Detect integration points
        if context and context.get("agent_os_structure", {}).get("has_agent_os"):
            analysis["integration_points"].append("agent_os_specs")
        
        if any(word in task_lower for word in ["api", "service", "external"]):
            analysis["integration_points"].append("external_service")
        
        if any(word in task_lower for word in ["database", "model", "data"]):
            analysis["integration_points"].append("database")
        
        # Identify potential dependencies
        if "auth" in task_lower and analysis["task_type"] != "authentication":
            analysis["dependencies"].append("authentication_system")
        
        if "database" in task_lower and analysis["task_type"] != "database_work":
            analysis["dependencies"].append("database_schema")
        
        return analysis
    
    def _create_planning_phase(self, task_description: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create planning phase based on task analysis"""
        
        base_activities = [
            "Understand requirements and constraints",
            "Design overall approach and architecture",
            "Identify key components and their relationships",
            "Plan implementation sequence",
            "Define success criteria and testing approach"
        ]
        
        # Add task-type specific planning activities
        task_type = analysis.get("task_type", "general")
        
        if task_type == "api_development":
            base_activities.extend([
                "Design API endpoints and request/response formats",
                "Plan validation and error handling strategy",
                "Consider authentication and authorization requirements"
            ])
        elif task_type == "database_work":
            base_activities.extend([
                "Design database schema and relationships", 
                "Plan migration strategy",
                "Consider indexing and performance implications"
            ])
        elif task_type == "authentication":
            base_activities.extend([
                "Design security model and user flow",
                "Plan password handling and session management",
                "Consider security best practices and compliance"
            ])
        elif task_type == "frontend_development":
            base_activities.extend([
                "Design component structure and user experience",
                "Plan responsive design and accessibility",
                "Consider state management and data flow"
            ])
        
        return {
            "name": "planning",
            "description": f"Plan and design approach for: {task_description}",
            "focus": "architecture and strategy",
            "estimated_time": "20-45 minutes",
            "activities": base_activities,
            "deliverables": [
                "detailed specification",
                "implementation roadmap",
                "component design",
                "testing strategy"
            ],
            "success_criteria": [
                "clear understanding of requirements",
                "comprehensive implementation plan",
                "identified risks and mitigation strategies"
            ]
        }
    
    def _create_implementation_phase(self, task_description: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create implementation phase with micro-tasks"""
        
        components = analysis.get("components", ["main_functionality"])
        task_type = analysis.get("task_type", "general")
        
        # Generate micro-tasks based on components
        micro_tasks = []
        for component in components:
            micro_tasks.append(f"Implement {component.replace('_', ' ')}")
        
        # Add task-type specific micro-tasks
        if task_type == "api_development":
            micro_tasks.extend([
                "Create route handlers",
                "Add request validation",
                "Implement error handling",
                "Add response formatting",
                "Write endpoint tests"
            ])
        elif task_type == "database_work":
            micro_tasks.extend([
                "Create database migration",
                "Define model relationships",
                "Add constraints and validations",
                "Test database operations"
            ])
        elif task_type == "authentication":
            micro_tasks.extend([
                "Create user model",
                "Implement password hashing",
                "Add login/logout functionality",
                "Create session management",
                "Add authentication middleware"
            ])
        elif task_type == "frontend_development":
            micro_tasks.extend([
                "Create basic component structure",
                "Add styling and layout",
                "Implement interactivity",
                "Add responsive design",
                "Test component functionality"
            ])
        
        return {
            "name": "implementation",
            "description": f"Systematic implementation of: {task_description}",
            "focus": "incremental development with testing",
            "estimated_time": "varies by complexity",
            "activities": [
                "Break work into small, testable pieces",
                "Implement one micro-task at a time",
                "Test each piece before moving to next",
                "Integrate components systematically"
            ],
            "micro_tasks": micro_tasks,
            "deliverables": [
                "working code for each component",
                "unit tests for core functionality",
                "integration between components"
            ],
            "success_criteria": [
                "all micro-tasks completed",
                "each component works independently",
                "components integrate properly"
            ]
        }
    
    def _create_review_phase(self, task_description: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create review phase for quality assurance"""
        
        task_type = analysis.get("task_type", "general")
        
        base_activities = [
            "Test complete functionality end-to-end",
            "Verify all requirements are met",
            "Check for edge cases and error conditions",
            "Review code quality and best practices",
            "Update documentation as needed"
        ]
        
        # Add task-type specific review activities
        if task_type == "api_development":
            base_activities.extend([
                "Test API endpoints with various inputs",
                "Verify error handling and status codes",
                "Check authentication and authorization",
                "Validate response formats"
            ])
        elif task_type == "database_work":
            base_activities.extend([
                "Test database operations and constraints",
                "Verify data integrity and relationships", 
                "Check migration rollback capability",
                "Validate performance with sample data"
            ])
        elif task_type == "authentication":
            base_activities.extend([
                "Test complete authentication flow",
                "Verify security measures and password handling",
                "Test session management and logout",
                "Check for security vulnerabilities"
            ])
        elif task_type == "frontend_development":
            base_activities.extend([
                "Test component across different browsers",
                "Verify responsive design on various screen sizes",
                "Check accessibility compliance",
                "Validate user experience flow"
            ])
        
        return {
            "name": "review",
            "description": f"Quality assurance and integration testing for: {task_description}",
            "focus": "validation and quality assurance",
            "estimated_time": "15-30 minutes",
            "activities": base_activities,
            "deliverables": [
                "validated solution meeting all requirements",
                "comprehensive test results",
                "updated documentation",
                "identified improvements for future"
            ],
            "success_criteria": [
                "all tests pass",
                "requirements fully satisfied",
                "no critical issues identified",
                "solution ready for production use"
            ]
        }
    
    def _estimate_total_time(self, phases: List[Dict[str, Any]]) -> str:
        """Estimate total time for all phases"""
        # This is a simple estimation - could be made more sophisticated
        phase_count = len(phases)
        
        if phase_count == 1:
            return "15-30 minutes"
        elif phase_count == 2:
            return "30-60 minutes"
        else:  # 3 phases
            return "45-90 minutes"
    
    def _define_success_criteria(self, task_description: str, analysis: Dict[str, Any]) -> List[str]:
        """Define overall success criteria for the task"""
        
        base_criteria = [
            "task completed as described",
            "solution works reliably",
            "code follows best practices",
            "appropriate tests are in place"
        ]
        
        task_type = analysis.get("task_type", "general")
        
        if task_type == "api_development":
            base_criteria.extend([
                "API endpoints respond correctly",
                "proper error handling implemented",
                "authentication/authorization working"
            ])
        elif task_type == "database_work":
            base_criteria.extend([
                "database operations work correctly",
                "data integrity maintained",
                "migrations can be rolled back safely"
            ])
        elif task_type == "authentication":
            base_criteria.extend([
                "user authentication flow works end-to-end",
                "passwords are properly secured",
                "session management functions correctly"
            ])
        elif task_type == "frontend_development":
            base_criteria.extend([
                "component renders correctly across browsers",
                "responsive design works on various devices",
                "user interactions function as expected"
            ])
        
        return base_criteria

# Example usage
if __name__ == "__main__":
    engine = MethodologyEngine()
    
    # Example three-phase breakdown
    task = "implement user authentication system"
    breakdown = engine.apply_three_phase_methodology(task)
    
    print(f"Task: {breakdown.original_task}")
    print(f"Methodology: {breakdown.methodology}")
    print(f"Estimated time: {breakdown.estimated_time}")
    print(f"Phases: {len(breakdown.phases)}")
    print(f"Micro-tasks: {len(breakdown.micro_tasks)}")
    print(f"Success criteria: {len(breakdown.success_criteria)}")