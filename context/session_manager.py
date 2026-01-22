"""Session manager for orchestration context"""
from typing import Dict, Optional
import uuid
from .models import ProjectState, ProblemStatement, ProgressStatus


class SessionManager:
    """Manages project sessions and state"""
    
    def __init__(self):
        self.sessions: Dict[str, ProjectState] = {}
        self.current_session_id: Optional[str] = None
    
    def create_session(self, problem_statement: ProblemStatement) -> str:
        """Create a new project session"""
        session_id = str(uuid.uuid4())
        
        project_state = ProjectState(
            project_id=session_id,
            problem_statement=problem_statement
        )
        
        self.sessions[session_id] = project_state
        self.current_session_id = session_id
        
        return session_id
    
    def get_session(self, session_id: Optional[str] = None) -> Optional[ProjectState]:
        """Get a project session by ID, or current session if no ID provided"""
        if session_id is None:
            session_id = self.current_session_id
        
        return self.sessions.get(session_id) if session_id else None
    
    def update_progress(self, step_name: str, status: ProgressStatus, details: Optional[str] = None):
        """Update progress for current session"""
        session = self.get_session()
        if session:
            session.update_progress(step_name, status, details)
    
    def get_all_sessions(self) -> Dict[str, ProjectState]:
        """Get all sessions"""
        return self.sessions
    
    def clear_session(self, session_id: str):
        """Clear a specific session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            if self.current_session_id == session_id:
                self.current_session_id = None


# Global session manager instance
session_manager = SessionManager()
