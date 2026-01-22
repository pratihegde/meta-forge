"""Pydantic models for MetaForge context management"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum


class ProgressStatus(str, Enum):
    """Status of a progress step"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"


class ProblemStatement(BaseModel):
    """User's problem statement input"""
    description: str
    tech_preferences: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class TechStack(BaseModel):
    """Technical stack selection"""
    model_config = ConfigDict(extra='forbid')
    frontend: str
    backend: str
    database: str

class RequirementSpec(BaseModel):
    """Parsed and structured requirements"""
    model_config = ConfigDict(extra='forbid')
    functional_components: List[str]
    tech_stack: TechStack
    clarifications: List[str]
    complexity: str


class GeneratedFile(BaseModel):
    """A single generated file"""
    model_config = ConfigDict(extra='forbid')
    path: str
    content: str
    language: str
    size: int
    
    def __init__(self, **data):
        super().__init__(**data)
        self.size = len(self.content)


class FileList(BaseModel):
    """A list of generated files for structured output"""
    model_config = ConfigDict(extra='forbid')
    files: List[GeneratedFile]


class ValidationResult(BaseModel):
    """Result of code validation"""
    passed: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


class ProgressStep(BaseModel):
    """A single progress step in the orchestration"""
    name: str
    status: ProgressStatus = ProgressStatus.PENDING
    timestamp: datetime = Field(default_factory=datetime.now)
    details: Optional[str] = None


class ProjectState(BaseModel):
    """Complete state of a generated project"""
    project_id: str
    problem_statement: ProblemStatement
    requirements: Optional[RequirementSpec] = None
    files: List[GeneratedFile] = []
    validation: Optional[ValidationResult] = None
    progress_steps: List[ProgressStep] = []
    adk_state: Dict[str, Any] = Field(default_factory=dict)
    adk_events: List[Any] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def update_progress(self, step_name: str, status: ProgressStatus, details: Optional[str] = None):
        """Update or add a progress step"""
        for step in self.progress_steps:
            if step.name == step_name:
                step.status = status
                step.timestamp = datetime.now()
                if details:
                    step.details = details
                self.updated_at = datetime.now()
                return
        
        # Add new step if not found
        self.progress_steps.append(
            ProgressStep(name=step_name, status=status, details=details)
        )
        self.updated_at = datetime.now()
