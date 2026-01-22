"""File tree component showing generated files"""
from nicegui import ui
from context.models import GeneratedFile
from utils.file_manager import get_file_icon
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter


class FileTree:
    """Right panel showing file structure"""
    
    def __init__(self):
        self.tree_container = None
        self.code_container = None
        self.code_scroll = None
        self.filename_label = None
        self.current_files = []
    
    def create(self):
        """Create the right panel UI with Flat File List and Code Preview"""
        with ui.column().classes('h-full w-full bg-slate-900 flex flex-col gap-0'):
            
            # Top: Flat File List (25%)
            with ui.column().classes('w-full h-[25%] p-4 border-b border-slate-800'):
                with ui.row().classes('w-full items-center justify-between mb-2'):
                    ui.label('📁 Project Files').classes('text-sm font-bold text-slate-400 uppercase tracking-wider')
                    ui.button(icon='download', on_click=self._download_zip).props('flat dense').classes('text-blue-400 hover:text-white')
                
                with ui.scroll_area().classes('w-full flex-grow'):
                     self.tree_container = ui.column().classes('w-full gap-1')
            
            # Bottom: Code Preview (75%)
            with ui.column().classes('w-full h-[75%] p-4 flex flex-col overflow-hidden bg-slate-950'):
                 with ui.row().classes('w-full items-center justify-between mb-2'):
                      ui.label('📄 Source Code').classes('text-sm font-bold text-slate-400 uppercase tracking-wider')
                      self.filename_label = ui.label('').classes('text-[10px] font-mono text-slate-500')
                 
                 with ui.scroll_area().classes('w-full flex-grow border border-slate-800 rounded bg-slate-900/50 p-2 shadow-inner') as self.code_scroll:
                      self.code_container = ui.html('<div class="text-slate-600 italic text-xs p-4">Select a file to view source...</div>', sanitize=False)
            
            return self

    def update_files(self, files: list[GeneratedFile]):
        """Update the file list with a flat structure"""
        if not files:
            return
            
        self.current_files = files
        
        self.tree_container.clear()
        with self.tree_container:
             # Sort files: app.py and index.html first, then alphabetic
             sorted_files = sorted(files, key=lambda f: (
                  f.path != 'index.html' and f.path != '/index.html',
                  f.path != 'app.py' and f.path != '/app.py',
                  f.path.lower()
             ))

             for f in sorted_files:
                  # Normalize path for display
                  path = f.path.replace('\\', '/').strip('/')
                  icon = get_file_icon(path)
                  
                  with ui.row().classes('w-full items-center px-2 py-1 hover:bg-slate-800 rounded cursor-pointer group transition-colors') \
                       .on('click', lambda _, file=f: self._handle_file_click(file)):
                       ui.icon(icon, size='xs').classes('text-slate-500 group-hover:text-blue-400')
                       ui.label(path).classes('text-xs text-slate-300 group-hover:text-white truncate')

        print(f"DEBUG: Updated flat file list with {len(files)} files.")

    def _handle_file_click(self, file_obj):
        """Handle click on a file in the flat list"""
        self.update_code(file_obj.content, file_obj.language, file_obj.path)
        if hasattr(self, 'on_select') and self.on_select:
             self.on_select(file_obj)

    def update_code(self, content: str, language: str, filename: str = ""):
        """Update the code preview window with syntax highlighting"""
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name, TextLexer
        from pygments.formatters import HtmlFormatter
        
        self.filename_label.text = filename
        
        try:
            lexer = get_lexer_by_name(language)
        except:
            lexer = TextLexer()
            
        formatter = HtmlFormatter(style='monokai', linenos=True, cssclass='source')
        highlighted = highlight(content, lexer, formatter)
        
        html = f'''
        <style>
            .source {{ font-size: 11px !important; line-height: 1.4 !important; font-family: "JetBrains Mono", monospace !important; }}
            {formatter.get_style_defs(".source")}
        </style>
        {highlighted}
        '''
        self.code_container.content = html
        if self.code_scroll:
            self.code_scroll.scroll_to(percent=0)

    def _download_zip(self):
        ui.notify('Download feature coming soon!', type='info')
