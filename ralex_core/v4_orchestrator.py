"""
Ralex V4 Orchestrator - Central coordination engine for voice-driven AI development

This module serves as the main orchestrator that coordinates all V4 components:
- OpenCode.ai for file operations and shell commands
- LiteLLM for intelligent model routing
- AgentOS for prompt enhancement and standards
- Context7 for dynamic documentation
- Context management for persistent intelligence
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# Import V4 components (will be implemented in subsequent tasks)
from ralex_core.context_manager import ContextManager
from ralex_core.command_parser import CommandParser
from ralex_core.agentos_v4_integration import AgentOSV4Enhancer
from ralex_core.litellm_v4_router import LiteLLMV4Router
from ralex_core.opencode_client import OpenCodeClient
from ralex_core.security_manager import SecurityManager
from ralex_core.workflow_engine import WorkflowEngine
from ralex_core.error_handler import ErrorHandler


class ProcessingStatus(Enum):
    """Status codes for processing results"""
    SUCCESS = "success"
    ERROR = "error"
    BLOCKED = "blocked"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"


@dataclass
class ProcessingResult:
    """Result of voice command processing"""
    status: ProcessingStatus
    message: str
    data: Dict[str, Any]
    execution_time: float
    cost: float
    context_updates: Dict[str, Any]
    
    @classmethod
    def success(cls, data: Dict[str, Any], message: str = "Command executed successfully", 
                execution_time: float = 0.0, cost: float = 0.0, 
                context_updates: Dict[str, Any] = None) -> 'ProcessingResult':
        return cls(
            status=ProcessingStatus.SUCCESS,
            message=message,
            data=data,
            execution_time=execution_time,
            cost=cost,
            context_updates=context_updates or {}
        )
    
    @classmethod
    def error(cls, message: str, data: Dict[str, Any] = None, 
              execution_time: float = 0.0) -> 'ProcessingResult':
        return cls(
            status=ProcessingStatus.ERROR,
            message=message,
            data=data or {},
            execution_time=execution_time,
            cost=0.0,
            context_updates={}
        )
    
    @classmethod
    def blocked(cls, reason: str, data: Dict[str, Any] = None) -> 'ProcessingResult':
        return cls(
            status=ProcessingStatus.BLOCKED,
            message=f"Command blocked: {reason}",
            data=data or {},
            execution_time=0.0,
            cost=0.0,
            context_updates={}
        )


class RalexV4Orchestrator:
    """
    Central orchestration engine for Ralex V4
    
    Coordinates all components in the V4 architecture:
    - Voice command processing and validation
    - Context loading and management
    - AgentOS enhancement pipeline
    - LiteLLM model routing
    - OpenCode execution
    - Results processing and context updates
    """
    
    def __init__(self, project_path: str = None):
        """Initialize the V4 orchestrator with all components"""
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.logger = logging.getLogger(__name__)
        
        # Initialize core components
        self.context_manager = ContextManager(self.project_path)
        self.command_parser = CommandParser()
        self.agentos_enhancer = AgentOSV4Enhancer()
        self.litellm_router = LiteLLMV4Router()
        self.opencode_client = OpenCodeClient(self.project_path)
        self.security_manager = SecurityManager(self.project_path)
        self.workflow_engine = WorkflowEngine()
        self.error_handler = ErrorHandler()
        
        # Processing state
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.processing_queue: List[Dict[str, Any]] = []
        self.is_initialized = False
        
        self.logger.info("Ralex V4 Orchestrator initialized")
    
    async def initialize(self) -> bool:
        """Initialize all components and verify system readiness"""
        try:
            self.logger.info("Initializing Ralex V4 Orchestrator...")
            
            # Initialize components in order
            await self.context_manager.initialize()
            await self.agentos_enhancer.initialize()
            await self.litellm_router.initialize()
            await self.opencode_client.initialize()
            await self.security_manager.initialize()
            await self.workflow_engine.initialize()
            
            # Verify system health
            health_check = await self._perform_health_check()
            if not health_check["healthy"]:
                raise Exception(f"Health check failed: {health_check['issues']}")
            
            self.is_initialized = True
            self.logger.info("Ralex V4 Orchestrator initialization complete")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize orchestrator: {e}")
            return False
    
    async def process_voice_command(self, 
                                  command: str, 
                                  session_id: str,
                                  user_context: Dict[str, Any] = None) -> ProcessingResult:
        """
        Main orchestration pipeline for processing voice commands
        
        Args:
            command: Raw voice command text
            session_id: Unique session identifier
            user_context: Additional user context (optional)
            
        Returns:
            ProcessingResult with execution details and results
        """
        start_time = datetime.now()
        
        try:
            if not self.is_initialized:
                return ProcessingResult.error("Orchestrator not initialized")
            
            self.logger.info(f"Processing voice command: '{command}' for session {session_id}")
            
            # Stage 1: Parse and validate command
            parsed_command = await self.command_parser.parse(command)
            if not parsed_command.is_valid:
                return ProcessingResult.error(f"Invalid command: {parsed_command.error}")
            
            # Stage 2: Security validation
            security_check = await self.security_manager.validate_command(
                parsed_command, user_context or {}
            )
            if not security_check.is_safe:
                return ProcessingResult.blocked(security_check.reason, {
                    "command": command,
                    "security_issues": security_check.issues
                })
            
            # Stage 3: Load relevant context
            context_package = await self.context_manager.load_context(
                session_id, parsed_command
            )
            
            # Stage 4: Enhance with AgentOS standards
            enhanced_prompt = await self.agentos_enhancer.enhance(
                parsed_command, context_package
            )
            
            # Stage 5: Route to appropriate model
            model_selection = await self.litellm_router.select_model(
                enhanced_prompt, context_package.complexity
            )
            
            # Stage 6: Execute via OpenCode
            execution_result = await self.opencode_client.execute(
                enhanced_prompt, model_selection, context_package
            )
            
            # Stage 7: Update context with results
            await self.context_manager.update_context(
                session_id, execution_result, parsed_command
            )
            
            # Calculate execution metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Build success result
            result = ProcessingResult.success(
                data={
                    "command": command,
                    "parsed_command": parsed_command.to_dict(),
                    "execution_result": execution_result.to_dict(),
                    "model_used": model_selection.model_name,
                    "context_sources": context_package.get_sources()
                },
                message="Command executed successfully",
                execution_time=execution_time,
                cost=execution_result.cost,
                context_updates=execution_result.context_updates
            )
            
            self.logger.info(f"Command processed successfully in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            error_message = await self.error_handler.handle_error(e, {
                "command": command,
                "session_id": session_id,
                "execution_time": execution_time
            })
            
            self.logger.error(f"Error processing command: {error_message}")
            return ProcessingResult.error(error_message, execution_time=execution_time)
    
    async def execute_workflow(self, 
                             workflow_name: str, 
                             session_id: str,
                             parameters: Dict[str, Any] = None) -> ProcessingResult:
        """
        Execute a predefined automated workflow
        
        Args:
            workflow_name: Name of the workflow to execute
            session_id: Session identifier
            parameters: Workflow parameters
            
        Returns:
            ProcessingResult with workflow execution details
        """
        start_time = datetime.now()
        
        try:
            self.logger.info(f"Executing workflow: {workflow_name} for session {session_id}")
            
            # Load workflow definition
            workflow = await self.workflow_engine.get_workflow(workflow_name)
            if not workflow:
                return ProcessingResult.error(f"Workflow '{workflow_name}' not found")
            
            # Execute workflow steps
            workflow_result = await self.workflow_engine.execute(
                workflow, session_id, parameters or {}
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return ProcessingResult.success(
                data={
                    "workflow": workflow_name,
                    "steps_completed": workflow_result.steps_completed,
                    "results": workflow_result.results
                },
                message=f"Workflow '{workflow_name}' completed successfully",
                execution_time=execution_time,
                cost=workflow_result.total_cost,
                context_updates=workflow_result.context_updates
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            error_message = await self.error_handler.handle_error(e, {
                "workflow": workflow_name,
                "session_id": session_id
            })
            
            return ProcessingResult.error(error_message, execution_time=execution_time)
    
    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get current status and context for a session"""
        try:
            context = await self.context_manager.get_session_context(session_id)
            return {
                "session_id": session_id,
                "status": "active" if session_id in self.active_sessions else "inactive",
                "context_files": len(context.get("files", {})),
                "recent_commands": context.get("recent_commands", [])[:5],
                "budget_remaining": await self.litellm_router.get_session_budget(session_id)
            }
        except Exception as e:
            self.logger.error(f"Error getting session status: {e}")
            return {"session_id": session_id, "status": "error", "error": str(e)}
    
    async def _perform_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check of all components"""
        health_status = {
            "healthy": True,
            "issues": [],
            "components": {}
        }
        
        # Check each component
        components = [
            ("context_manager", self.context_manager),
            ("command_parser", self.command_parser),
            ("agentos_enhancer", self.agentos_enhancer),
            ("litellm_router", self.litellm_router),
            ("opencode_client", self.opencode_client),
            ("security_manager", self.security_manager),
            ("workflow_engine", self.workflow_engine)
        ]
        
        for name, component in components:
            try:
                if hasattr(component, 'health_check'):
                    component_health = await component.health_check()
                else:
                    component_health = {"status": "unknown", "message": "No health check available"}
                
                health_status["components"][name] = component_health
                
                if component_health.get("status") != "healthy":
                    health_status["healthy"] = False
                    health_status["issues"].append(f"{name}: {component_health.get('message', 'Unknown issue')}")
                    
            except Exception as e:
                health_status["healthy"] = False
                health_status["issues"].append(f"{name}: Health check failed - {str(e)}")
                health_status["components"][name] = {"status": "error", "message": str(e)}
        
        return health_status
    
    async def shutdown(self):
        """Gracefully shutdown the orchestrator and all components"""
        try:
            self.logger.info("Shutting down Ralex V4 Orchestrator...")
            
            # Shutdown components in reverse order
            await self.workflow_engine.shutdown()
            await self.security_manager.shutdown()
            await self.opencode_client.shutdown()
            await self.litellm_router.shutdown()
            await self.agentos_enhancer.shutdown()
            await self.context_manager.shutdown()
            
            self.is_initialized = False
            self.logger.info("Ralex V4 Orchestrator shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")


# Global orchestrator instance (will be initialized by main application)
_orchestrator_instance: Optional[RalexV4Orchestrator] = None


def get_orchestrator() -> RalexV4Orchestrator:
    """Get the global orchestrator instance"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = RalexV4Orchestrator()
    return _orchestrator_instance


async def initialize_orchestrator(project_path: str = None) -> bool:
    """Initialize the global orchestrator instance"""
    global _orchestrator_instance
    _orchestrator_instance = RalexV4Orchestrator(project_path)
    return await _orchestrator_instance.initialize()


async def shutdown_orchestrator():
    """Shutdown the global orchestrator instance"""
    global _orchestrator_instance
    if _orchestrator_instance:
        await _orchestrator_instance.shutdown()
        _orchestrator_instance = None