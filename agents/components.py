"""Specialized Agents implementation using the official Google ADK."""
from .base import LlmAgent
from context.models import RequirementSpec, FileList, ProgressStatus
import config

# Use the 'openai/' prefix for LiteLLM resolution in ADK
MODEL_ID = f"openai/{config.MODEL_NAME}"

class PlannerAgent(LlmAgent):
    """Agent responsible for requirements analysis and planning."""
    
    def __init__(self):
        super().__init__(
            name="Planner",
            description="Analyzes requirements and creates a technical plan",
            instruction=config.REQUIREMENTS_ANALYZER_PROMPT,
            model=MODEL_ID,
            output_key="requirements",
            output_schema=RequirementSpec
        )

class FrontendAgent(LlmAgent):
    """Agent responsible for generating frontend code."""
    
    def __init__(self):
        super().__init__(
            name="FrontendCoder",
            description="Generates React frontend code",
            instruction=config.FRONTEND_GENERATOR_PROMPT,
            model=MODEL_ID,
            output_key="frontend_files",
            output_schema=FileList
        )

class BackendAgent(LlmAgent):
    """Agent responsible for generating backend code."""
    
    def __init__(self):
        super().__init__(
            name="BackendCoder",
            description="Generates Flask/FastAPI backend code",
            instruction=config.BACKEND_GENERATOR_PROMPT,
            model=MODEL_ID,
            output_key="backend_files",
            output_schema=FileList
        )
