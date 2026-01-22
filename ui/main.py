"""Main NiceGUI application for MetaForge"""
from nicegui import ui, app
import asyncio
from pathlib import Path

import config
from context import ProblemStatement, ProgressStatus
from context.session_manager import session_manager
from agents import MetaForgeOrchestrator
from ui.components import create_landing_page, ProgressPanel, LivePreview, FileTree
from utils import write_files_to_disk
from preview import PreviewServer
from utils import validate_code
from context.models import ValidationResult


class MetaForgeApp:
    """Main MetaForge application"""
    
    def __init__(self):
        # Initialize with OpenAI Key
        self.orchestrator = MetaForgeOrchestrator()
        # self.preview_server = PreviewServer(port=config.PREVIEW_PORT)
        
        # UI Components
        self.progress_panel = None
        self.live_preview = None
        self.file_tree = None
        self.spinner = None
        self.spinner_container = None
        
        # State
        self.current_session_id = None
        self.is_generating = False
    
    def create_ui(self):
        """Create the main UI"""
        
        # Landing page
        @ui.page('/')
        def index():
            # Dark theme background
            ui.query('body').classes('bg-slate-950')
            create_landing_page(on_generate=self.start_generation)
        
        # Workspace page (shown during generation)
        @ui.page('/workspace')
        def workspace():
            # Dark theme background
            ui.query('body').classes('bg-slate-950')
            self.create_workspace()
    
    def create_workspace(self):
        """Create the three-panel workspace"""
        ui.colors(primary='#3b82f6', secondary='#8b5cf6', accent='#06b6d4', dark='#0f172a')
        
        # Transparent/Dark Header
        with ui.header().classes('bg-slate-900/80 backdrop-blur-md border-b border-slate-800 h-16'):
            with ui.row().classes('w-full h-full items-center justify-between px-6'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('bolt', size='20px').classes('text-blue-500')
                    ui.label('MetaForge').classes('text-xl font-bold text-white tracking-tight')
                
                with ui.row().classes('items-center gap-4'):
                    with ui.row().classes('items-center gap-2') as self.spinner_container:
                        ui.label('Building...').classes('text-xs text-blue-400 font-mono animate-pulse')
                        self.spinner = ui.spinner(size='sm', color='blue')
                    self.spinner_container.set_visibility(False)
                    
                    ui.button('New Project', icon='add', on_click=lambda: ui.navigate.to('/')).props('flat dense').classes('text-slate-400 hover:text-white')
        
        # Three-panel layout
        with ui.row().classes('w-full h-[calc(100vh-64px)] gap-0 overflow-hidden'):
            # Left: Chat & Progress (25%)
            with ui.column().classes('w-1/4 h-full bg-slate-900 border-r border-slate-800 p-0 overflow-hidden shadow-xl z-10'):
                self.progress_panel = ProgressPanel()
                self.progress_panel.create()
                self.progress_panel.on_chat_message = self.handle_chat_message
                
                # Add initial user message if we just started
                if hasattr(self, 'initial_problem') and self.initial_problem:
                     self.progress_panel.add_message(self.initial_problem, sent=True)
                     self.initial_problem = None # Clear after adding
            
            # Center: Full Live Preview (55%)
            with ui.column().classes('w-[55%] h-full bg-slate-950 p-6 relative overflow-hidden'):
                self.live_preview = LivePreview(preview_port=config.PREVIEW_PORT).create()
            
            # Right: Files & Code (20%)
            with ui.column().classes('w-1/5 h-full bg-slate-900 border-l border-slate-800 p-0 overflow-hidden'):
                self.file_tree = FileTree().create()
                # Hook up selection to code preview (inside file_tree)
                self.file_tree.on_select = lambda f: self.file_tree.update_code(f.content, f.language, f.path)
        
        # Start auto-refresh for progress updates
        if hasattr(self, 'workspace_timer') and self.workspace_timer:
            self.workspace_timer.cancel()
        self.workspace_timer = ui.timer(1.0, self.update_workspace)
        
    async def handle_chat_message(self, message: str):
        """Handle iterative updates from chat"""
        if not self.current_session_id:
             ui.notify("No active session!", type='warning')
             return
             
        # Start background refinement
        asyncio.create_task(self.run_refinement(message))
        
    async def run_refinement(self, instruction: str):
         """Run refinement task"""
         if self.is_generating: return
         self.is_generating = True
         if self.spinner_container: self.spinner_container.set_visibility(True)
         try:
             session = session_manager.get_session(self.current_session_id)
             session.update_progress("Refinement requested", ProgressStatus.IN_PROGRESS, instruction[:200])
             await self.orchestrator.refine(instruction, self.current_session_id)
             
             # Write updates
             project_dir = config.OUTPUT_DIR / self.current_session_id
             write_files_to_disk(session.files, project_dir)
             print(f"[DEBUG] Wrote {len(session.files)} files to {project_dir}")
             import sys
             sys.stdout.flush()
             
             # Identify the correct directory to serve
             frontend_dir = self._get_frontend_dir(project_dir)
             
             # Mount the generated project directory to a unique path
             route_path = f'/preview/{self.current_session_id}'
             app.add_static_files(route_path, str(frontend_dir))
             
             print(f"[DEBUG] Restarting preview for refinement at {route_path}, serving: {frontend_dir}")
             
             # Reload preview
             if self.live_preview:
                 preview_url = route_path + '/index.html'
                 await self.live_preview.load_preview_url(preview_url)
                 
                 # Show first file in code view
                 if session.files:
                     f = session.files[0]
                     self.file_tree.update_code(f.content, f.language, f.path)

             # Validate updated code (basic syntax checks)
             errors: list[str] = []
             for f in session.files:
                  ok, msgs = validate_code(f.content, f.language)
                  if not ok:
                       errors.extend([f"{f.path}: {m}" for m in msgs])
             session.validation = ValidationResult(passed=len(errors) == 0, errors=errors)
             
             # Self-healing: if validation fails, retry with error feedback (max 2 retries)
             if errors and len(errors) > 0:
                 session.update_progress(
                     "Validation & Testing",
                     ProgressStatus.IN_PROGRESS,
                     f"Found {len(errors)} errors, attempting self-healing..."
                 )
                 try:
                     healed_state = await self.orchestrator.self_heal(self.current_session_id, errors, max_retries=2)
                     # Re-validate after healing
                     errors_after_heal: list[str] = []
                     for f in healed_state.files:
                          ok, msgs = validate_code(f.content, f.language)
                          if not ok:
                               errors_after_heal.extend([f"{f.path}: {m}" for m in msgs])
                     session.validation = ValidationResult(passed=len(errors_after_heal) == 0, errors=errors_after_heal)
                     session.files = healed_state.files  # Update with healed files
                     errors = errors_after_heal  # Update for status message
                 except Exception as heal_error:
                     session.update_progress(
                         "Self-healing failed",
                         ProgressStatus.ERROR,
                         f"Could not auto-fix errors: {str(heal_error)}"
                     )
             
             session.update_progress(
                  "Validation & Testing",
                  ProgressStatus.COMPLETED if session.validation.passed else ProgressStatus.ERROR,
                  "All checks passed" if session.validation.passed else f"{len(errors)} errors remain",
             )
             
             # Notify user
             try:
                  if self.progress_panel and self.progress_panel.chat_container.client.connected:
                      self.progress_panel.add_message("Refinement complete! Check updated files.", sent=False)
             except:
                  pass
             
             # Refresh preview
             try:
                  if self.live_preview:
                      self.live_preview.refresh()
             except:
                  pass
                   
         except Exception as e:
             import traceback
             traceback.print_exc()
             try:
                  if self.progress_panel and self.progress_panel.chat_container.client.connected:
                      self.progress_panel.add_message(f"Refinement failed: {str(e)}", sent=False)
             except:
                  pass
         finally:
             self.is_generating = False
             try:
                  if self.spinner_container and self.spinner_container.client.connected:
                      self.spinner_container.set_visibility(False)
             except:
                  pass
             
    
    def start_generation(self, problem_statement: str):
        """Start the app generation process"""
        if not problem_statement or not problem_statement.strip():
            ui.notify('Please enter a problem statement', type='warning')
            return
        
        if not config.OPENAI_API_KEY:
            ui.notify('Please set OPENAI_API_KEY environment variable', type='negative')
            return
        
        # Store for chat display in workspace
        self.initial_problem = problem_statement
        
        # Create session
        problem = ProblemStatement(description=problem_statement)
        self.current_session_id = session_manager.create_session(problem)
        
        # Navigate to workspace
        ui.navigate.to('/workspace')
        
        # Start generation in background
        asyncio.create_task(self.run_generation())
    
    async def run_generation(self):
        """Run the generation process"""
        if self.is_generating:
            return
        
        self.is_generating = True
        

        
        # Give the workspace page a moment to load so the spinner is available
        await asyncio.sleep(0.5)
        if self.spinner_container: 
             self.spinner_container.set_visibility(True)
             
        print(f"[INFO] Starting generation for session {self.current_session_id}...")
        import sys
        sys.stdout.flush()
        
        try:
            # Run orchestrator
            session = session_manager.get_session(self.current_session_id)
            problem_statement = session.problem_statement.description
            
            result = await self.orchestrator.orchestrate(problem_statement, self.current_session_id)
            
            # Write files to disk
            project_dir = config.OUTPUT_DIR / self.current_session_id
            write_files_to_disk(result.files, project_dir)

            # Validate generated code (basic syntax checks)
            errors: list[str] = []
            for f in result.files:
                 ok, msgs = validate_code(f.content, f.language)
                 if not ok:
                      errors.extend([f"{f.path}: {m}" for m in msgs])
            session.validation = ValidationResult(passed=len(errors) == 0, errors=errors)
            
            # Self-healing: if validation fails, retry with error feedback (max 2 retries)
            if errors and len(errors) > 0:
                session.update_progress(
                    "Validation & Testing",
                    ProgressStatus.IN_PROGRESS,
                    f"Found {len(errors)} errors, attempting self-healing..."
                )
                try:
                    healed_state = await self.orchestrator.self_heal(self.current_session_id, errors, max_retries=2)
                    # Re-write healed files to disk
                    write_files_to_disk(healed_state.files, project_dir)
                    print(f"[DEBUG] Re-wrote {len(healed_state.files)} healed files to {project_dir}")
                    
                    # Re-validate after healing
                    errors_after_heal: list[str] = []
                    for f in healed_state.files:
                         ok, msgs = validate_code(f.content, f.language)
                         if not ok:
                              errors_after_heal.extend([f"{f.path}: {m}" for m in msgs])
                    session.validation = ValidationResult(passed=len(errors_after_heal) == 0, errors=errors_after_heal)
                    session.files = healed_state.files  # Update with healed files
                    result = healed_state
                    errors = errors_after_heal  # Update for status message
                except Exception as heal_error:
                    session.update_progress(
                        "Self-healing failed",
                        ProgressStatus.ERROR,
                        f"Could not auto-fix errors: {str(heal_error)}"
                    )
                    print(f"[ERROR] Self-healing failed: {heal_error}")
            
            session.update_progress(
                 "Validation & Testing",
                 ProgressStatus.COMPLETED if session.validation.passed else ProgressStatus.ERROR,
                 "All checks passed" if session.validation.passed else f"{len(errors)} errors remain",
            )
            
            # Serve files via NiceGUI instead of separate server
            frontend_dir = self._get_frontend_dir(project_dir)
            
            # Mount the generated project directory to a unique path
            # We use app.add_static_files to serve the folder at /preview/{session_id}
            route_path = f'/preview/{self.current_session_id}'
            app.add_static_files(route_path, str(frontend_dir))
            
            print(f"[DEBUG] Mounted preview at {route_path}, serving: {frontend_dir}")
            
            # Auto-load preview
            if self.live_preview:
                 # Calculate the relative URL for the iframe
                 preview_url = route_path + '/index.html'
                 print(f"[DEBUG] Loading preview from {preview_url}")
                 await self.live_preview.load_preview_url(preview_url)
                 
                 # Show first file in code view (now in file_tree)
                 if result.files:
                      f = result.files[0]
                      self.file_tree.update_code(f.content, f.language, f.path)
            else:
                 print("[WARNING] live_preview is None, cannot load preview")
            
            # Success - update status in session (will be picked up by UI)
            session.update_progress("Done", ProgressStatus.COMPLETED)
            if self.progress_panel:
                 self.progress_panel.add_message("Build successful! You can now preview and edit your app.", sent=False)
        
        finally:
            self.is_generating = False
            if self.spinner_container: self.spinner_container.set_visibility(False)
            print("[INFO] Generation process concluded.")
            import sys
            sys.stdout.flush()
    
    def update_workspace(self):
        """Update workspace with latest session data"""
        if not self.current_session_id:
            return
        
        session = session_manager.get_session(self.current_session_id)
        if not session:
            return
        
        # Sync spinner visibility with generation state
        try:
            if self.spinner_container and self.spinner_container.client.connected:
                self.spinner_container.set_visibility(self.is_generating)
        except:
            pass
        
        # Update progress panel
        if self.progress_panel and session.progress_steps:
            try:
                self.progress_panel.update_steps(session.progress_steps)
            except:
                pass
        
        # Update file tree and status
        if self.file_tree and session.files:
            # Refresh if we just stopped generating or if file count changed
            last_gen_state = getattr(self, '_last_gen_state', False)
            current_count = getattr(self.file_tree, '_last_file_count', 0)
            
            if (last_gen_state and not self.is_generating) or len(session.files) != current_count:
                self.file_tree.update_files(session.files)
                self.file_tree._last_file_count = len(session.files)
            
            self._last_gen_state = self.is_generating
            
        # Check if we need to load preview (poll check)
        # In a real app we might use websockets or events, but polling is safe
        if self.live_preview and session.files and not self.live_preview.loaded:
             # Basic check if files exist to load
             pass

    def _get_frontend_dir(self, project_dir: Path) -> Path:
        """Helper to find the best directory to serve static files from"""
        # 1. Check root
        if (project_dir / "index.html").exists():
            return project_dir
            
        # 2. Check common subdirectories
        for sub in ["frontend", "public", "dist", "web"]:
            if (project_dir / sub / "index.html").exists():
                return project_dir / sub
                
        # 3. Fallback to frontend folder if it exists, otherwise root
        return project_dir / "frontend" if (project_dir / "frontend").exists() else project_dir


def main():
    """Main entry point"""
    app_instance = MetaForgeApp()
    app_instance.create_ui()
    
    ui.run(
        title='MetaForge - AI App Builder',
        port=config.NICEGUI_PORT,
        reload=False,
        show=True,
        dark=True # Force dark mode
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()
