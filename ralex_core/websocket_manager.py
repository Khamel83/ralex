"""
WebSocket Manager for Ralex V3

Manages WebSocket connections for real-time updates including:
- Budget updates
- Typing indicators  
- Session status changes
- File context updates
- System notifications
"""

import json
import uuid
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Set, Any, Optional, Callable
from enum import Enum

from fastapi import WebSocket, WebSocketDisconnect


class MessageType(Enum):
    """WebSocket message types"""
    BUDGET_UPDATE = "budget_update"
    TYPING_INDICATOR = "typing_indicator"
    SESSION_INFO = "session_info"
    FILE_CONTEXT_UPDATE = "file_context_update"
    SYSTEM_NOTIFICATION = "system_notification"
    ERROR = "error"
    PING = "ping"
    PONG = "pong"
    MODEL_SELECTION = "model_selection"
    PROCESSING_STATUS = "processing_status"


class ConnectionInfo:
    """Information about a WebSocket connection"""
    
    def __init__(self, connection_id: str, websocket: WebSocket, session_id: str):
        self.connection_id = connection_id
        self.websocket = websocket
        self.session_id = session_id
        self.connected_at = datetime.now()
        self.last_ping = datetime.now()
        self.is_alive = True
        self.user_agent = ""
        self.ip_address = ""
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "connection_id": self.connection_id,
            "session_id": self.session_id,
            "connected_at": self.connected_at.isoformat(),
            "last_ping": self.last_ping.isoformat(),
            "is_alive": self.is_alive,
            "user_agent": self.user_agent,
            "ip_address": self.ip_address
        }


class WebSocketManager:
    """Manages WebSocket connections for real-time communication"""
    
    def __init__(self):
        # Connection management
        self.active_connections: Dict[str, ConnectionInfo] = {}
        self.session_connections: Dict[str, Set[str]] = {}
        
        # Event handlers
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        # Metrics
        self.total_connections = 0
        self.total_messages_sent = 0
        self.total_messages_received = 0
        
        # Background tasks
        self.heartbeat_task = None
        self.cleanup_task = None
        
        # Logger
        self.logger = logging.getLogger(__name__)
    
    async def connect(self, websocket: WebSocket, session_id: str, 
                     user_agent: str = "", ip_address: str = "") -> str:
        """Accept WebSocket connection and return connection ID"""
        try:
            await websocket.accept()
            connection_id = str(uuid.uuid4())
            
            # Create connection info
            conn_info = ConnectionInfo(connection_id, websocket, session_id)
            conn_info.user_agent = user_agent
            conn_info.ip_address = ip_address
            
            # Store connection
            self.active_connections[connection_id] = conn_info
            
            # Add to session connections
            if session_id not in self.session_connections:
                self.session_connections[session_id] = set()
            self.session_connections[session_id].add(connection_id)
            
            # Update metrics
            self.total_connections += 1
            
            self.logger.info(f"WebSocket connected: {connection_id} for session {session_id}")
            
            # Send initial connection info
            await self.send_to_connection(connection_id, {
                "type": MessageType.SESSION_INFO.value,
                "data": {
                    "connection_id": connection_id,
                    "session_id": session_id,
                    "server_time": datetime.now().isoformat(),
                    "message": "Connected to Ralex V3"
                }
            })
            
            # Trigger connection event
            await self._trigger_event("connection_opened", {
                "connection_id": connection_id,
                "session_id": session_id
            })
            
            return connection_id
            
        except Exception as e:
            self.logger.error(f"Error accepting WebSocket connection: {e}")
            raise
    
    async def disconnect(self, connection_id: str, code: int = 1000, reason: str = ""):
        """Disconnect WebSocket"""
        if connection_id not in self.active_connections:
            return
        
        conn_info = self.active_connections[connection_id]
        session_id = conn_info.session_id
        
        try:
            # Close WebSocket
            if conn_info.is_alive:
                await conn_info.websocket.close(code, reason)
            
            # Remove from active connections
            del self.active_connections[connection_id]
            
            # Remove from session connections
            if session_id in self.session_connections:
                self.session_connections[session_id].discard(connection_id)
                if not self.session_connections[session_id]:
                    del self.session_connections[session_id]
            
            self.logger.info(f"WebSocket disconnected: {connection_id} from session {session_id}")
            
            # Trigger disconnection event
            await self._trigger_event("connection_closed", {
                "connection_id": connection_id,
                "session_id": session_id,
                "code": code,
                "reason": reason
            })
            
        except Exception as e:
            self.logger.error(f"Error disconnecting WebSocket {connection_id}: {e}")
    
    async def send_to_connection(self, connection_id: str, message: Dict[str, Any]) -> bool:
        """Send message to specific connection"""
        if connection_id not in self.active_connections:
            return False
        
        conn_info = self.active_connections[connection_id]
        
        try:
            # Add metadata to message
            if "metadata" not in message:
                message["metadata"] = {}
            message["metadata"]["timestamp"] = datetime.now().isoformat()
            message["metadata"]["connection_id"] = connection_id
            
            # Send message
            await conn_info.websocket.send_text(json.dumps(message))
            self.total_messages_sent += 1
            
            return True
            
        except WebSocketDisconnect:
            # Connection was closed
            await self.disconnect(connection_id, 1001, "Client disconnected")
            return False
        except Exception as e:
            self.logger.error(f"Error sending message to {connection_id}: {e}")
            await self.disconnect(connection_id, 1011, f"Send error: {e}")
            return False
    
    async def send_to_session(self, session_id: str, message: Dict[str, Any]) -> int:
        """Send message to all connections in a session"""
        if session_id not in self.session_connections:
            return 0
        
        connection_ids = list(self.session_connections[session_id])
        successful_sends = 0
        
        for connection_id in connection_ids:
            if await self.send_to_connection(connection_id, message):
                successful_sends += 1
        
        return successful_sends
    
    async def broadcast(self, message: Dict[str, Any], exclude_sessions: Set[str] = None) -> int:
        """Broadcast message to all active connections"""
        exclude_sessions = exclude_sessions or set()
        successful_sends = 0
        
        for connection_id, conn_info in list(self.active_connections.items()):
            if conn_info.session_id not in exclude_sessions:
                if await self.send_to_connection(connection_id, message):
                    successful_sends += 1
        
        return successful_sends
    
    async def handle_client_message(self, connection_id: str, raw_message: str):
        """Handle message received from client"""
        if connection_id not in self.active_connections:
            return
        
        conn_info = self.active_connections[connection_id]
        
        try:
            message = json.loads(raw_message)
            message_type = message.get("type")
            data = message.get("data", {})
            
            self.total_messages_received += 1
            
            # Update last ping time
            conn_info.last_ping = datetime.now()
            
            # Handle different message types
            if message_type == MessageType.PING.value:
                await self.send_to_connection(connection_id, {
                    "type": MessageType.PONG.value,
                    "data": {"timestamp": datetime.now().isoformat()}
                })
            
            elif message_type == "budget_add":
                # Handle budget addition request
                amount = float(data.get("amount", 0))
                await self._trigger_event("budget_add_request", {
                    "connection_id": connection_id,
                    "session_id": conn_info.session_id,
                    "amount": amount
                })
            
            elif message_type == "file_add":
                # Handle file context addition
                file_path = data.get("file_path", "")
                await self._trigger_event("file_add_request", {
                    "connection_id": connection_id,
                    "session_id": conn_info.session_id,
                    "file_path": file_path
                })
            
            elif message_type == "session_info_request":
                # Send session information
                await self._trigger_event("session_info_request", {
                    "connection_id": connection_id,
                    "session_id": conn_info.session_id
                })
            
            else:
                # Unknown message type
                await self.send_to_connection(connection_id, {
                    "type": MessageType.ERROR.value,
                    "data": {
                        "error": f"Unknown message type: {message_type}",
                        "received_message": message
                    }
                })
        
        except json.JSONDecodeError:
            await self.send_to_connection(connection_id, {
                "type": MessageType.ERROR.value,
                "data": {"error": "Invalid JSON format"}
            })
        except Exception as e:
            self.logger.error(f"Error handling client message from {connection_id}: {e}")
            await self.send_to_connection(connection_id, {
                "type": MessageType.ERROR.value,
                "data": {"error": f"Message handling error: {str(e)}"}
            })
    
    # Convenience methods for specific message types
    
    async def send_budget_update(self, session_id: str, budget_data: Dict[str, Any]) -> int:
        """Send budget update to session"""
        return await self.send_to_session(session_id, {
            "type": MessageType.BUDGET_UPDATE.value,
            "data": budget_data
        })
    
    async def send_typing_indicator(self, session_id: str, is_typing: bool, 
                                  model: str = "", message: str = "") -> int:
        """Send typing indicator to session"""
        return await self.send_to_session(session_id, {
            "type": MessageType.TYPING_INDICATOR.value,
            "data": {
                "is_typing": is_typing,
                "model": model,
                "message": message
            }
        })
    
    async def send_model_selection(self, session_id: str, model: str, 
                                 reasoning: str = "", estimated_cost: float = 0) -> int:
        """Send model selection info to session"""
        return await self.send_to_session(session_id, {
            "type": MessageType.MODEL_SELECTION.value,
            "data": {
                "model": model,
                "reasoning": reasoning,
                "estimated_cost": estimated_cost,
                "timestamp": datetime.now().isoformat()
            }
        })
    
    async def send_processing_status(self, session_id: str, status: str, 
                                   progress: float = 0, message: str = "") -> int:
        """Send processing status to session"""
        return await self.send_to_session(session_id, {
            "type": MessageType.PROCESSING_STATUS.value,
            "data": {
                "status": status,
                "progress": progress,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
        })
    
    async def send_system_notification(self, session_id: str, notification: str, 
                                     level: str = "info", action_required: bool = False) -> int:
        """Send system notification to session"""
        return await self.send_to_session(session_id, {
            "type": MessageType.SYSTEM_NOTIFICATION.value,
            "data": {
                "message": notification,
                "level": level,  # info, warning, error, success
                "action_required": action_required,
                "timestamp": datetime.now().isoformat()
            }
        })
    
    # Event handling
    
    def on(self, event: str, handler: Callable):
        """Register event handler"""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    async def _trigger_event(self, event: str, data: Dict[str, Any]):
        """Trigger event handlers"""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(data)
                    else:
                        handler(data)
                except Exception as e:
                    self.logger.error(f"Error in event handler for {event}: {e}")
    
    # Management methods
    
    def get_connection_info(self, connection_id: str) -> Optional[Dict[str, Any]]:
        """Get connection information"""
        if connection_id in self.active_connections:
            return self.active_connections[connection_id].to_dict()
        return None
    
    def get_session_connections(self, session_id: str) -> List[str]:
        """Get all connection IDs for a session"""
        return list(self.session_connections.get(session_id, set()))
    
    def get_active_sessions(self) -> List[str]:
        """Get all active session IDs"""
        return list(self.session_connections.keys())
    
    def get_stats(self) -> Dict[str, Any]:
        """Get WebSocket manager statistics"""
        return {
            "active_connections": len(self.active_connections),
            "active_sessions": len(self.session_connections),
            "total_connections": self.total_connections,
            "messages_sent": self.total_messages_sent,
            "messages_received": self.total_messages_received,
            "uptime": (datetime.now() - datetime.now()).total_seconds()  # Would track actual uptime
        }
    
    async def cleanup_dead_connections(self):
        """Remove dead connections"""
        dead_connections = []
        
        for connection_id, conn_info in list(self.active_connections.items()):
            try:
                # Try to send a ping
                await conn_info.websocket.ping()
            except:
                # Connection is dead
                dead_connections.append(connection_id)
        
        # Clean up dead connections
        for connection_id in dead_connections:
            await self.disconnect(connection_id, 1006, "Connection dead")
        
        if dead_connections:
            self.logger.info(f"Cleaned up {len(dead_connections)} dead connections")
    
    async def start_background_tasks(self):
        """Start background maintenance tasks"""
        async def heartbeat_worker():
            while True:
                try:
                    await self.cleanup_dead_connections()
                    await asyncio.sleep(30)  # Check every 30 seconds
                except Exception as e:
                    self.logger.error(f"Heartbeat worker error: {e}")
                    await asyncio.sleep(60)
        
        # Start heartbeat task
        self.heartbeat_task = asyncio.create_task(heartbeat_worker())
    
    async def shutdown(self):
        """Shutdown WebSocket manager"""
        # Cancel background tasks
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
        
        # Close all connections
        for connection_id in list(self.active_connections.keys()):
            await self.disconnect(connection_id, 1001, "Server shutdown")
        
        self.logger.info("WebSocket manager shutdown complete")


# Global WebSocket manager instance
websocket_manager = WebSocketManager()