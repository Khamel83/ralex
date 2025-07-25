"""
Command Parser for Ralex V4

Parses natural language voice commands into structured intents for the orchestrator.
Handles command validation, parameter extraction, and intent classification.
"""

import re
import logging
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class CommandType(Enum):
    """Types of commands that can be processed"""
    FILE_OPERATION = "file_operation"
    SHELL_COMMAND = "shell_command"
    WORKFLOW = "workflow"
    QUESTION = "question"
    REFACTOR = "refactor"
    DEBUG = "debug"
    TEST = "test"
    DEPLOY = "deploy"
    ANALYZE = "analyze"
    UNKNOWN = "unknown"


class AutoSubmitTrigger(Enum):
    """Auto-submit trigger phrases"""
    EXECUTE = "execute"
    SEND_IT = "send it"
    GO_AHEAD = "go ahead"
    DO_IT = "do it"
    RUN_IT = "run it"


@dataclass
class FileReference:
    """Represents a file mentioned in a command"""
    path: str
    exists: Optional[bool] = None
    file_type: Optional[str] = None
    confidence: float = 1.0


@dataclass
class ParsedCommand:
    """Structured representation of a parsed voice command"""
    original_text: str
    command_type: CommandType
    intent: str
    is_valid: bool
    error: Optional[str] = None
    
    # Command components
    action: str = ""
    target: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    # File references
    file_references: List[FileReference] = field(default_factory=list)
    
    # Auto-submit detection
    auto_submit: bool = False
    trigger_phrase: Optional[str] = None
    
    # Complexity indicators
    complexity_score: int = 1
    complexity_factors: List[str] = field(default_factory=list)
    
    # Metadata
    parsed_at: datetime = field(default_factory=datetime.now)
    confidence: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "original_text": self.original_text,
            "command_type": self.command_type.value,
            "intent": self.intent,
            "is_valid": self.is_valid,
            "error": self.error,
            "action": self.action,
            "target": self.target,
            "parameters": self.parameters,
            "file_references": [
                {
                    "path": ref.path,
                    "exists": ref.exists,
                    "file_type": ref.file_type,
                    "confidence": ref.confidence
                }
                for ref in self.file_references
            ],
            "auto_submit": self.auto_submit,
            "trigger_phrase": self.trigger_phrase,
            "complexity_score": self.complexity_score,
            "complexity_factors": self.complexity_factors,
            "parsed_at": self.parsed_at.isoformat(),
            "confidence": self.confidence
        }


class CommandParser:
    """
    Natural language command parser for voice input
    
    Converts voice commands into structured ParsedCommand objects
    with intent classification, parameter extraction, and validation.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Auto-submit trigger phrases
        self.auto_submit_triggers = {
            "execute", "send it", "go ahead", "do it", "run it",
            "make it happen", "proceed", "continue", "apply it"
        }
        
        # Command type patterns
        self.command_patterns = self._build_command_patterns()
        
        # File extension patterns
        self.file_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c',
            '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
            '.html', '.css', '.scss', '.less', '.json', '.xml', '.yaml',
            '.yml', '.md', '.txt', '.sql', '.sh', '.bat', '.ps1'
        }
        
        # Complexity indicators
        self.complexity_indicators = {
            "simple": ["fix", "add", "remove", "delete", "create", "update"],
            "moderate": ["refactor", "optimize", "improve", "enhance", "modify"],
            "complex": ["implement", "build", "design", "architect", "restructure"],
            "very_complex": ["migrate", "overhaul", "rewrite", "redesign"]
        }
        
        self.logger.info("Command parser initialized")
    
    def _build_command_patterns(self) -> Dict[CommandType, List[str]]:
        """Build regex patterns for different command types"""
        return {
            CommandType.FILE_OPERATION: [
                r'(?:read|open|show|display|view)\s+(.+)',
                r'(?:write|save|create|make)\s+(?:a\s+)?(?:new\s+)?(.+)',
                r'(?:edit|modify|change|update)\s+(.+)',
                r'(?:delete|remove|rm)\s+(.+)',
                r'(?:copy|cp)\s+(.+?)\s+(?:to|into)\s+(.+)',
                r'(?:move|mv)\s+(.+?)\s+(?:to|into)\s+(.+)'
            ],
            CommandType.SHELL_COMMAND: [
                r'(?:run|execute)\s+(.+)',
                r'(?:git|npm|pip|docker|kubectl)\s+(.+)',
                r'(?:install|uninstall)\s+(.+)',
                r'(?:start|stop|restart)\s+(.+)',
                r'(?:build|compile|deploy)\s*(.+)?'
            ],
            CommandType.WORKFLOW: [
                r'(?:deploy|release)\s+(.+)',
                r'(?:setup|configure)\s+(.+)',
                r'(?:initialize|init)\s+(.+)',
                r'(?:prepare|ready)\s+(.+?)\s+for\s+(.+)'
            ],
            CommandType.REFACTOR: [
                r'(?:refactor|restructure|reorganize)\s+(.+)',
                r'(?:optimize|improve|enhance)\s+(.+)',
                r'(?:clean\s+up|cleanup)\s+(.+)',
                r'(?:simplify|streamline)\s+(.+)'
            ],
            CommandType.DEBUG: [
                r'(?:debug|fix|solve|resolve)\s+(.+)',
                r'(?:find|locate|identify)\s+(?:the\s+)?(?:bug|error|issue)\s+in\s+(.+)',
                r'(?:troubleshoot|diagnose)\s+(.+)',
                r'(?:investigate|analyze)\s+(?:the\s+)?(?:problem|issue)\s+in\s+(.+)'
            ],
            CommandType.TEST: [
                r'(?:test|check|verify)\s+(.+)',
                r'(?:add|create|write)\s+(?:tests?|specs?)\s+for\s+(.+)',
                r'(?:run|execute)\s+(?:tests?|specs?)\s*(?:for\s+(.+))?',
                r'(?:validate|ensure)\s+(.+)'
            ],
            CommandType.ANALYZE: [
                r'(?:analyze|examine|review|inspect)\s+(.+)',
                r'(?:explain|describe|tell\s+me\s+about)\s+(.+)',
                r'(?:what|how|why)\s+(.+)',
                r'(?:show\s+me|display)\s+(?:the\s+)?(.+)'
            ],
            CommandType.QUESTION: [
                r'(?:what|how|why|when|where|which)\s+(.+)\?',
                r'(?:can\s+you|could\s+you|please)\s+(.+)\?',
                r'(?:help\s+me|assist\s+me)\s+(?:with\s+)?(.+)\??',
                r'(?:is|are|does|do|will|would)\s+(.+)\?'
            ]
        }
    
    async def parse(self, command_text: str) -> ParsedCommand:
        """
        Parse a natural language command into structured components
        
        Args:
            command_text: Raw voice command text
            
        Returns:
            ParsedCommand object with parsed components
        """
        try:
            self.logger.debug(f"Parsing command: '{command_text}'")
            
            # Clean and normalize input
            cleaned_text = self._clean_command_text(command_text)
            if not cleaned_text:
                return ParsedCommand(
                    original_text=command_text,
                    command_type=CommandType.UNKNOWN,
                    intent="empty_command",
                    is_valid=False,
                    error="Empty or invalid command"
                )
            
            # Detect auto-submit triggers
            auto_submit, trigger_phrase = self._detect_auto_submit(cleaned_text)
            
            # Remove trigger phrase for parsing
            parsing_text = self._remove_trigger_phrase(cleaned_text, trigger_phrase)
            
            # Extract file references
            file_references = self._extract_file_references(parsing_text)
            
            # Classify command type and extract intent
            command_type, intent, action, target = self._classify_command(parsing_text)
            
            # Extract parameters
            parameters = self._extract_parameters(parsing_text, command_type)
            
            # Calculate complexity
            complexity_score, complexity_factors = self._calculate_complexity(
                parsing_text, command_type, file_references
            )
            
            # Validate command
            is_valid, error = self._validate_command(
                command_type, action, target, parameters, file_references
            )
            
            # Build parsed command
            parsed_command = ParsedCommand(
                original_text=command_text,
                command_type=command_type,
                intent=intent,
                is_valid=is_valid,
                error=error,
                action=action,
                target=target,
                parameters=parameters,
                file_references=file_references,
                auto_submit=auto_submit,
                trigger_phrase=trigger_phrase,
                complexity_score=complexity_score,
                complexity_factors=complexity_factors,
                confidence=self._calculate_confidence(command_type, intent, file_references)
            )
            
            self.logger.debug(f"Parsed command: {parsed_command.intent} ({parsed_command.command_type.value})")
            return parsed_command
            
        except Exception as e:
            self.logger.error(f"Error parsing command '{command_text}': {e}")
            return ParsedCommand(
                original_text=command_text,
                command_type=CommandType.UNKNOWN,
                intent="parse_error",
                is_valid=False,
                error=f"Parse error: {str(e)}"
            )
    
    def _clean_command_text(self, text: str) -> str:
        """Clean and normalize command text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Convert to lowercase for processing
        text = text.lower()
        
        # Remove common filler words at the start
        filler_patterns = [
            r'^(?:um|uh|hmm|well|so|okay|ok)\s+',
            r'^(?:please|can you|could you|would you)\s+',
            r'^(?:i want to|i need to|i would like to)\s+'
        ]
        
        for pattern in filler_patterns:
            text = re.sub(pattern, '', text)
        
        return text.strip()
    
    def _detect_auto_submit(self, text: str) -> tuple[bool, Optional[str]]:
        """Detect auto-submit trigger phrases"""
        text_lower = text.lower()
        
        for trigger in self.auto_submit_triggers:
            if text_lower.endswith(trigger):
                return True, trigger
            
            # Also check for trigger at end of sentence
            pattern = f"\\b{re.escape(trigger)}$"
            if re.search(pattern, text_lower):
                return True, trigger
        
        return False, None
    
    def _remove_trigger_phrase(self, text: str, trigger_phrase: Optional[str]) -> str:
        """Remove trigger phrase from text for parsing"""
        if not trigger_phrase:
            return text
        
        # Remove the trigger phrase from the end
        pattern = f"\\s*\\b{re.escape(trigger_phrase)}$"
        return re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
    
    def _extract_file_references(self, text: str) -> List[FileReference]:
        """Extract file references from command text"""
        file_references = []
        
        # Patterns for file references
        file_patterns = [
            # Explicit file paths with extensions
            r'([a-zA-Z0-9_/.-]+\.[a-zA-Z]{1,4})',
            # Files in quotes
            r'["\']([a-zA-Z0-9_/.-]+\.[a-zA-Z]{1,4})["\']',
            # Files with 'file' keyword
            r'(?:file|script|module)\s+([a-zA-Z0-9_/.-]+(?:\.[a-zA-Z]{1,4})?)',
            # Common file names without extension
            r'\b(readme|makefile|dockerfile|requirements)\b',
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Validate file extension if present
                if '.' in match:
                    ext = '.' + match.split('.')[-1].lower()
                    if ext in self.file_extensions:
                        file_references.append(FileReference(
                            path=match,
                            file_type=ext,
                            confidence=0.9
                        ))
                else:
                    file_references.append(FileReference(
                        path=match,
                        confidence=0.7
                    ))
        
        # Remove duplicates
        seen = set()
        unique_refs = []
        for ref in file_references:
            if ref.path not in seen:
                seen.add(ref.path)
                unique_refs.append(ref)
        
        return unique_refs
    
    def _classify_command(self, text: str) -> tuple[CommandType, str, str, str]:
        """Classify command type and extract intent"""
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    groups = match.groups()
                    action = self._extract_action_word(text)
                    target = groups[0] if groups else ""
                    intent = f"{action}_{command_type.value}"
                    
                    return command_type, intent, action, target
        
        # Default classification
        action = self._extract_action_word(text)
        return CommandType.UNKNOWN, f"{action}_unknown", action, text
    
    def _extract_action_word(self, text: str) -> str:
        """Extract the main action word from the command"""
        action_words = [
            'create', 'make', 'build', 'write', 'add', 'insert',
            'read', 'open', 'show', 'display', 'view', 'get',
            'edit', 'modify', 'change', 'update', 'alter',
            'delete', 'remove', 'rm', 'clear', 'clean',
            'copy', 'move', 'rename',
            'fix', 'debug', 'solve', 'resolve',
            'test', 'check', 'verify', 'validate',
            'deploy', 'build', 'compile', 'run', 'execute',
            'refactor', 'optimize', 'improve', 'enhance',
            'analyze', 'examine', 'review', 'inspect'
        ]
        
        words = text.split()
        for word in words:
            if word in action_words:
                return word
        
        return words[0] if words else "unknown"
    
    def _extract_parameters(self, text: str, command_type: CommandType) -> Dict[str, Any]:
        """Extract command parameters based on type"""
        parameters = {}
        
        # Common parameter patterns
        param_patterns = {
            'with': r'with\s+([^,\s]+(?:\s+[^,\s]+)?)',
            'using': r'using\s+([^,\s]+(?:\s+[^,\s]+)?)',
            'in': r'in\s+([^,\s]+)',
            'to': r'to\s+([^,\s]+)',
            'from': r'from\s+([^,\s]+)',
            'for': r'for\s+([^,\s]+)',
        }
        
        for param_name, pattern in param_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                parameters[param_name] = match.group(1)
        
        # Command-specific parameters
        if command_type == CommandType.TEST:
            if 'coverage' in text:
                parameters['coverage'] = True
            if re.search(r'(\d+)%?\s+coverage', text):
                coverage_match = re.search(r'(\d+)%?\s+coverage', text)
                parameters['coverage_target'] = int(coverage_match.group(1))
        
        return parameters
    
    def _calculate_complexity(self, text: str, command_type: CommandType, 
                            file_references: List[FileReference]) -> tuple[int, List[str]]:
        """Calculate command complexity score and factors"""
        complexity_score = 1
        factors = []
        
        # Base complexity by command type
        type_complexity = {
            CommandType.FILE_OPERATION: 1,
            CommandType.SHELL_COMMAND: 2,
            CommandType.QUESTION: 1,
            CommandType.REFACTOR: 3,
            CommandType.DEBUG: 2,
            CommandType.TEST: 2,
            CommandType.DEPLOY: 4,
            CommandType.WORKFLOW: 4,
            CommandType.ANALYZE: 2
        }
        
        complexity_score = type_complexity.get(command_type, 1)
        
        # Multiple files increase complexity
        if len(file_references) > 1:
            complexity_score += 2
            factors.append("multiple_files")
        
        # Check for complexity keywords
        for level, keywords in self.complexity_indicators.items():
            for keyword in keywords:
                if keyword in text:
                    if level == "moderate":
                        complexity_score += 1
                        factors.append("moderate_operation")
                    elif level == "complex":
                        complexity_score += 2
                        factors.append("complex_operation")
                    elif level == "very_complex":
                        complexity_score += 3
                        factors.append("very_complex_operation")
                    break
        
        # Additional complexity factors
        complexity_words = {
            'comprehensive': 2,
            'complete': 1,
            'full': 1,
            'entire': 2,
            'all': 1,
            'everything': 2,
            'system': 2,
            'architecture': 3,
            'framework': 2,
            'integration': 2,
            'migration': 3,
            'security': 2,
            'performance': 2,
            'scalability': 3
        }
        
        for word, score_add in complexity_words.items():
            if word in text:
                complexity_score += score_add
                factors.append(f"mentions_{word}")
        
        return min(complexity_score, 10), factors  # Cap at 10
    
    def _validate_command(self, command_type: CommandType, action: str, target: str,
                         parameters: Dict[str, Any], file_references: List[FileReference]) -> tuple[bool, Optional[str]]:
        """Validate that the parsed command is valid and complete"""
        
        # Check for empty or invalid components
        if not action:
            return False, "No action specified"
        
        if command_type == CommandType.UNKNOWN:
            return False, "Could not determine command type"
        
        # File operation validation
        if command_type == CommandType.FILE_OPERATION:
            if not target and not file_references:
                return False, "File operation requires a file target"
        
        # Shell command validation
        if command_type == CommandType.SHELL_COMMAND:
            if not target:
                return False, "Shell command requires a command to execute"
        
        return True, None
    
    def _calculate_confidence(self, command_type: CommandType, intent: str, 
                            file_references: List[FileReference]) -> float:
        """Calculate confidence score for the parsing"""
        confidence = 0.8  # Base confidence
        
        # Increase confidence for clear command types
        if command_type != CommandType.UNKNOWN:
            confidence += 0.1
        
        # Increase confidence for file references with valid extensions
        if file_references:
            valid_refs = sum(1 for ref in file_references if ref.file_type)
            confidence += min(0.1 * valid_refs, 0.2)
        
        return min(confidence, 1.0)
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for command parser"""
        return {"status": "healthy", "message": "Command parser operational"}