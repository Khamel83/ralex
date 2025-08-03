"""
Enhanced AgentOS Integration for Web Interface

Extends the base AgentOS integration with web-specific features including
session management, file context tracking, and web-optimized prompt formatting.
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

from ralex_core.agentos_integration import AgentOSIntegration, TaskBreakdown


class WebFileContext:
    """Manages file context for web sessions"""

    def __init__(self):
        self.files: Dict[str, Dict[str, Any]] = {}
        self.recent_files: List[str] = []

    def add_file(self, file_path: str, content: str = None, metadata: Dict = None):
        """Add file to context"""
        self.files[file_path] = {
            "content": content,
            "metadata": metadata or {},
            "added_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
        }

        # Update recent files
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)

        # Keep only last 10 files
        self.recent_files = self.recent_files[:10]

    def get_file_context(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get context for specific file"""
        if file_path in self.files:
            self.files[file_path]["last_accessed"] = datetime.now().isoformat()
            return self.files[file_path]
        return None

    def get_context_summary(self) -> str:
        """Get summary of current file context"""
        if not self.files:
            return "No files in context."

        summary = f"Files in context ({len(self.files)}):\n"
        for file_path in self.recent_files[:5]:  # Show 5 most recent
            if file_path in self.files:
                metadata = self.files[file_path]["metadata"]
                file_type = metadata.get("type", "unknown")
                summary += f"- {file_path} ({file_type})\n"

        if len(self.files) > 5:
            summary += f"... and {len(self.files) - 5} more files\n"

        return summary


class AgentOSWebIntegration(AgentOSIntegration):
    """Enhanced AgentOS integration for web interface"""

    def __init__(self, agent_os_path: str = "agent_os"):
        super().__init__(agent_os_path)
        self.web_standards = self.load_web_standards()
        self.session_contexts: Dict[str, WebFileContext] = {}

    def load_web_standards(self) -> Dict[str, str]:
        """Load web-specific standards and guidelines"""
        return {
            "response_format": """
For web responses:
- Use clear, formatted code blocks with language specification
- Provide concise explanations before code
- Include error handling and edge cases
- Specify full file paths when modifying files
- Keep responses focused and actionable
""",
            "code_quality": """
Code quality standards:
- Follow existing project patterns and conventions
- Include appropriate comments for complex logic
- Use descriptive variable and function names
- Follow language-specific best practices
- Consider performance and maintainability
""",
            "file_operations": """
File operation guidelines:
- Always specify complete file paths
- Show both old and new code when making changes
- Explain the purpose of each change
- Consider dependencies and imports
- Test changes before committing
""",
        }

    def get_session_context(self, session_id: str) -> WebFileContext:
        """Get or create file context for session"""
        if session_id not in self.session_contexts:
            self.session_contexts[session_id] = WebFileContext()
        return self.session_contexts[session_id]

    def add_file_to_session(
        self,
        session_id: str,
        file_path: str,
        content: str = None,
        metadata: Dict = None,
    ):
        """Add file to session context"""
        context = self.get_session_context(session_id)
        context.add_file(file_path, content, metadata)

    def extract_file_references(self, user_message: str) -> List[str]:
        """Extract file references from user message"""
        # Simple heuristic - look for file extensions and paths
        import re

        # Common file patterns
        file_patterns = [
            r"[a-zA-Z0-9_/.-]+\.[a-zA-Z]{1,4}",  # file.ext
            r"[a-zA-Z0-9_/-]+/[a-zA-Z0-9_.-]+",  # path/file
        ]

        files = []
        for pattern in file_patterns:
            matches = re.findall(pattern, user_message)
            files.extend(matches)

        # Filter out common false positives
        filtered_files = []
        for file_path in files:
            if len(file_path) > 3 and "." in file_path:
                # Skip URLs and version numbers
                if not file_path.startswith("http") and not file_path.startswith("www"):
                    filtered_files.append(file_path)

        return list(set(filtered_files))  # Remove duplicates

    def enhance_web_request(self, user_message: str, session_id: str) -> str:
        """Enhance user request with AgentOS standards for web interface"""

        # Get session file context
        file_context = self.get_session_context(session_id)

        # Extract potential file references
        referenced_files = self.extract_file_references(user_message)

        # Build enhanced prompt
        enhanced_parts = []

        # 1. Web-specific standards
        enhanced_parts.append("=== CODING STANDARDS ===")
        for standard_name, standard_content in self.web_standards.items():
            enhanced_parts.append(f"{standard_name.upper()}:{standard_content}")

        # 2. Project context
        project_context = self.get_project_context()
        if project_context:
            enhanced_parts.append("=== PROJECT CONTEXT ===")
            enhanced_parts.append(project_context)

        # 3. File context
        context_summary = file_context.get_context_summary()
        if context_summary != "No files in context.":
            enhanced_parts.append("=== FILE CONTEXT ===")
            enhanced_parts.append(context_summary)

            # Add details for referenced files
            for file_ref in referenced_files:
                file_info = file_context.get_file_context(file_ref)
                if file_info and file_info.get("content"):
                    enhanced_parts.append(f"\nContent of {file_ref}:")
                    enhanced_parts.append(f"```\n{file_info['content']}\n```")

        # 4. Original user request
        enhanced_parts.append("=== USER REQUEST ===")
        enhanced_parts.append(user_message)

        # 5. Response instructions
        enhanced_parts.append("=== RESPONSE INSTRUCTIONS ===")
        enhanced_parts.append(
            """
Please provide a helpful response that:
1. Follows all coding standards above
2. Uses the project context appropriately
3. References files accurately with full paths
4. Provides working, tested code
5. Explains your reasoning clearly

If modifying files, show both the original and updated code sections.
"""
        )

        return "\n\n".join(enhanced_parts)

    def analyze_complexity(self, user_message: str, session_id: str) -> Dict[str, Any]:
        """Analyze request complexity for smart routing"""

        # Keywords that indicate different complexity levels
        simple_keywords = [
            "fix typo",
            "add comment",
            "format",
            "style",
            "simple",
            "quick",
            "small change",
            "minor",
        ]

        complex_keywords = [
            "refactor",
            "architecture",
            "design",
            "implement",
            "create",
            "build",
            "system",
            "framework",
            "algorithm",
            "optimize",
        ]

        analysis_keywords = [
            "analyze",
            "review",
            "explain",
            "understand",
            "how does",
            "what is",
            "why",
            "best practices",
            "recommendations",
        ]

        message_lower = user_message.lower()

        # Count keyword matches
        simple_score = sum(1 for kw in simple_keywords if kw in message_lower)
        complex_score = sum(1 for kw in complex_keywords if kw in message_lower)
        analysis_score = sum(1 for kw in analysis_keywords if kw in message_lower)

        # Additional complexity factors
        file_context = self.get_session_context(session_id)
        files_referenced = len(self.extract_file_references(user_message))
        message_length = len(user_message.split())

        # Calculate overall complexity
        total_score = complex_score * 3 + analysis_score * 2 + simple_score

        if files_referenced > 3:
            total_score += 2
        if message_length > 50:
            total_score += 1

        # Determine complexity level
        if total_score <= 2 and simple_score > 0:
            complexity = "simple"
            tier = "fast"
        elif analysis_score > complex_score:
            complexity = "analysis"
            tier = "smart"
        elif total_score >= 5 or complex_score >= 2:
            complexity = "complex"
            tier = "smart"
        else:
            complexity = "moderate"
            tier = "balanced"

        return {
            "complexity": complexity,
            "recommended_tier": tier,
            "scores": {
                "simple": simple_score,
                "complex": complex_score,
                "analysis": analysis_score,
                "total": total_score,
            },
            "factors": {
                "files_referenced": files_referenced,
                "message_length": message_length,
            },
        }

    def create_task_breakdown(
        self, user_message: str, session_id: str
    ) -> TaskBreakdown:
        """Create task breakdown for complex requests"""

        complexity_analysis = self.analyze_complexity(user_message, session_id)

        if complexity_analysis["complexity"] in ["simple", "moderate"]:
            # Direct execution for simple tasks
            return TaskBreakdown(
                analysis_prompt="",
                execution_tasks=[user_message],
                estimated_cost=0.001,
                complexity=complexity_analysis["complexity"],
            )

        # For complex tasks, create analysis + execution breakdown
        analysis_prompt = f"""
Analyze this coding request and break it down into specific, actionable steps:

{user_message}

Consider:
1. What files need to be modified or created?
2. What are the main components or functions involved?
3. What's the logical sequence of changes?
4. Are there any dependencies or prerequisites?
5. What testing or validation is needed?

Provide a detailed breakdown with specific steps that can be executed individually.
"""

        # Estimated execution tasks (would be dynamically generated in practice)
        execution_tasks = [
            "Step 1: [Analysis result will determine specific tasks]",
            "Step 2: [Generated based on complexity analysis]",
            "Step 3: [Additional steps as needed]",
        ]

        return TaskBreakdown(
            analysis_prompt=analysis_prompt,
            execution_tasks=execution_tasks,
            estimated_cost=0.015 + (len(execution_tasks) * 0.003),
            complexity=complexity_analysis["complexity"],
        )

    def format_web_response(
        self, response: str, task_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format response for web display with metadata"""

        return {
            "content": response,
            "metadata": {
                "model_used": task_info.get("model", "unknown"),
                "complexity": task_info.get("complexity", "unknown"),
                "estimated_cost": task_info.get("cost", 0.0),
                "processing_time": task_info.get("processing_time", 0.0),
                "timestamp": datetime.now().isoformat(),
            },
            "suggestions": self.generate_followup_suggestions(response, task_info),
        }

    def generate_followup_suggestions(
        self, response: str, task_info: Dict[str, Any]
    ) -> List[str]:
        """Generate follow-up suggestions based on response"""

        suggestions = []

        # Code-related suggestions
        if "```" in response:  # Contains code
            suggestions.extend(
                [
                    "Would you like me to add tests for this code?",
                    "Should I review this code for potential improvements?",
                    "Do you need help with error handling for this implementation?",
                ]
            )

        # File modification suggestions
        if any(
            keyword in response.lower()
            for keyword in ["create", "modify", "update", "file"]
        ):
            suggestions.extend(
                [
                    "Would you like me to show you how to integrate this with your existing code?",
                    "Should I create documentation for these changes?",
                ]
            )

        # Analysis suggestions
        if task_info.get("complexity") == "analysis":
            suggestions.extend(
                [
                    "Would you like me to implement any of these recommendations?",
                    "Do you need more details about any specific aspect?",
                ]
            )

        return suggestions[:3]  # Limit to 3 suggestions

    def get_web_slash_commands(self) -> Dict[str, str]:
        """Get available slash commands for web interface"""
        return {
            "/help": "Show available commands and usage",
            "/context": "Show current file context",
            "/clear": "Clear file context for this session",
            "/add": "Add file to context: /add path/to/file.py",
            "/budget": "Show current budget status",
            "/standards": "Show current coding standards",
            "/complexity": "Analyze complexity of last request",
        }

    def handle_web_slash_command(
        self, command: str, args: str, session_id: str
    ) -> Dict[str, Any]:
        """Handle slash commands in web interface"""

        if command == "/help":
            commands = self.get_web_slash_commands()
            help_text = "Available commands:\n\n"
            for cmd, desc in commands.items():
                help_text += f"**{cmd}** - {desc}\n"

            return {
                "type": "system_message",
                "content": help_text,
                "metadata": {"command": command},
            }

        elif command == "/context":
            file_context = self.get_session_context(session_id)
            context_summary = file_context.get_context_summary()

            return {
                "type": "system_message",
                "content": f"**Current File Context:**\n\n{context_summary}",
                "metadata": {"command": command},
            }

        elif command == "/clear":
            if session_id in self.session_contexts:
                del self.session_contexts[session_id]

            return {
                "type": "system_message",
                "content": "✅ File context cleared for this session.",
                "metadata": {"command": command},
            }

        elif command == "/add":
            if not args:
                return {
                    "type": "error",
                    "content": "Usage: /add path/to/file.py",
                    "metadata": {"command": command},
                }

            file_path = args.strip()
            # In practice, would read file content
            self.add_file_to_session(
                session_id,
                file_path,
                "# File content would be loaded here",
                {"type": "code", "language": "python"},
            )

            return {
                "type": "system_message",
                "content": f"✅ Added {file_path} to context.",
                "metadata": {"command": command},
            }

        elif command == "/standards":
            standards_text = "**Current Coding Standards:**\n\n"
            for name, content in self.web_standards.items():
                standards_text += f"**{name.title()}:**{content}\n\n"

            return {
                "type": "system_message",
                "content": standards_text,
                "metadata": {"command": command},
            }

        else:
            return {
                "type": "error",
                "content": f"Unknown command: {command}. Type /help for available commands.",
                "metadata": {"command": command},
            }
