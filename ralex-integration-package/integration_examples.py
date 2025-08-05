#!/usr/bin/env python3
"""
Integration Examples - Shows how to integrate Agent OS with Ralex
These examples demonstrate the expected integration patterns.
"""

import asyncio
from agent_os_bridge import AgentOSBridge, TaskRequest
from context_analyzer import AgentOSContextAnalyzer
from methodology_engine import MethodologyEngine
from pattern_manager import PatternManager

class RalexAgentOSIntegration:
    """Example of how Ralex would integrate with Agent OS"""
    
    def __init__(self):
        self.bridge = AgentOSBridge()
        self.is_agent_os_project = self.bridge.is_agent_os_project()
        
    async def handle_user_request(self, user_input: str) -> dict:
        """Main entry point for user requests"""
        
        # Check for lifecycle commands first
        if user_input.lower() in ["start-project", "start project"]:
            return await self.handle_lifecycle_command("start-project")
        elif user_input.lower() in ["resume-project", "resume project", "resume"]:
            return await self.handle_lifecycle_command("resume-project")
        elif user_input.lower() in ["end-project", "end project", "finish"]:
            return await self.handle_lifecycle_command("end-project")
        
        # Handle regular task requests
        return await self.handle_task_request(user_input)
    
    async def handle_lifecycle_command(self, command: str) -> dict:
        """Handle project lifecycle commands"""
        
        if not self.is_agent_os_project:
            return {
                "type": "info",
                "message": "This doesn't appear to be an Agent OS project. Using standard Ralex functionality.",
                "action": "standard_processing"
            }
        
        result = self.bridge.execute_project_lifecycle_command(command)
        
        if command == "start-project":
            return {
                "type": "workflow_executed",
                "workflow": "start-project",
                "message": "Project analysis complete. Development environment ready.",
                "context_analyzed": result.get("context_analyzed", False),
                "next_steps": result.get("next_steps", []),
                "action": "ready_for_development"
            }
        
        elif command == "resume-project":
            return {
                "type": "workflow_executed", 
                "workflow": "resume-project",
                "message": f"Project context restored. Next task: {result.get('next_task', 'No active tasks')}",
                "current_spec": result.get("current_spec"),
                "recommended_action": result.get("recommended_action"),
                "action": "continue_development"
            }
        
        elif command == "end-project":
            return {
                "type": "workflow_executed",
                "workflow": "end-project", 
                "message": "Project completion workflow initiated.",
                "tasks_completed": result.get("tasks_completed", 0),
                "next_steps": result.get("next_steps", []),
                "action": "project_finalization"
            }
        
        return {"type": "error", "message": f"Unknown lifecycle command: {command}"}
    
    async def handle_task_request(self, user_input: str) -> dict:
        """Handle regular task requests with Agent OS optimization"""
        
        task_request = TaskRequest(description=user_input)
        
        if self.is_agent_os_project:
            # Apply Agent OS methodology
            plan = self.bridge.analyze_task_request(task_request)
            
            return {
                "type": "task_planned",
                "original_request": user_input,
                "methodology": plan.methodology,
                "complexity": plan.estimated_complexity,
                "phases": plan.phases,
                "patterns_available": plan.patterns_available,
                "model_recommendations": plan.model_recommendations,
                "action": "execute_optimized_plan"
            }
        else:
            # Standard Ralex processing
            return {
                "type": "standard_task",
                "original_request": user_input,
                "action": "execute_standard_processing"
            }

# Example Usage Scenarios

async def example_project_start():
    """Example: Starting a new project"""
    
    integration = RalexAgentOSIntegration()
    
    print("=== Example: Project Start ===")
    result = await integration.handle_user_request("start-project")
    print(f"Result: {result}")
    
    return result

async def example_task_breakdown():
    """Example: Complex task with methodology application"""
    
    integration = RalexAgentOSIntegration()
    
    print("\n=== Example: Task Breakdown ===")
    result = await integration.handle_user_request("implement user authentication system")
    print(f"Result: {result}")
    
    if result["type"] == "task_planned":
        print(f"Methodology: {result['methodology']}")
        print(f"Complexity: {result['complexity']}")
        print(f"Number of phases: {len(result['phases'])}")
        print(f"Patterns available: {result['patterns_available']}")
    
    return result

async def example_pattern_reuse():
    """Example: Task that matches existing patterns"""
    
    # First, let's simulate saving a successful pattern
    pattern_manager = PatternManager()
    
    # Simulate a successful authentication implementation
    success_metrics = {
        "success": True,
        "actual_time": "45 minutes",
        "success_factors": ["good planning", "pattern reuse", "systematic testing"],
        "pitfalls": ["initially forgot password hashing"]
    }
    
    phases = [
        {"name": "planning", "description": "Plan authentication system"},
        {"name": "implementation", "description": "Implement auth components", 
         "micro_tasks": ["user model", "password hashing", "login endpoint", "middleware"]},
        {"name": "review", "description": "Test and validate"}
    ]
    
    pattern_id = pattern_manager.save_successful_pattern(
        "implement user authentication",
        "three-phase",
        phases,
        success_metrics
    )
    
    print(f"\n=== Example: Pattern Reuse ===")
    print(f"Saved pattern: {pattern_id}")
    
    # Now test pattern matching
    matches = pattern_manager.find_matching_patterns("add user login functionality")
    print(f"Found {len(matches)} matching patterns")
    
    for match in matches:
        print(f"- {match['name']} (confidence: {match['confidence']:.2f})")
    
    return matches

async def example_context_analysis():
    """Example: Context analysis of current project"""
    
    analyzer = AgentOSContextAnalyzer()
    context = analyzer.get_full_context()
    
    print("\n=== Example: Context Analysis ===")
    print(f"Agent OS detected: {context['agent_os_structure']['has_agent_os']}")
    print(f"Git repo: {context['git_context']['is_git_repo']}")
    print(f"Current branch: {context['git_context']['current_branch']}")
    print(f"Project size: {context['project_state']['estimated_size']}")
    print(f"Languages detected: {context['development_context']['likely_languages']}")
    
    if context['current_spec']:
        print(f"Current spec: {context['current_spec']['name']}")
        print(f"Next task: {context['next_task']}")
    
    return context

# Ralex Integration Points

class RalexCommandHandler:
    """Example of how Ralex would handle commands with Agent OS integration"""
    
    def __init__(self):
        self.integration = RalexAgentOSIntegration()
    
    async def process_command(self, command: str, args: list = None) -> str:
        """Process a command with Agent OS awareness"""
        
        # Route through Agent OS integration
        result = await self.integration.handle_user_request(command)
        
        if result["action"] == "execute_optimized_plan":
            return await self.execute_optimized_plan(result)
        elif result["action"] == "ready_for_development":
            return self.format_project_ready_response(result)
        elif result["action"] == "continue_development":
            return self.format_resume_response(result)
        elif result["action"] == "project_finalization":
            return self.format_completion_response(result)
        else:
            return await self.execute_standard_processing(command)
    
    async def execute_optimized_plan(self, plan_result: dict) -> str:
        """Execute a task using Agent OS methodology"""
        
        methodology = plan_result["methodology"]
        phases = plan_result["phases"]
        
        response = f"Using {methodology} methodology for this task.\n\n"
        
        for i, phase in enumerate(phases, 1):
            response += f"Phase {i}: {phase['name']}\n"
            response += f"Focus: {phase['focus']}\n"
            response += f"Estimated time: {phase['estimated_time']}\n"
            
            # In real implementation, this would execute the phase
            response += f"[Phase {i} would be executed here]\n\n"
        
        # In real implementation, pattern learning would happen here
        response += "Task completed successfully. Pattern saved for future reuse."
        
        return response
    
    def format_project_ready_response(self, result: dict) -> str:
        """Format response for project start completion"""
        
        response = "🚀 Project analysis complete!\n\n"
        response += f"Agent OS project detected: {'Yes' if result.get('context_analyzed') else 'No'}\n"
        
        if result.get("next_steps"):
            response += "\nNext steps:\n"
            for step in result["next_steps"]:
                response += f"• {step}\n"
        
        response += "\nReady for development! Just describe what you want to build."
        
        return response
    
    def format_resume_response(self, result: dict) -> str:
        """Format response for project resume"""
        
        response = "🔄 Project context restored!\n\n"
        
        if result.get("current_spec"):
            response += f"Current spec: {result['current_spec']}\n"
        
        if result.get("recommended_action"):
            response += f"Next: {result['recommended_action']}\n"
        
        response += "\nReady to continue development!"
        
        return response
    
    def format_completion_response(self, result: dict) -> str:
        """Format response for project completion"""
        
        response = "🏁 Project completion initiated!\n\n"
        response += f"Tasks completed: {result.get('tasks_completed', 0)}\n\n"
        
        if result.get("next_steps"):
            response += "Completion checklist:\n"
            for step in result["next_steps"]:
                response += f"• {step}\n"
        
        return response
    
    async def execute_standard_processing(self, command: str) -> str:
        """Standard Ralex processing for non-Agent OS projects"""
        
        return f"Processing: {command}\n[Standard Ralex functionality would execute here]"

# Example of complete integration flow
async def complete_integration_example():
    """Example showing complete integration flow"""
    
    print("=== Complete Integration Example ===")
    
    handler = RalexCommandHandler()
    
    # 1. Start project
    print("\n1. Starting project...")
    start_result = await handler.process_command("start-project")
    print(start_result)
    
    # 2. Execute a task
    print("\n2. Executing task...")
    task_result = await handler.process_command("implement user registration")
    print(task_result)
    
    # 3. Resume later
    print("\n3. Resuming project...")
    resume_result = await handler.process_command("resume-project")
    print(resume_result)
    
    # 4. End project
    print("\n4. Ending project...")
    end_result = await handler.process_command("end-project")
    print(end_result)

# Run examples
if __name__ == "__main__":
    async def run_all_examples():
        await example_project_start()
        await example_task_breakdown()
        await example_pattern_reuse()
        await example_context_analysis()
        await complete_integration_example()
    
    asyncio.run(run_all_examples())