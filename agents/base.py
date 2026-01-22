"""Base Agent definitions using the official Google ADK library."""
from typing import Any, Dict, List, Optional, Union
import asyncio
import os

# Official ADK Imports
from google.adk.agents import (
    BaseAgent, 
    LlmAgent, 
    SequentialAgent, 
    ParallelAgent, 
    InvocationContext
)
from google.adk import Runner
from google.adk.sessions.session import Session
from google.adk.events.event import Event
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService

import config
from context.models import ProjectState

# Configure LiteLLM for OpenAI support within ADK
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY

def create_adk_session(state: ProjectState) -> Session:
    """Bridges our ProjectState to an ADK Session."""
    session = Session(
        app_name="MetaForge",
        user_id="default_user",
        id=state.project_id
    )
    
    if hasattr(state, 'adk_state'):
        session.state.update(state.adk_state)
    else:
        session.state["project_id"] = state.project_id
        
    if hasattr(state, 'adk_events'):
        session.events = state.adk_events
        
    return session

class MetaForgeRunner:
    """Wrapper for the official ADK Runner to interact with NiceGUI."""
    def __init__(self, root_agent: BaseAgent):
        # Runner requires session_service and artifact_service
        self.session_service = InMemorySessionService()
        self.artifact_service = InMemoryArtifactService()
        
        self.runner = Runner(
            app_name="MetaForge",
            agent=root_agent,
            session_service=self.session_service,
            artifact_service=self.artifact_service
        )
        self.root_agent = root_agent
        
    async def run(self, problem: str, session: Session):
        """Executes the ADK pipeline and yields events for the UI."""
        # Manual registration in InMemorySessionService
        app_name = session.app_name
        user_id = session.user_id
        session_id = session.id
        
        if app_name not in self.session_service.sessions:
            self.session_service.sessions[app_name] = {}
        if user_id not in self.session_service.sessions[app_name]:
            self.session_service.sessions[app_name][user_id] = {}
            
        self.session_service.sessions[app_name][user_id][session_id] = session
        
        # The official Runner.run_async() yields events
        from google.genai import types
        msg_content = types.Content(
            role="user",
            parts=[types.Part(text=problem)]
        )
        
        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=msg_content
        ):
            yield event
