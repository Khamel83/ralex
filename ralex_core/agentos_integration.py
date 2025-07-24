#!/usr/bin/env python3
"""
AgentOS Integration - Real implementation for Ralex V2
Loads standards, structures prompts for cost optimization
"""
import os
import json
import glob
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class TaskBreakdown:
    """Represents a broken-down task with cost optimization"""
    analysis_prompt: str  # Expensive smart model prompt
    execution_tasks: List[str]  # Cheap model tasks
    estimated_cost: float
    complexity: str

class AgentOSIntegration:
    """Real AgentOS integration for standards and prompt structuring"""
    
    def __init__(self, agent_os_path: str = "agent_os"):
        self.agent_os_path = agent_os_path
        self.standards = {}
        self.instructions = {}
        self.project_info = {}
        self.load_all_agentos_data()
    
    def load_all_agentos_data(self) -> None:
        """Load all AgentOS standards, instructions, and project info"""
        if not os.path.exists(self.agent_os_path):
            print(f"⚠️  AgentOS directory not found at {self.agent_os_path}")
            return
        
        # Load project info
        project_info_path = os.path.join(self.agent_os_path, "project_info.json")
        if os.path.exists(project_info_path):
            with open(project_info_path, 'r') as f:
                self.project_info = json.load(f)
        
        # Load standards
        standards_dir = os.path.join(self.agent_os_path, "standards")
        if os.path.exists(standards_dir):
            for md_file in glob.glob(os.path.join(standards_dir, "*.md")):
                standard_name = os.path.splitext(os.path.basename(md_file))[0]
                with open(md_file, 'r') as f:
                    self.standards[standard_name] = f.read()
        
        # Load instructions  
        instructions_dir = os.path.join(self.agent_os_path, "instructions")
        if os.path.exists(instructions_dir):
            for md_file in glob.glob(os.path.join(instructions_dir, "*.md")):
                instruction_name = os.path.splitext(os.path.basename(md_file))[0]
                with open(md_file, 'r') as f:
                    self.instructions[instruction_name] = f.read()
        
        print(f"✅ Loaded AgentOS data: {len(self.standards)} standards, {len(self.instructions)} instructions")
    
    def get_standards_context(self) -> str:
        """Get formatted standards context for prompts"""
        if not self.standards:
            return ""
        
        context = "## Project Standards (from AgentOS):\n\n"
        for name, content in self.standards.items():
            context += f"### {name.replace('-', ' ').title()} Standards:\n"
            context += f"{content}\n\n"
        
        return context
    
    def get_instructions_context(self) -> str:
        """Get formatted instructions context for prompts"""
        if not self.instructions:
            return ""
        
        context = "## Project Instructions (from AgentOS):\n\n"
        for name, content in self.instructions.items():
            context += f"### {name.replace('-', ' ').title()}:\n"
            context += f"{content}\n\n"
        
        return context
    
    def analyze_task_complexity(self, user_prompt: str) -> Tuple[str, float]:
        """Analyze task complexity for cost optimization"""
        prompt_lower = user_prompt.lower()
        
        # High complexity patterns (need expensive analysis)
        high_complexity_patterns = [
            'architecture', 'design', 'refactor', 'analyze', 'complex',
            'review', 'optimize', 'performance', 'security', 'scalability',
            'multiple', 'entire', 'system', 'structure', 'approach'
        ]
        
        # Medium complexity patterns
        medium_complexity_patterns = [
            'implement', 'create', 'build', 'add feature', 'modify',
            'extend', 'integrate', 'update', 'enhance'
        ]
        
        # Low complexity patterns (can go straight to cheap)
        low_complexity_patterns = [
            'fix', 'typo', 'format', 'comment', 'rename', 'small',
            'simple', 'quick', 'minor', 'style', 'lint'
        ]
        
        high_score = sum(1 for pattern in high_complexity_patterns if pattern in prompt_lower)
        medium_score = sum(1 for pattern in medium_complexity_patterns if pattern in prompt_lower)
        low_score = sum(1 for pattern in low_complexity_patterns if pattern in prompt_lower)
        
        if high_score > 0 or len(user_prompt.split()) > 20:
            return "high", 0.8 + (high_score * 0.1)
        elif medium_score > 0:
            return "medium", 0.5 + (medium_score * 0.1)
        else:
            return "low", 0.2 + (low_score * 0.05)
    
    def structure_smart_prompt(self, user_prompt: str, file_context: Dict[str, str]) -> TaskBreakdown:
        """Structure prompt for cost optimization: expensive analysis + cheap execution"""
        complexity, confidence = self.analyze_task_complexity(user_prompt)
        
        if complexity == "low":
            # Simple task - can go straight to cheap execution
            execution_tasks = [user_prompt]
            analysis_prompt = ""
            estimated_cost = 0.001  # Very cheap
            
        else:
            # Complex task - needs expensive analysis first
            standards_context = self.get_standards_context()
            instructions_context = self.get_instructions_context()
            
            # Build expensive analysis prompt
            analysis_prompt = f"""
You are an expert software architect and code analyst. Analyze the following request and break it down into specific, actionable tasks.

{standards_context}

{instructions_context}

## User Request:
{user_prompt}

## File Context:
{self._format_file_context(file_context)}

## Your Task:
1. ANALYZE the request thoroughly
2. BREAK DOWN into 3-7 specific, clear tasks
3. ORDER tasks logically (dependencies first)
4. SPECIFY exact changes needed for each task
5. IDENTIFY which files need modification
6. INCLUDE testing requirements

## Output Format:
Provide a detailed breakdown like this:

**ANALYSIS:**
[Your thorough analysis of the request, requirements, and approach]

**TASK BREAKDOWN:**
1. [Specific task 1 - be very detailed about what to do]
2. [Specific task 2 - include file names and exact changes]
3. [Specific task 3 - mention testing needs]
[etc...]

**DEPENDENCIES:**
- Task X depends on Task Y
- [List any task dependencies]

**TESTING PLAN:**
- [Specific tests needed]
- [How to verify each task]

Make each task so clear that a junior developer could execute it without questions.
"""

            # Estimate execution tasks (will be filled by analysis response)
            execution_tasks = []  # Will be populated after analysis
            estimated_cost = 0.015 if complexity == "high" else 0.008  # Analysis cost
        
        return TaskBreakdown(
            analysis_prompt=analysis_prompt,
            execution_tasks=execution_tasks,
            estimated_cost=estimated_cost,
            complexity=complexity
        )
    
    def _format_file_context(self, file_context: Dict[str, str]) -> str:
        """Format file context for prompts"""
        if not file_context:
            return "No files in context."
        
        formatted = ""
        for file_path, content in file_context.items():
            formatted += f"### {file_path}:\n```\n{content}\n```\n\n"
        
        return formatted
    
    def parse_task_breakdown(self, analysis_response: str) -> List[str]:
        """Parse the analysis response to extract execution tasks"""
        lines = analysis_response.split('\n')
        tasks = []
        in_task_section = False
        
        for line in lines:
            line = line.strip()
            if "**TASK BREAKDOWN:**" in line or "TASK BREAKDOWN:" in line:
                in_task_section = True
                continue
            elif line.startswith("**") and in_task_section:
                # End of task section
                break
            elif in_task_section and line:
                # Extract task (remove numbering)
                if line[0].isdigit() and '.' in line:
                    task = line.split('.', 1)[1].strip()
                    if task and not task.startswith('['):  # Skip template examples
                        tasks.append(task)
        
        return tasks
    
    def create_execution_prompt(self, task: str, file_context: Dict[str, str], 
                              analysis_context: str = "") -> str:
        """Create a focused execution prompt for cheap models"""
        standards_summary = self._get_standards_summary()
        
        execution_prompt = f"""
You are an expert programmer. Execute this specific task following project standards.

## Standards Summary:
{standards_summary}

## Task to Execute:
{task}

## Previous Analysis Context:
{analysis_context[:500] if analysis_context else "None"}

## File Context:
{self._format_file_context(file_context)}

## Instructions:
1. Follow the project standards exactly
2. Focus ONLY on this specific task
3. Provide complete, working code
4. Use the exact format for file modifications:
   ```filename.py
   [complete file content]
   ```
5. Be precise and efficient

Execute the task now.
"""
        
        return execution_prompt
    
    def _get_standards_summary(self) -> str:
        """Get a condensed summary of standards for execution prompts"""
        if not self.standards:
            return "No specific standards loaded."
        
        summary = ""
        if "python" in self.standards:
            summary += "Python: Use type hints, PEP 8, docstrings, f-strings, proper error handling. "
        if "git-workflow" in self.standards:
            summary += "Git: Atomic commits, descriptive messages. "
        
        return summary or "Follow general best practices."
    
    def get_slash_commands(self) -> Dict[str, str]:
        """Return available slash commands"""
        return {
            "/review": "Review code with AgentOS standards",
            "/standards": "Show current AgentOS standards",
            "/instructions": "Show AgentOS instructions", 
            "/breakdown": "Break down complex task into cheap execution steps",
            "/apply-standards": "Apply AgentOS standards to current context",
            "/reload": "Reload AgentOS data from disk",
            "/help": "Show available commands and usage"
        }
    
    def handle_slash_command(self, command: str, args: str = "") -> str:
        """Handle slash command execution"""
        if command == "/standards":
            if not self.standards:
                return "No AgentOS standards loaded."
            result = "## Current AgentOS Standards:\n\n"
            for name, content in self.standards.items():
                result += f"### {name}:\n{content[:200]}...\n\n"
            return result
        
        elif command == "/instructions":
            if not self.instructions:
                return "No AgentOS instructions loaded."
            result = "## Current AgentOS Instructions:\n\n"
            for name, content in self.instructions.items():
                result += f"### {name}:\n{content[:200]}...\n\n"
            return result
        
        elif command == "/reload":
            self.load_all_agentos_data()
            return "✅ AgentOS data reloaded from disk."
        
        elif command == "/review":
            return self._create_review_prompt(args)
        
        elif command == "/breakdown":
            if not args:
                return "Usage: /breakdown <task description>"
            return self._create_breakdown_preview(args)
        
        elif command == "/help":
            result = "## AgentOS Slash Commands:\n\n"
            for cmd, desc in self.get_slash_commands().items():
                result += f"**{cmd}**: {desc}\n"
            result += "\n## Usage Examples:\n"
            result += "- `/review myfile.py` - Review code against standards\n"
            result += "- `/breakdown refactor user authentication` - Preview task breakdown\n"
            result += "- `/standards` - Show all project standards\n"
            return result
        
        else:
            available = ", ".join(self.get_slash_commands().keys())
            return f"Unknown command '{command}'. Available: {available}"
    
    def _create_review_prompt(self, file_path: str = "") -> str:
        """Create a code review prompt with AgentOS standards"""
        if not file_path:
            return "Usage: /review <file_path>"
        
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        try:
            with open(file_path, 'r') as f:
                file_content = f.read()
        except Exception as e:
            return f"Error reading file: {e}"
        
        standards_context = self.get_standards_context()
        
        review_prompt = f"""
Perform a comprehensive code review of the following file against our AgentOS standards.

{standards_context}

## File to Review: {file_path}
```
{file_content}
```

## Review Requirements:
1. Check compliance with all project standards
2. Identify potential bugs or issues
3. Suggest improvements for readability and maintainability
4. Verify proper error handling and type hints
5. Check for security concerns
6. Suggest optimizations if applicable

## Output Format:
**OVERALL ASSESSMENT:** [Brief summary]

**STANDARDS COMPLIANCE:**
- ✅ What follows standards well
- ❌ What violates standards

**ISSUES FOUND:**
1. [Issue description with line number if applicable]
2. [Another issue]

**RECOMMENDATIONS:**
1. [Specific improvement suggestion]
2. [Another recommendation]

**PRIORITY:** [High/Medium/Low based on issues found]
"""
        
        return review_prompt
    
    def _create_breakdown_preview(self, task_description: str) -> str:
        """Preview how a task would be broken down"""
        complexity, confidence = self.analyze_task_complexity(task_description)
        
        result = f"## Task Breakdown Preview\n\n"
        result += f"**Task**: {task_description}\n"
        result += f"**Complexity**: {complexity} (confidence: {confidence:.2f})\n\n"
        
        if complexity == "low":
            result += "**Strategy**: Direct execution with cheap model\n"
            result += f"**Estimated Cost**: ~$0.001\n"
            result += "**Process**: Single step execution\n"
        else:
            result += "**Strategy**: Analysis first (smart model), then execution (cheap models)\n"
            result += f"**Estimated Cost**: ~$0.01-0.02 for analysis + $0.001-0.005 per execution task\n"
            result += "**Process**:\n"
            result += "1. 💰 **Analysis Phase** (smart model): Break down requirements, identify dependencies\n"
            result += "2. 💸 **Execution Phase** (cheap models): Execute each specific task\n"
            result += "\n**Expected Tasks**: 3-7 specific implementation tasks\n"
        
        result += f"\n💡 **Tip**: This analysis helps optimize costs by using expensive models only for planning."
        
        return result