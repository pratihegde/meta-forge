"""Orchestrator implementation using official Google ADK library."""
import asyncio
from .base import MetaForgeRunner, create_adk_session, SequentialAgent, ParallelAgent
from .components import PlannerAgent, FrontendAgent, BackendAgent
from context.session_manager import session_manager
from context.models import ProjectState, ProgressStatus, RequirementSpec, FileList

class MetaForgeOrchestrator:
    """The 'Team Leader' agent that orchestrates the entire application build."""
    
    def __init__(self):
        # 1. Define the 'Team' using official ADK Agents
        self.planner = PlannerAgent()
        self.frontend_coder = FrontendAgent()
        self.backend_coder = BackendAgent()
        # NOTE: ADK agents cannot be attached to multiple parents; use distinct instances for refinement.
        self.refine_frontend_coder = FrontendAgent()
        self.refine_backend_coder = BackendAgent()
        
        # 2. Compose the official ADK Workflow
        self.team_pipeline = SequentialAgent(
            name="MetaForgePipeline",
            sub_agents=[
                self.planner,
                ParallelAgent(
                    name="Coders",
                    sub_agents=[self.frontend_coder, self.backend_coder]
                )
            ]
        )

        # Refinement pipeline: skip planner, run only coders
        self.refine_pipeline = ParallelAgent(
            name="RefineCoders",
            sub_agents=[self.refine_frontend_coder, self.refine_backend_coder],
        )
        
        # 3. Setup the official Runner wrapper
        self.runner = MetaForgeRunner(root_agent=self.team_pipeline)
        self.refine_runner = MetaForgeRunner(root_agent=self.refine_pipeline)
        
    async def orchestrate(self, problem_description: str, session_id: str) -> ProjectState:
        """Execute the ADK pipeline using official patterns."""
        state = session_manager.get_session(session_id)
        if not state:
            raise ValueError(f"Session {session_id} not found")
            
        # Bridge to official ADK Session
        adk_session = create_adk_session(state)
        
        try:
            state.update_progress("Starting official ADK Pipeline", ProgressStatus.IN_PROGRESS)
            
            # Execute via official Runner
            async for event in self.runner.run(problem_description, adk_session):
                # Terminal Logging for Visibility
                print(f"[ADK] Agent [{event.author}] is thinking...")
                import sys
                sys.stdout.flush()
                
                # Observability: Log internal ADK events to the progress panel
                if event.author != "user" and event.content:
                     # Correctly extract text from Content object
                     text = ""
                     if hasattr(event.content, 'parts') and event.content.parts:
                          text = "".join(p.text for p in event.content.parts if hasattr(p, 'text') and p.text)
                     
                     if text:
                         print(f"[ADK] {event.author}: {text[:150]}...")
                         sys.stdout.flush()
                         log_msg = f"[{event.author}] {text[:100]}..."
                         state.update_progress(f"ADK: {event.author} active", ProgressStatus.IN_PROGRESS, log_msg)
                
                # Sync results from ADK session state back to our UI state
                
                # Planner output
                if "requirements" in adk_session.state:
                     reqs = adk_session.state["requirements"]
                     if isinstance(reqs, dict):
                          state.requirements = RequirementSpec(**reqs)
                          state.update_progress("Requirements analyzed", ProgressStatus.IN_PROGRESS)
                     else:
                          state.requirements = reqs
                
                # Coder outputs
                all_files = []
                for key in ["frontend_files", "backend_files"]:
                    if key in adk_session.state:
                         val = adk_session.state[key]
                         if isinstance(val, dict):
                              file_list = FileList(**val)
                              all_files.extend(file_list.files)
                              state.update_progress(f"{key.replace('_', ' ').title()} generated", ProgressStatus.IN_PROGRESS)
                         elif hasattr(val, "files"):
                              all_files.extend(val.files)
                
                if all_files:
                    # Smart Merge: Update existing files by path or add new ones
                    current_files_map = {f.path.replace('\\', '/').strip('/'): f for f in state.files}
                    for new_file in all_files:
                         norm_path = new_file.path.replace('\\', '/').strip('/')
                         # Normalize the internal path as well for consistency
                         new_file.path = norm_path
                         current_files_map[norm_path] = new_file
                    
                    state.files = list(current_files_map.values())
            
            # Persist ADK-specific state and history to ProjectState
            state.adk_state = dict(adk_session.state)
            state.adk_events = list(adk_session.events)
                
            state.update_progress("Project Built via Google ADK", ProgressStatus.COMPLETED)
            return state
            
        except Exception as e:
            state.update_progress("ADK Orchestration Failed", ProgressStatus.ERROR, str(e))
            raise

    async def refine(self, instruction: str, session_id: str) -> ProjectState:
        """Handle iterative updates: reuse existing requirements and update code only."""
        state = session_manager.get_session(session_id)
        if not state:
            raise ValueError(f"Session {session_id} not found")
            
        # Continue with the same ADK session state (requirements + prior events)
        adk_session = create_adk_session(state)
        
        # Build a refinement prompt that preserves the existing spec and asks for diffs only.
        existing_reqs = state.requirements.model_dump() if state.requirements else None
        existing_files = [f.path for f in state.files] if state.files else []

        prompt = (
            "You are refining an existing project.\n"
            "Do NOT re-plan the spec; keep requirements as-is.\n"
            "Return ONLY updated/added files that implement the requested change.\n\n"
            f"Existing requirements (JSON): {existing_reqs}\n"
            f"Existing file paths: {existing_files}\n\n"
            f"User change request: {instruction}\n"
        )

        try:
            state.update_progress("Refinement: applying changes", ProgressStatus.IN_PROGRESS)

            async for event in self.refine_runner.run(prompt, adk_session):
                print(f"[ADK] Agent [{event.author}] is thinking...")
                import sys
                sys.stdout.flush()

                if event.author != "user" and event.content:
                    text = ""
                    if hasattr(event.content, 'parts') and event.content.parts:
                        text = "".join(
                            p.text for p in event.content.parts
                            if hasattr(p, 'text') and p.text
                        )
                    if text:
                        log_msg = f"[{event.author}] {text[:100]}..."
                        state.update_progress(
                            f"ADK refine: {event.author} active",
                            ProgressStatus.IN_PROGRESS,
                            log_msg,
                        )

                # Sync coder outputs only (requirements should not be overwritten here)
                all_files = []
                for key in ["frontend_files", "backend_files"]:
                    if key in adk_session.state:
                        val = adk_session.state[key]
                        if isinstance(val, dict):
                            file_list = FileList(**val)
                            all_files.extend(file_list.files)
                        elif hasattr(val, "files"):
                            all_files.extend(val.files)

                if all_files:
                    current_files_map = {f.path.replace('\\', '/').strip('/'): f for f in state.files}
                    for new_file in all_files:
                        norm_path = new_file.path.replace('\\', '/').strip('/')
                        new_file.path = norm_path
                        current_files_map[norm_path] = new_file
                    state.files = list(current_files_map.values())

            state.adk_state = dict(adk_session.state)
            state.adk_events = list(adk_session.events)
            state.update_progress("Refinement complete", ProgressStatus.COMPLETED)
            return state

        except Exception as e:
            state.update_progress("Refinement failed", ProgressStatus.ERROR, str(e))
            raise
    
    async def self_heal(self, session_id: str, validation_errors: list[str], max_retries: int = 2) -> ProjectState:
        """Self-healing: retry code generation with validation error feedback (max 2 retries)."""
        state = session_manager.get_session(session_id)
        if not state:
            raise ValueError(f"Session {session_id} not found")
        
        errors_summary = "\n".join(validation_errors[:20])  # Limit error text
        
        for attempt in range(max_retries):
            state.update_progress(
                f"Self-healing attempt {attempt + 1}/{max_retries}",
                ProgressStatus.IN_PROGRESS,
                f"Fixing validation errors: {errors_summary[:200]}..."
            )
            
            # Build a prompt that includes the errors and asks for fixes
            adk_session = create_adk_session(state)
            
            heal_prompt = (
                "CRITICAL: The previous code generation had validation errors. "
                "You MUST fix these errors in your output.\n\n"
                f"Validation Errors:\n{errors_summary}\n\n"
                "Please regenerate the affected files with these errors fixed. "
                "Ensure all syntax is correct, tags are closed, and code is valid.\n"
            )
            
            # If we have requirements, include them; otherwise use existing files as context
            if state.requirements:
                existing_reqs = state.requirements.model_dump()
                heal_prompt += f"\nExisting requirements (keep these): {existing_reqs}\n"
            
            try:
                async for event in self.refine_runner.run(heal_prompt, adk_session):
                    if event.author != "user" and event.content:
                        text = ""
                        if hasattr(event.content, 'parts') and event.content.parts:
                            text = "".join(
                                p.text for p in event.content.parts
                                if hasattr(p, 'text') and p.text
                            )
                        if text:
                            state.update_progress(
                                f"Self-heal [{attempt + 1}]: {event.author} fixing errors",
                                ProgressStatus.IN_PROGRESS,
                                text[:100]
                            )
                
                # Sync updated files
                all_files = []
                for key in ["frontend_files", "backend_files"]:
                    if key in adk_session.state:
                        val = adk_session.state[key]
                        if isinstance(val, dict):
                            file_list = FileList(**val)
                            all_files.extend(file_list.files)
                        elif hasattr(val, "files"):
                            all_files.extend(val.files)
                
                if all_files:
                    current_files_map = {f.path.replace('\\', '/').strip('/'): f for f in state.files}
                    for new_file in all_files:
                        norm_path = new_file.path.replace('\\', '/').strip('/')
                        new_file.path = norm_path
                        current_files_map[norm_path] = new_file
                    state.files = list(current_files_map.values())
                
                state.adk_state = dict(adk_session.state)
                state.adk_events = list(adk_session.events)
                
                # Return updated state for re-validation
                return state
                
            except Exception as e:
                state.update_progress(
                    f"Self-heal attempt {attempt + 1} failed",
                    ProgressStatus.ERROR,
                    str(e)
                )
                if attempt == max_retries - 1:
                    # Last attempt failed, give up
                    raise
        
        return state
