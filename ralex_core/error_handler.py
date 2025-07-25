"""
Error Handler for Ralex V4

Provides comprehensive error handling, recovery mechanisms, and user-friendly
error reporting for all orchestrator components.
"""

import asyncio
import logging
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum
import json


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Categories of errors"""
    PARSING_ERROR = "parsing_error"
    SECURITY_ERROR = "security_error"
    CONTEXT_ERROR = "context_error"
    EXECUTION_ERROR = "execution_error"
    NETWORK_ERROR = "network_error"
    FILESYSTEM_ERROR = "filesystem_error"
    API_ERROR = "api_error"
    CONFIGURATION_ERROR = "configuration_error"
    TIMEOUT_ERROR = "timeout_error"
    UNKNOWN_ERROR = "unknown_error"


@dataclass
class ErrorContext:
    """Context information for error analysis"""
    component: str
    operation: str
    input_data: Dict[str, Any]
    timestamp: datetime
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    additional_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ErrorInfo:
    """Comprehensive error information"""
    error_id: str
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    user_message: str
    details: Dict[str, Any]
    context: ErrorContext
    stacktrace: Optional[str] = None
    recovery_suggestions: List[str] = field(default_factory=list)
    retry_possible: bool = False
    retry_count: int = 0
    max_retries: int = 3


class RetryStrategy:
    """Retry strategy configuration"""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, 
                 exponential_backoff: bool = True, max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.exponential_backoff = exponential_backoff
        self.max_delay = max_delay
    
    def get_delay(self, retry_count: int) -> float:
        """Calculate delay for retry attempt"""
        if self.exponential_backoff:
            delay = self.base_delay * (2 ** retry_count)
            return min(delay, self.max_delay)
        return self.base_delay


class ErrorHandler:
    """
    Comprehensive error handling and recovery system
    
    Features:
    - Error classification and categorization
    - User-friendly error messages
    - Automatic retry with exponential backoff
    - Error context preservation
    - Recovery suggestions
    - Error analytics and reporting
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_history: List[ErrorInfo] = []
        self.retry_strategies: Dict[ErrorCategory, RetryStrategy] = {}
        self.recovery_handlers: Dict[ErrorCategory, Callable] = {}
        self.error_count = 0
        
        # Initialize default retry strategies
        self._initialize_retry_strategies()
        
        # Initialize recovery handlers
        self._initialize_recovery_handlers()
        
        self.logger.info("Error handler initialized")
    
    def _initialize_retry_strategies(self):
        """Initialize default retry strategies for different error categories"""
        self.retry_strategies = {
            ErrorCategory.NETWORK_ERROR: RetryStrategy(max_retries=3, base_delay=2.0),
            ErrorCategory.API_ERROR: RetryStrategy(max_retries=2, base_delay=1.0),
            ErrorCategory.TIMEOUT_ERROR: RetryStrategy(max_retries=2, base_delay=5.0),
            ErrorCategory.EXECUTION_ERROR: RetryStrategy(max_retries=1, base_delay=1.0),
            ErrorCategory.FILESYSTEM_ERROR: RetryStrategy(max_retries=2, base_delay=0.5),
            ErrorCategory.CONTEXT_ERROR: RetryStrategy(max_retries=1, base_delay=0.5),
            ErrorCategory.PARSING_ERROR: RetryStrategy(max_retries=0),  # No retry
            ErrorCategory.SECURITY_ERROR: RetryStrategy(max_retries=0),  # No retry
            ErrorCategory.CONFIGURATION_ERROR: RetryStrategy(max_retries=0),  # No retry
        }
    
    def _initialize_recovery_handlers(self):
        """Initialize recovery handlers for different error categories"""
        self.recovery_handlers = {
            ErrorCategory.CONTEXT_ERROR: self._recover_context_error,
            ErrorCategory.FILESYSTEM_ERROR: self._recover_filesystem_error,
            ErrorCategory.API_ERROR: self._recover_api_error,
            ErrorCategory.NETWORK_ERROR: self._recover_network_error,
        }
    
    async def handle_error(self, exception: Exception, context: Dict[str, Any]) -> str:
        """
        Main error handling entry point
        
        Args:
            exception: The exception that occurred
            context: Context information about the error
            
        Returns:
            User-friendly error message
        """
        try:
            # Generate unique error ID
            error_id = self._generate_error_id()
            
            # Create error context
            error_context = self._create_error_context(context)
            
            # Classify error
            category = self._classify_error(exception)
            severity = self._assess_severity(exception, category)
            
            # Create error info
            error_info = ErrorInfo(
                error_id=error_id,
                category=category,
                severity=severity,
                message=str(exception),
                user_message=self._create_user_message(exception, category),
                details=self._extract_error_details(exception),
                context=error_context,
                stacktrace=traceback.format_exc(),
                recovery_suggestions=self._generate_recovery_suggestions(exception, category),
                retry_possible=self._is_retry_possible(category),
                retry_count=0,
                max_retries=self.retry_strategies.get(category, RetryStrategy()).max_retries
            )
            
            # Store error
            self.error_history.append(error_info)
            self.error_count += 1
            
            # Log error
            self._log_error(error_info)
            
            # Attempt recovery if possible
            if category in self.recovery_handlers:
                try:
                    await self.recovery_handlers[category](error_info)
                except Exception as recovery_error:
                    self.logger.warning(f"Recovery failed for {error_id}: {recovery_error}")
            
            return error_info.user_message
            
        except Exception as handler_error:
            self.logger.error(f"Error in error handler: {handler_error}")
            return "An unexpected error occurred. Please try again."
    
    async def retry_with_backoff(self, operation: Callable, context: Dict[str, Any], 
                               category: ErrorCategory = ErrorCategory.UNKNOWN_ERROR) -> Any:
        """
        Execute operation with retry and exponential backoff
        
        Args:
            operation: Async function to execute
            context: Context for error handling
            category: Error category for retry strategy
            
        Returns:
            Result of successful operation
            
        Raises:
            Last exception if all retries failed
        """
        strategy = self.retry_strategies.get(category, RetryStrategy())
        last_exception = None
        
        for attempt in range(strategy.max_retries + 1):
            try:
                return await operation()
                
            except Exception as e:
                last_exception = e
                
                if attempt < strategy.max_retries:
                    delay = strategy.get_delay(attempt)
                    self.logger.warning(
                        f"Operation failed (attempt {attempt + 1}/{strategy.max_retries + 1}): {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )
                    await asyncio.sleep(delay)
                else:
                    self.logger.error(f"Operation failed after {strategy.max_retries + 1} attempts")
        
        # All retries failed, handle the error
        await self.handle_error(last_exception, context)
        raise last_exception
    
    def _generate_error_id(self) -> str:
        """Generate unique error ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"ERR_{timestamp}_{self.error_count:04d}"
    
    def _create_error_context(self, context: Dict[str, Any]) -> ErrorContext:
        """Create ErrorContext from context dictionary"""
        return ErrorContext(
            component=context.get("component", "unknown"),
            operation=context.get("operation", "unknown"),
            input_data=context.get("input_data", {}),
            timestamp=datetime.now(),
            session_id=context.get("session_id"),
            user_id=context.get("user_id"),
            additional_info=context.get("additional_info", {})
        )
    
    def _classify_error(self, exception: Exception) -> ErrorCategory:
        """Classify error into appropriate category"""
        error_type = type(exception).__name__
        error_message = str(exception).lower()
        
        # Network-related errors
        if any(keyword in error_message for keyword in ["connection", "network", "timeout", "unreachable"]):
            return ErrorCategory.NETWORK_ERROR
        
        # API-related errors
        if any(keyword in error_message for keyword in ["api", "http", "status", "unauthorized", "forbidden"]):
            return ErrorCategory.API_ERROR
        
        # File system errors
        if any(keyword in error_message for keyword in ["file", "directory", "path", "permission", "not found"]):
            return ErrorCategory.FILESYSTEM_ERROR
        
        # Parsing errors
        if any(keyword in error_message for keyword in ["parse", "syntax", "invalid format", "decode"]):
            return ErrorCategory.PARSING_ERROR
        
        # Security errors
        if any(keyword in error_message for keyword in ["security", "permission denied", "access denied", "unauthorized"]):
            return ErrorCategory.SECURITY_ERROR
        
        # Timeout errors
        if "timeout" in error_message or isinstance(exception, asyncio.TimeoutError):
            return ErrorCategory.TIMEOUT_ERROR
        
        # Configuration errors
        if any(keyword in error_message for keyword in ["config", "setting", "environment", "missing"]):
            return ErrorCategory.CONFIGURATION_ERROR
        
        # Context errors
        if any(keyword in error_message for keyword in ["context", "session", "state"]):
            return ErrorCategory.CONTEXT_ERROR
        
        return ErrorCategory.UNKNOWN_ERROR
    
    def _assess_severity(self, exception: Exception, category: ErrorCategory) -> ErrorSeverity:
        """Assess error severity"""
        # Critical errors that stop system operation
        if category in [ErrorCategory.SECURITY_ERROR, ErrorCategory.CONFIGURATION_ERROR]:
            return ErrorSeverity.CRITICAL
        
        # High severity errors that affect core functionality
        if category in [ErrorCategory.EXECUTION_ERROR, ErrorCategory.API_ERROR]:
            return ErrorSeverity.HIGH
        
        # Medium severity errors that affect user experience
        if category in [ErrorCategory.NETWORK_ERROR, ErrorCategory.FILESYSTEM_ERROR]:
            return ErrorSeverity.MEDIUM
        
        # Low severity errors that are recoverable
        return ErrorSeverity.LOW
    
    def _create_user_message(self, exception: Exception, category: ErrorCategory) -> str:
        """Create user-friendly error message"""
        base_messages = {
            ErrorCategory.PARSING_ERROR: "I couldn't understand that command. Please try rephrasing it.",
            ErrorCategory.SECURITY_ERROR: "This operation is not allowed for security reasons.",
            ErrorCategory.CONTEXT_ERROR: "I lost track of the conversation context. Please provide more details.",
            ErrorCategory.EXECUTION_ERROR: "There was an error executing your command.",
            ErrorCategory.NETWORK_ERROR: "I'm having trouble connecting to external services. Please check your internet connection.",
            ErrorCategory.FILESYSTEM_ERROR: "I couldn't access the requested file or directory.",
            ErrorCategory.API_ERROR: "There was an error communicating with the AI service.",
            ErrorCategory.CONFIGURATION_ERROR: "There's a configuration issue that needs to be resolved.",
            ErrorCategory.TIMEOUT_ERROR: "The operation timed out. Please try again.",
            ErrorCategory.UNKNOWN_ERROR: "An unexpected error occurred."
        }
        
        return base_messages.get(category, "An error occurred while processing your request.")
    
    def _extract_error_details(self, exception: Exception) -> Dict[str, Any]:
        """Extract detailed error information"""
        return {
            "type": type(exception).__name__,
            "message": str(exception),
            "args": list(exception.args) if exception.args else [],
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_recovery_suggestions(self, exception: Exception, category: ErrorCategory) -> List[str]:
        """Generate suggestions for error recovery"""
        suggestions = []
        
        if category == ErrorCategory.PARSING_ERROR:
            suggestions = [
                "Try rephrasing your command more clearly",
                "Use simpler language or break down complex requests",
                "Check if file names are spelled correctly"
            ]
        elif category == ErrorCategory.NETWORK_ERROR:
            suggestions = [
                "Check your internet connection",
                "Try again in a few moments",
                "Verify API credentials and endpoints"
            ]
        elif category == ErrorCategory.FILESYSTEM_ERROR:
            suggestions = [
                "Check if the file or directory exists",
                "Verify file permissions",
                "Ensure the path is correct"
            ]
        elif category == ErrorCategory.API_ERROR:
            suggestions = [
                "Check API key and credentials",
                "Verify service availability",
                "Try again after a short delay"
            ]
        elif category == ErrorCategory.CONTEXT_ERROR:
            suggestions = [
                "Provide more specific details about what you want to do",
                "Mention file names or specific functionality",
                "Start a new conversation if context is lost"
            ]
        
        return suggestions
    
    def _is_retry_possible(self, category: ErrorCategory) -> bool:
        """Check if retry is possible for error category"""
        return category in self.retry_strategies and self.retry_strategies[category].max_retries > 0
    
    def _log_error(self, error_info: ErrorInfo):
        """Log error information"""
        log_level = {
            ErrorSeverity.LOW: logging.INFO,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL
        }.get(error_info.severity, logging.ERROR)
        
        self.logger.log(
            log_level,
            f"Error {error_info.error_id} ({error_info.category.value}): {error_info.message}"
        )
        
        if error_info.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
            self.logger.error(f"Stacktrace for {error_info.error_id}:\n{error_info.stacktrace}")
    
    # Recovery handlers
    async def _recover_context_error(self, error_info: ErrorInfo):
        """Attempt to recover from context errors"""
        self.logger.info(f"Attempting context recovery for {error_info.error_id}")
        # Context recovery logic would be implemented here
        pass
    
    async def _recover_filesystem_error(self, error_info: ErrorInfo):
        """Attempt to recover from filesystem errors"""
        self.logger.info(f"Attempting filesystem recovery for {error_info.error_id}")
        # Filesystem recovery logic would be implemented here
        pass
    
    async def _recover_api_error(self, error_info: ErrorInfo):
        """Attempt to recover from API errors"""
        self.logger.info(f"Attempting API recovery for {error_info.error_id}")
        # API recovery logic would be implemented here
        pass
    
    async def _recover_network_error(self, error_info: ErrorInfo):
        """Attempt to recover from network errors"""
        self.logger.info(f"Attempting network recovery for {error_info.error_id}")
        # Network recovery logic would be implemented here
        pass
    
    # Analytics and reporting
    def get_error_statistics(self, time_window: timedelta = None) -> Dict[str, Any]:
        """Get error statistics for analysis"""
        if time_window:
            cutoff_time = datetime.now() - time_window
            relevant_errors = [e for e in self.error_history if e.context.timestamp >= cutoff_time]
        else:
            relevant_errors = self.error_history
        
        if not relevant_errors:
            return {"total_errors": 0}
        
        # Calculate statistics
        category_counts = {}
        severity_counts = {}
        component_counts = {}
        
        for error in relevant_errors:
            category_counts[error.category.value] = category_counts.get(error.category.value, 0) + 1
            severity_counts[error.severity.value] = severity_counts.get(error.severity.value, 0) + 1
            component_counts[error.context.component] = component_counts.get(error.context.component, 0) + 1
        
        return {
            "total_errors": len(relevant_errors),
            "by_category": category_counts,
            "by_severity": severity_counts,
            "by_component": component_counts,
            "time_window": str(time_window) if time_window else "all_time"
        }
    
    def get_recent_errors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent errors for debugging"""
        recent_errors = sorted(self.error_history, key=lambda e: e.context.timestamp, reverse=True)[:limit]
        
        return [
            {
                "error_id": error.error_id,
                "category": error.category.value,
                "severity": error.severity.value,
                "message": error.message,
                "user_message": error.user_message,
                "timestamp": error.context.timestamp.isoformat(),
                "component": error.context.component,
                "retry_count": error.retry_count
            }
            for error in recent_errors
        ]
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for error handler"""
        recent_critical_errors = [
            e for e in self.error_history 
            if e.severity == ErrorSeverity.CRITICAL and 
               e.context.timestamp > datetime.now() - timedelta(minutes=5)
        ]
        
        return {
            "status": "critical" if recent_critical_errors else "healthy",
            "total_errors": len(self.error_history),
            "recent_critical_errors": len(recent_critical_errors),
            "message": "Error handler operational"
        }