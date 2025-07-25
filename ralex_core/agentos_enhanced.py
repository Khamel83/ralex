"""
Enhanced AgentOS Integration for Ralex V3

Provides advanced context awareness, better file detection, and streaming integration
with AgentOS standards for optimal web-based coding assistance.
"""

import re
import ast
import os
import json
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime
from pathlib import Path
import logging

from ralex_core.agentos_web_integration import AgentOSWebIntegration, WebFileContext


class EnhancedWebFileContext(WebFileContext):
    """Enhanced file context with better analysis and detection"""
    
    def __init__(self):
        super().__init__()
        self.code_patterns: Dict[str, List[str]] = {}
        self.dependencies: Dict[str, Set[str]] = {}
        self.logger = logging.getLogger(__name__)
    
    def analyze_code_content(self, file_path: str, content: str) -> Dict[str, Any]:
        """Analyze code content for patterns, functions, and dependencies"""
        analysis = {
            "language": self._detect_language(file_path),
            "functions": [],
            "classes": [],
            "imports": [],
            "complexity_score": 0,
            "lines_of_code": len(content.splitlines()),
            "patterns": []
        }
        
        try:
            if analysis["language"] == "python":
                analysis.update(self._analyze_python_content(content))
            elif analysis["language"] in ["javascript", "typescript"]:
                analysis.update(self._analyze_js_content(content))
            
        except Exception as e:
            self.logger.warning(f"Code analysis failed for {file_path}: {e}")
        
        return analysis
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix.lower()
        language_map = {
            '.py': 'python',
            '.js': 'javascript', 
            '.ts': 'typescript',
            '.jsx': 'react',
            '.tsx': 'react-typescript',
            '.go': 'go',
            '.rs': 'rust',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.html': 'html',
            '.css': 'css',
            '.sql': 'sql',
            '.md': 'markdown',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml'
        }
        return language_map.get(ext, 'text')
    
    def _analyze_python_content(self, content: str) -> Dict[str, Any]:
        """Analyze Python code using AST"""
        try:
            tree = ast.parse(content)
            analysis = {
                "functions": [],
                "classes": [],
                "imports": [],
                "complexity_score": 0
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis["functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": len(node.args.args),
                        "is_async": isinstance(node, ast.AsyncFunctionDef)
                    })
                    analysis["complexity_score"] += 1
                
                elif isinstance(node, ast.ClassDef):
                    analysis["classes"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                    })
                    analysis["complexity_score"] += 2
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis["imports"].append(alias.name)
                    else:
                        module = node.module or ""
                        for alias in node.names:
                            analysis["imports"].append(f"{module}.{alias.name}")
            
            return analysis
            
        except Exception as e:
            self.logger.warning(f"Python AST analysis failed: {e}")
            return {"functions": [], "classes": [], "imports": [], "complexity_score": 0}
    
    def _analyze_js_content(self, content: str) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript content with regex patterns"""
        analysis = {
            "functions": [],
            "classes": [],
            "imports": [],
            "complexity_score": 0
        }
        
        # Function patterns
        func_patterns = [
            r'function\s+(\w+)\s*\(',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>',
            r'(\w+)\s*:\s*\([^)]*\)\s*=>',
            r'async\s+function\s+(\w+)\s*\('
        ]
        
        for pattern in func_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                analysis["functions"].append({"name": match, "type": "function"})
                analysis["complexity_score"] += 1
        
        # Class patterns
        class_matches = re.findall(r'class\s+(\w+)', content)
        for match in class_matches:
            analysis["classes"].append({"name": match})
            analysis["complexity_score"] += 2
        
        # Import patterns
        import_patterns = [
            r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s+[\'"]([^\'"]+)[\'"]',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            analysis["imports"].extend(matches)
        
        return analysis
    
    def add_file_with_analysis(self, file_path: str, content: str = None, metadata: Dict = None):
        """Add file with comprehensive analysis"""
        if content:
            analysis = self.analyze_code_content(file_path, content)
            enhanced_metadata = {
                **(metadata or {}),
                "analysis": analysis
            }
        else:
            enhanced_metadata = metadata or {}
        
        self.add_file(file_path, content, enhanced_metadata)
        
        # Track code patterns for context suggestions
        if content and file_path.endswith(('.py', '.js', '.ts')):
            self.code_patterns[file_path] = self._extract_patterns(content)
    
    def _extract_patterns(self, content: str) -> List[str]:
        """Extract common code patterns for context suggestions"""
        patterns = []
        
        # Common patterns to track
        pattern_regexes = [
            r'class\s+\w+',
            r'def\s+\w+',
            r'function\s+\w+',
            r'import\s+\w+',
            r'from\s+\w+\s+import',
            r'@\w+',  # Decorators
            r'async\s+def',
            r'try:',
            r'except\s+\w*:',
            r'if\s+__name__\s*==\s*["\']__main__["\']'
        ]
        
        for pattern in pattern_regexes:
            matches = re.findall(pattern, content)
            patterns.extend(matches)
        
        return patterns[:10]  # Limit to top 10 patterns
    
    def get_related_files(self, file_path: str) -> List[str]:
        """Get files related to the given file based on imports and patterns"""
        related = []
        
        if file_path in self.files:
            file_analysis = self.files[file_path].get("metadata", {}).get("analysis", {})
            imports = file_analysis.get("imports", [])
            
            # Find files that might match imports
            for other_path in self.files:
                if other_path != file_path:
                    # Simple matching based on filename
                    other_name = Path(other_path).stem
                    if any(other_name in imp for imp in imports):
                        related.append(other_path)
        
        return related[:5]  # Limit to top 5 related files


class EnhancedAgentOSIntegration(AgentOSWebIntegration):
    """Enhanced AgentOS integration with advanced context awareness"""
    
    def __init__(self, agent_os_path: str = "agent_os"):
        # Initialize parent with enhanced file context
        super().__init__(agent_os_path)
        self.session_contexts = {}  # Will be populated with EnhancedWebFileContext
        self.context_cache: Dict[str, Dict[str, Any]] = {}
        self.pattern_memory: Dict[str, List[str]] = {}
        self.logger = logging.getLogger(__name__)
    
    def get_session_context(self, session_id: str) -> EnhancedWebFileContext:
        """Get or create enhanced file context for session"""
        if session_id not in self.session_contexts:
            self.session_contexts[session_id] = EnhancedWebFileContext()
        return self.session_contexts[session_id]
    
    def extract_file_references_enhanced(self, user_message: str) -> Dict[str, List[str]]:
        """Enhanced file reference extraction with better pattern matching"""
        references = {
            "explicit_files": [],
            "function_names": [],
            "class_names": [],
            "module_names": [],
            "potential_files": []
        }
        
        # Explicit file patterns (enhanced)
        file_patterns = [
            r'(?:file|in|from|edit|modify|update|check)\s+([a-zA-Z0-9_/.-]+\.[a-zA-Z]{1,4})',
            r'([a-zA-Z0-9_/.-]+\.[a-zA-Z]{1,4})',
            r'`([a-zA-Z0-9_/.-]+\.[a-zA-Z]{1,4})`',
            r'"([a-zA-Z0-9_/.-]+\.[a-zA-Z]{1,4})"',
            r"'([a-zA-Z0-9_/.-]+\.[a-zA-Z]{1,4})'"
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, user_message, re.IGNORECASE)
            references["explicit_files"].extend(matches)
        
        # Function/method patterns
        func_patterns = [
            r'(?:function|method|def)\s+(\w+)',
            r'(\w+)\s*\(\s*\)',  # function calls
            r'`(\w+)\(\)`',  # backtick function references
        ]
        
        for pattern in func_patterns:
            matches = re.findall(pattern, user_message)
            references["function_names"].extend(matches)
        
        # Class patterns
        class_patterns = [
            r'(?:class|Class)\s+(\w+)',
            r'(\w+)\.(\w+)',  # Class.method patterns
        ]
        
        for pattern in class_patterns:
            matches = re.findall(pattern, user_message)
            if isinstance(matches[0], tuple):
                references["class_names"].extend([m[0] for m in matches])
                references["function_names"].extend([m[1] for m in matches])
            else:
                references["class_names"].extend(matches)
        
        # Module/import patterns
        module_patterns = [
            r'(?:import|from)\s+(\w+)',
            r'(\w+)\.py',
            r'module\s+(\w+)'
        ]
        
        for pattern in module_patterns:
            matches = re.findall(pattern, user_message)
            references["module_names"].extend(matches)
        
        # Clean and deduplicate
        for key in references:
            references[key] = list(set(filter(None, references[key])))
        
        return references
    
    def build_enhanced_context(self, user_message: str, session_id: str) -> Dict[str, Any]:
        """Build comprehensive context for the request"""
        context = {
            "file_references": self.extract_file_references_enhanced(user_message),
            "complexity_analysis": self.analyze_complexity_enhanced(user_message, session_id),
            "session_state": self.get_session_state(session_id),
            "related_files": [],
            "suggested_standards": [],
            "context_summary": ""
        }
        
        # Get session file context
        file_context = self.get_session_context(session_id)
        
        # Find related files based on references
        for file_ref in context["file_references"]["explicit_files"]:
            related = file_context.get_related_files(file_ref)
            context["related_files"].extend(related)
        
        # Suggest relevant standards based on file types and patterns
        context["suggested_standards"] = self.suggest_relevant_standards(
            context["file_references"], 
            context["complexity_analysis"]
        )
        
        # Build context summary
        context["context_summary"] = self.build_context_summary(context, file_context)
        
        return context
    
    def analyze_complexity_enhanced(self, user_message: str, session_id: str) -> Dict[str, Any]:
        """Enhanced complexity analysis with more factors"""
        base_analysis = super().analyze_complexity(user_message, session_id)
        
        # Additional complexity factors
        enhancement_factors = {
            "mentions_multiple_files": len(self.extract_file_references_enhanced(user_message)["explicit_files"]) > 1,
            "mentions_testing": any(word in user_message.lower() for word in ["test", "testing", "spec", "coverage"]),
            "mentions_refactoring": any(word in user_message.lower() for word in ["refactor", "restructure", "reorganize"]),
            "mentions_architecture": any(word in user_message.lower() for word in ["architecture", "design", "pattern", "structure"]),
            "mentions_performance": any(word in user_message.lower() for word in ["performance", "optimize", "speed", "efficiency"]),
            "mentions_database": any(word in user_message.lower() for word in ["database", "db", "sql", "query", "model"]),
            "mentions_api": any(word in user_message.lower() for word in ["api", "endpoint", "route", "service", "client"]),
            "question_type": self.classify_question_type(user_message)
        }
        
        # Adjust complexity based on enhancement factors
        additional_score = sum([
            2 if enhancement_factors["mentions_multiple_files"] else 0,
            1 if enhancement_factors["mentions_testing"] else 0,
            3 if enhancement_factors["mentions_refactoring"] else 0,
            3 if enhancement_factors["mentions_architecture"] else 0,
            2 if enhancement_factors["mentions_performance"] else 0,
            2 if enhancement_factors["mentions_database"] else 0,
            1 if enhancement_factors["mentions_api"] else 0,
        ])
        
        # Update complexity based on question type
        if enhancement_factors["question_type"] == "explanation":
            base_analysis["recommended_tier"] = "smart"
        elif enhancement_factors["question_type"] == "implementation":
            additional_score += 2
        
        # Recalculate overall complexity
        total_score = base_analysis["scores"]["total"] + additional_score
        
        if total_score >= 8:
            complexity = "very_complex"
            tier = "smart"
        elif total_score >= 5:
            complexity = "complex"  
            tier = "smart"
        elif total_score >= 3:
            complexity = "moderate"
            tier = "balanced"
        else:
            complexity = base_analysis["complexity"]
            tier = base_analysis["recommended_tier"]
        
        # Enhanced analysis result
        return {
            **base_analysis,
            "complexity": complexity,
            "recommended_tier": tier,
            "enhancement_factors": enhancement_factors,
            "enhanced_score": total_score,
            "reasoning": self.build_complexity_reasoning(base_analysis, enhancement_factors, total_score)
        }
    
    def classify_question_type(self, user_message: str) -> str:
        """Classify the type of question/request"""
        message_lower = user_message.lower()
        
        explanation_words = ["explain", "how does", "what is", "why", "describe", "clarify"]
        implementation_words = ["create", "build", "implement", "add", "write", "develop"]
        debugging_words = ["fix", "debug", "error", "bug", "issue", "problem"]
        review_words = ["review", "check", "analyze", "audit", "improve"]
        
        if any(word in message_lower for word in explanation_words):
            return "explanation"
        elif any(word in message_lower for word in implementation_words):
            return "implementation"
        elif any(word in message_lower for word in debugging_words):
            return "debugging"
        elif any(word in message_lower for word in review_words):
            return "review"
        else:
            return "general"
    
    def suggest_relevant_standards(self, file_references: Dict[str, List[str]], 
                                 complexity_analysis: Dict[str, Any]) -> List[str]:
        """Suggest relevant standards based on context"""
        suggestions = []
        
        # File-type based suggestions
        explicit_files = file_references.get("explicit_files", [])
        for file_path in explicit_files:
            if file_path.endswith('.py'):
                suggestions.append("python")
            elif file_path.endswith(('.js', '.ts')):
                suggestions.append("javascript")
            elif file_path.endswith('.md'):
                suggestions.append("documentation")
        
        # Complexity-based suggestions
        if complexity_analysis.get("complexity") in ["complex", "very_complex"]:
            suggestions.extend(["testing", "error-handling", "documentation"])
        
        # Enhancement factor suggestions
        factors = complexity_analysis.get("enhancement_factors", {})
        if factors.get("mentions_testing"):
            suggestions.append("testing")
        if factors.get("mentions_architecture"):
            suggestions.extend(["design-patterns", "architecture"])
        if factors.get("mentions_database"):
            suggestions.append("database")
        if factors.get("mentions_api"):
            suggestions.append("api-design")
        
        return list(set(suggestions))  # Remove duplicates
    
    def build_complexity_reasoning(self, base_analysis: Dict[str, Any], 
                                 enhancement_factors: Dict[str, Any], 
                                 enhanced_score: int) -> str:
        """Build human-readable reasoning for complexity analysis"""
        reasons = []
        
        # Base factors
        if base_analysis["scores"]["complex"] > 0:
            reasons.append(f"contains {base_analysis['scores']['complex']} complex keywords")
        if base_analysis["scores"]["analysis"] > 0:
            reasons.append(f"requires {base_analysis['scores']['analysis']} analysis tasks")
        
        # Enhancement factors
        if enhancement_factors["mentions_multiple_files"]:
            reasons.append("involves multiple files")
        if enhancement_factors["mentions_refactoring"]:
            reasons.append("requires refactoring")
        if enhancement_factors["mentions_architecture"]:
            reasons.append("involves architectural decisions")
        if enhancement_factors["mentions_testing"]:
            reasons.append("includes testing requirements")
        
        question_type = enhancement_factors["question_type"]
        if question_type == "implementation":
            reasons.append("requires implementation work")
        elif question_type == "explanation":
            reasons.append("needs detailed explanation")
        
        return f"Enhanced score: {enhanced_score}/10. " + ", ".join(reasons) if reasons else "Standard complexity analysis"
    
    def get_session_state(self, session_id: str) -> Dict[str, Any]:
        """Get current session state for context"""
        file_context = self.get_session_context(session_id)
        
        return {
            "files_in_context": len(file_context.files),
            "recent_files": file_context.recent_files[:3],
            "languages_present": self.get_languages_in_context(file_context),
            "patterns_detected": len(file_context.code_patterns),
            "session_age": "current"  # Could track actual session age
        }
    
    def get_languages_in_context(self, file_context: EnhancedWebFileContext) -> List[str]:
        """Get programming languages present in the current context"""
        languages = set()
        
        for file_path, file_data in file_context.files.items():
            analysis = file_data.get("metadata", {}).get("analysis", {})
            language = analysis.get("language")
            if language and language != "text":
                languages.add(language)
        
        return list(languages)
    
    def build_context_summary(self, context: Dict[str, Any], 
                            file_context: EnhancedWebFileContext) -> str:
        """Build a comprehensive context summary"""
        summary_parts = []
        
        # Session state
        session_state = context["session_state"]
        if session_state["files_in_context"] > 0:
            summary_parts.append(f"{session_state['files_in_context']} files in context")
            if session_state["languages_present"]:
                summary_parts.append(f"Languages: {', '.join(session_state['languages_present'])}")
        
        # File references
        file_refs = context["file_references"]
        if file_refs["explicit_files"]:
            summary_parts.append(f"Referenced files: {', '.join(file_refs['explicit_files'][:3])}")
        
        # Complexity
        complexity = context["complexity_analysis"]
        summary_parts.append(f"Complexity: {complexity['complexity']} ({complexity['recommended_tier']} model)")
        
        # Standards
        if context["suggested_standards"]:
            summary_parts.append(f"Relevant standards: {', '.join(context['suggested_standards'][:3])}")
        
        return "; ".join(summary_parts) if summary_parts else "No specific context"
    
    def enhance_web_request_v2(self, user_message: str, session_id: str) -> str:
        """Enhanced version of web request enhancement"""
        
        # Build comprehensive context
        context = self.build_enhanced_context(user_message, session_id)
        
        # Get session file context
        file_context = self.get_session_context(session_id)
        
        # Build enhanced prompt sections
        prompt_sections = []
        
        # 1. Enhanced standards (context-aware)
        prompt_sections.append("=== ENHANCED CODING STANDARDS ===")
        relevant_standards = self.get_relevant_standards(context["suggested_standards"])
        for standard_name, standard_content in relevant_standards.items():
            prompt_sections.append(f"{standard_name.upper()}:\n{standard_content}")
        
        # 2. Session context
        if context["session_state"]["files_in_context"] > 0:
            prompt_sections.append("=== SESSION CONTEXT ===")
            prompt_sections.append(context["context_summary"])
            
            # Include relevant file content
            for file_path in context["file_references"]["explicit_files"][:2]:
                file_info = file_context.get_file_context(file_path)
                if file_info and file_info.get("content"):
                    prompt_sections.append(f"\nCurrent content of {file_path}:")
                    # Include analysis if available
                    analysis = file_info.get("metadata", {}).get("analysis", {})
                    if analysis:
                        prompt_sections.append(f"// Analysis: {analysis.get('language', 'unknown')} file with {len(analysis.get('functions', []))} functions, {len(analysis.get('classes', []))} classes")
                    prompt_sections.append(f"```\n{file_info['content'][:1000]}...\n```")
        
        # 3. Complexity guidance
        prompt_sections.append("=== REQUEST ANALYSIS ===")
        complexity = context["complexity_analysis"]
        prompt_sections.append(f"Complexity: {complexity['complexity']}")
        prompt_sections.append(f"Recommended approach: {complexity['reasoning']}")
        
        # 4. Original request
        prompt_sections.append("=== USER REQUEST ===")
        prompt_sections.append(user_message)
        
        # 5. Enhanced response instructions
        prompt_sections.append("=== RESPONSE INSTRUCTIONS ===")
        prompt_sections.append(self.build_response_instructions(context))
        
        return "\n\n".join(prompt_sections)
    
    def get_relevant_standards(self, suggested_standards: List[str]) -> Dict[str, str]:
        """Get only the standards relevant to the current context"""
        relevant = {}
        
        # Always include web standards
        relevant.update(self.web_standards)
        
        # Add AgentOS standards that are relevant
        for standard_name in suggested_standards:
            if standard_name in self.standards:
                relevant[standard_name] = self.standards[standard_name]
        
        return relevant
    
    def build_response_instructions(self, context: Dict[str, Any]) -> str:
        """Build context-aware response instructions"""
        instructions = [
            "Please provide a response that:",
            "1. Follows all relevant coding standards above",
            "2. Uses the session context appropriately"
        ]
        
        complexity = context["complexity_analysis"]["complexity"]
        if complexity in ["complex", "very_complex"]:
            instructions.extend([
                "3. Breaks down complex tasks into clear steps",
                "4. Explains architectural decisions and trade-offs",
                "5. Includes comprehensive error handling"
            ])
        else:
            instructions.extend([
                "3. Provides direct, actionable solutions",
                "4. Includes brief explanations for key decisions"
            ])
        
        # File-specific instructions
        file_refs = context["file_references"]
        if file_refs["explicit_files"]:
            instructions.append("6. Shows both original and modified code sections when editing files")
            instructions.append("7. Uses complete file paths for all file operations")
        
        # Testing instructions
        if any("test" in word for word in context["suggested_standards"]):
            instructions.append("8. Includes test cases with good coverage")
        
        return "\n".join(instructions)


# Global enhanced instance
enhanced_agentos = EnhancedAgentOSIntegration()