"""
Web Session Management for Ralex V3

Manages web sessions, conversation history, and user context with
integration for budget tracking and file context management.
"""

import uuid
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import threading
import time

from ralex_core.agentos_web_integration import AgentOSWebIntegration, WebFileContext


@dataclass
class ConversationMessage:
    """Represents a single message in conversation"""
    id: str
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: str
    metadata: Dict[str, Any]
    cost: float = 0.0
    model: str = ""
    tokens: int = 0


@dataclass 
class SessionBudget:
    """Budget tracking for a session"""
    initial: float
    current_limit: float
    spent: float
    transactions: List[Dict[str, Any]]
    daily_limit: float = 50.0
    warning_threshold: float = 0.8  # Warn at 80% of budget
    
    @property
    def remaining(self) -> float:
        return max(0.0, self.current_limit - self.spent)
    
    @property
    def percentage_used(self) -> float:
        if self.current_limit <= 0:
            return 100.0
        return (self.spent / self.current_limit) * 100.0
    
    @property
    def is_low(self) -> bool:
        return self.percentage_used >= (self.warning_threshold * 100)
    
    @property
    def is_exhausted(self) -> bool:
        return self.remaining <= 0.01  # Allow small rounding errors


class WebSession:
    """Represents a web session with conversation and context"""
    
    def __init__(self, session_id: str, initial_budget: float = 5.0):
        self.id = session_id
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.conversation: List[ConversationMessage] = []
        self.budget = SessionBudget(
            initial=initial_budget,
            current_limit=initial_budget,
            spent=0.0,
            transactions=[]
        )
        self.file_context = WebFileContext()
        self.user_preferences = {}
        self.session_metadata = {}
        self.is_active = True
        
        # Performance tracking
        self.total_requests = 0
        self.total_response_time = 0.0
        self.average_response_time = 0.0
    
    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None, 
                   cost: float = 0.0, model: str = "", tokens: int = 0) -> str:
        """Add message to conversation history"""
        message_id = str(uuid.uuid4())[:8]
        
        message = ConversationMessage(
            id=message_id,
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {},
            cost=cost,
            model=model,
            tokens=tokens
        )
        
        self.conversation.append(message)
        self.last_activity = datetime.now()
        
        # Update budget if there's a cost
        if cost > 0:
            self.charge_budget(cost, model, f"Message {message_id}", tokens)
        
        return message_id
    
    def charge_budget(self, cost: float, model: str, description: str, tokens: int = 0):
        """Charge cost to session budget"""
        self.budget.spent += cost
        
        transaction = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now().isoformat(),
            "cost": cost,
            "model": model,
            "description": description,
            "tokens": tokens
        }
        
        self.budget.transactions.append(transaction)
        
        # Keep only last 50 transactions
        if len(self.budget.transactions) > 50:
            self.budget.transactions = self.budget.transactions[-50:]
    
    def add_budget(self, amount: float) -> float:
        """Add budget to session"""
        self.budget.current_limit += amount
        self.last_activity = datetime.now()
        
        # Log budget addition
        transaction = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now().isoformat(),
            "cost": -amount,  # Negative cost for budget addition
            "model": "system",
            "description": f"Budget added: ${amount:.2f}",
            "tokens": 0
        }
        self.budget.transactions.append(transaction)
        
        return self.budget.remaining
    
    def get_conversation_context(self, max_messages: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation context for AI"""
        recent_messages = self.conversation[-max_messages:] if self.conversation else []
        
        context = []
        for msg in recent_messages:
            if msg.role in ['user', 'assistant']:  # Skip system messages
                context.append({
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp
                })
        
        return context
    
    def update_performance_metrics(self, response_time: float):
        """Update session performance metrics"""
        self.total_requests += 1
        self.total_response_time += response_time
        self.average_response_time = self.total_response_time / self.total_requests
        self.last_activity = datetime.now()
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get session summary for display"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "messages": len(self.conversation),
            "budget": {
                "initial": self.budget.initial,
                "remaining": self.budget.remaining,
                "spent": self.budget.spent,
                "percentage_used": self.budget.percentage_used,
                "is_low": self.budget.is_low,
                "is_exhausted": self.budget.is_exhausted
            },
            "files_in_context": len(self.file_context.files),
            "performance": {
                "total_requests": self.total_requests,
                "average_response_time": round(self.average_response_time, 3)
            }
        }
    
    def is_expired(self, max_age_hours: int = 24) -> bool:
        """Check if session has expired"""
        age = datetime.now() - self.last_activity
        return age > timedelta(hours=max_age_hours)


class WebSessionManager:
    """Manages multiple web sessions"""
    
    def __init__(self, agentos_integration: AgentOSWebIntegration = None):
        self.sessions: Dict[str, WebSession] = {}
        self.agentos = agentos_integration or AgentOSWebIntegration()
        self.cleanup_thread = None
        self.running = True
        self._lock = threading.Lock()
        
        # Start cleanup thread
        self.start_cleanup_thread()
    
    def create_session(self, user_id: str = None, initial_budget: float = 5.0) -> str:
        """Create new session"""
        if user_id:
            session_id = f"user_{user_id}_{int(time.time())}"
        else:
            session_id = f"session_{uuid.uuid4().hex[:12]}"
        
        with self._lock:
            session = WebSession(session_id, initial_budget)
            self.sessions[session_id] = session
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[WebSession]:
        """Get session by ID"""
        with self._lock:
            return self.sessions.get(session_id)
    
    def get_or_create_session(self, session_id: str = None, initial_budget: float = 5.0) -> Tuple[str, WebSession]:
        """Get existing session or create new one"""
        if session_id and session_id in self.sessions:
            session = self.sessions[session_id]
            if not session.is_expired():
                return session_id, session
        
        # Create new session
        new_session_id = self.create_session(initial_budget=initial_budget)
        return new_session_id, self.sessions[new_session_id]
    
    def update_session_activity(self, session_id: str):
        """Update last activity timestamp"""
        with self._lock:
            if session_id in self.sessions:
                self.sessions[session_id].last_activity = datetime.now()
    
    def get_session_budget_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get budget status for session"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        return {
            "session_id": session_id,
            "remaining": session.budget.remaining,
            "spent": session.budget.spent,
            "limit": session.budget.current_limit,
            "percentage_used": session.budget.percentage_used,
            "is_low": session.budget.is_low,
            "is_exhausted": session.budget.is_exhausted,
            "recent_transactions": session.budget.transactions[-5:],  # Last 5 transactions
            "transaction_count": len(session.budget.transactions)
        }
    
    def add_budget_to_session(self, session_id: str, amount: float) -> Optional[Dict[str, Any]]:
        """Add budget to session"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        remaining = session.add_budget(amount)
        
        return {
            "session_id": session_id,
            "amount_added": amount,
            "new_remaining": remaining,
            "new_limit": session.budget.current_limit
        }
    
    def charge_session(self, session_id: str, cost: float, model: str, 
                      description: str, tokens: int = 0) -> bool:
        """Charge cost to session budget"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        # Check if session can afford the cost
        if session.budget.remaining < cost:
            return False
        
        session.charge_budget(cost, model, description, tokens)
        return True
    
    def can_afford(self, session_id: str, estimated_cost: float) -> bool:
        """Check if session can afford estimated cost"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        return session.budget.remaining >= estimated_cost
    
    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs"""
        with self._lock:
            return [sid for sid, session in self.sessions.items() 
                   if session.is_active and not session.is_expired()]
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get overall session statistics"""
        with self._lock:
            total_sessions = len(self.sessions)
            active_sessions = len(self.get_active_sessions())
            
            total_budget_spent = sum(s.budget.spent for s in self.sessions.values())
            total_messages = sum(len(s.conversation) for s in self.sessions.values())
            
            return {
                "total_sessions": total_sessions,
                "active_sessions": active_sessions,
                "total_budget_spent": round(total_budget_spent, 3),
                "total_messages": total_messages,
                "average_messages_per_session": round(total_messages / max(total_sessions, 1), 1)
            }
    
    def cleanup_expired_sessions(self, max_age_hours: int = 24):
        """Remove expired sessions"""
        expired_sessions = []
        
        with self._lock:
            for session_id, session in list(self.sessions.items()):
                if session.is_expired(max_age_hours):
                    expired_sessions.append(session_id)
                    del self.sessions[session_id]
        
        if expired_sessions:
            print(f"Cleaned up {len(expired_sessions)} expired sessions")
    
    def start_cleanup_thread(self):
        """Start background thread for session cleanup"""
        def cleanup_worker():
            while self.running:
                try:
                    self.cleanup_expired_sessions()
                    time.sleep(3600)  # Run every hour
                except Exception as e:
                    print(f"Session cleanup error: {e}")
                    time.sleep(300)  # Wait 5 minutes on error
        
        self.cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        self.cleanup_thread.start()
    
    def shutdown(self):
        """Shutdown session manager"""
        self.running = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=5)
    
    def export_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Export session data for backup/analysis"""
        session = self.get_session(session_id)
        if not session:
            return None
        
        return {
            "session_id": session_id,
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
            "conversation": [asdict(msg) for msg in session.conversation],
            "budget": asdict(session.budget),
            "file_context": {
                "files": dict(session.file_context.files),
                "recent_files": list(session.file_context.recent_files)
            },
            "performance": {
                "total_requests": session.total_requests,
                "average_response_time": session.average_response_time
            }
        }


# Global session manager instance
session_manager = WebSessionManager()