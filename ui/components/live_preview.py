"""Live preview component with iframe"""
from nicegui import ui
from pathlib import Path
import time


class LivePreview:
    """Center panel showing live preview of generated app"""
    
    def __init__(self, preview_port: int = 8081):
        self.preview_port = preview_port
        self.iframe = None
        self.status_label = None
        self.loaded = False
    
    def create(self):
        """Create the live preview UI"""
        # Full height container, no padding, no border
        with ui.column().classes('h-full w-full p-0 bg-slate-950 gap-0 relative'):
            
            # Placeholder for building state
            with ui.column().classes('absolute inset-0 items-center justify-center z-0 text-slate-700 gap-4') as self.placeholder:
                ui.icon('auto_awesome', size='64px').classes('animate-pulse opacity-20')
                ui.label('Your application will appear here...').classes('text-lg font-light tracking-wide opacity-30')

            # Status overlay (hidden by default) - needs pointer events to be clickable
            with ui.row().classes('absolute top-2 right-2 z-50 gap-2').style('pointer-events: auto;') as self.controls_container:
                self.status_label = ui.label('').classes('text-xs text-green-400 bg-black/50 px-2 rounded')

            # Preview iframe - Full Height, Full Width
            # Added onload focus helper for games
            self.iframe = ui.html(
                f'<iframe id="preview-iframe" src="about:blank" class="w-full h-full border-none bg-transparent" '
                f'onload="this.contentWindow.focus()"></iframe>', 
                sanitize=False
            ).classes('w-full h-full flex-grow z-10')
            
            return self
    
    async def load_preview_url(self, url: str):
        """Load the preview from a specific URL"""
        self.loaded = True
        self.status_label.text = 'Loading...'
        self.status_label.classes('text-sm text-blue-400')
        
        # Cache bust
        final_url = f"{url}?t={int(time.time() * 1000)}"
        
        try:
            # Hide placeholder
            if hasattr(self, 'placeholder'):
                 self.placeholder.set_visibility(False)

            # Update iframe src and set background to white for the project
            self.iframe.content = f'<iframe id="preview-iframe" src="{final_url}" class="w-full h-full border-none bg-white" onload="this.contentWindow.focus()"></iframe>'
            
            # Update controls container
            self.controls_container.clear()
            with self.controls_container:
                 self.status_label = ui.label('Preview active').classes('text-sm text-green-500')
                 ui.link('Open in New Tab', final_url, new_tab=True).classes('text-[10px] text-blue-400 ml-2')
                 # ui.button(icon='refresh', on_click=lambda: self.load_preview_url(url)).props('flat dense').classes('text-xs text-slate-400 ml-auto')
                 
        except Exception as e:
            self.status_label.text = f'Preview error: {str(e)}'
            self.status_label.classes('text-sm text-red-500')
            print(f"[ERROR] Preview load failed: {e}")
            
    async def load_preview(self, project_dir: Path):
        """Deprecated: Load the preview from project directory (uses separate server)"""
        # Kept for backward compatibility if needed, but we prefer load_preview_url now
        pass

    def show_error(self, message: str):
        """Show error message in preview area"""
        self.status_label.text = f'❌ {message}'
        self.status_label.classes('text-sm text-red-500')
        self.iframe.content = f'<div class="flex items-center justify-center h-full text-red-400 p-4 text-center">{message}</div>'
    
    def refresh(self):
        """Refresh the preview"""
        if self.iframe:
            # Trigger iframe reload (cache-bust)
            url = f'http://127.0.0.1:{self.preview_port}/?t={int(time.time() * 1000)}'
            self.iframe.content = f'<iframe id="preview-iframe" src="{url}" class="w-full h-full border-none bg-white" onload="this.contentWindow.focus()"></iframe>'
    
    def _set_viewport(self, size: str):
        """Change viewport size"""
        if size == 'mobile':
            # Update iframe width for mobile view
            pass
        elif size == 'desktop':
            # Update iframe width for desktop view
            pass
