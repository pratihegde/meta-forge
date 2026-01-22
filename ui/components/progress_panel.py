"""Left panel with Progress and Chat"""
from nicegui import ui
from context.models import ProgressStep, ProgressStatus
import datetime

class ProgressPanel:
    """Left panel showing orchestration progress and Chat interactions"""
    
    def __init__(self):
        self.steps_container = None
        self.chat_container = None
        self.step_map = {} # Map step name to UI element for updates
        
    def create(self):
        """Create the left panel UI with 50/50 Chat and Progress split"""
        with ui.column().classes('h-full w-full bg-slate-900 border-r border-slate-800 flex flex-col gap-0'):
            
            # Top: Chat Section (50%)
            with ui.column().classes('w-full h-1/2 p-4 flex flex-col overflow-hidden border-b border-slate-800'):
                ui.label('💬 Chat & Refine').classes('text-sm font-bold mb-2 text-slate-400 uppercase tracking-wider')
                
                # Messages Area
                with ui.scroll_area().classes('w-full flex-grow bg-slate-950 rounded-lg p-2 mb-2 border border-slate-800 shadow-inner') as self.scroll_area:
                    self.chat_container = ui.column().classes('w-full gap-2')
                    # Initial messages
                    with self.chat_container:
                         self.add_message("Hi! I'm MetaForge. Describe your app or ask for changes.", sent=False)

                # Input Area
                with ui.row().classes('w-full gap-2 items-center'):
                    self.chat_input = ui.input(placeholder='Type changes...').props('rounded outlined dense dark').classes('flex-grow text-xs')
                    self.chat_input.on('keydown.enter', self.send_message)
                    ui.button(icon='send', on_click=self.send_message).props('round dense flat').classes('text-blue-500 hover:scale-110 transition-transform')
            
            # Bottom: Progress/Logs Section (50%)
            with ui.column().classes('w-full h-1/2 p-4 flex flex-col overflow-hidden bg-slate-950/50'):
                ui.label('📋 Activity Logs').classes('text-sm font-bold mb-2 text-slate-400 uppercase tracking-wider')
                with ui.scroll_area().classes('w-full flex-grow font-mono text-[10px] leading-tight') as self.log_scroll:
                    self.steps_container = ui.column().classes('w-full gap-1')
            
            return self

    def update_steps(self, steps: list[ProgressStep]):
        """Update the progress steps as a rolling log"""
        if not self.steps_container or not self.steps_container.client.connected:
            return
            
        try:
            self.steps_container.clear()
            with self.steps_container:
                for step in steps:
                    color = "text-blue-400" if step.status == ProgressStatus.IN_PROGRESS else \
                            "text-green-400" if step.status == ProgressStatus.COMPLETED else \
                            "text-red-400" if step.status == ProgressStatus.ERROR else "text-slate-500"
                    
                    icon = "⚙️" if step.status == ProgressStatus.IN_PROGRESS else \
                           "✅" if step.status == ProgressStatus.COMPLETED else \
                           "❌" if step.status == ProgressStatus.ERROR else "⏳"
                    
                    with ui.row().classes('w-full gap-2 items-start opacity-90'):
                        ui.label(f"[{step.timestamp.strftime('%H:%M:%S')}]").classes('text-[8px] text-slate-600 flex-none font-mono')
                        ui.label(icon).classes('flex-none text-[10px]')
                        with ui.column().classes('flex-grow gap-0'):
                            ui.label(step.name).classes(f'font-bold {color} break-all')
                            if step.details:
                                ui.label(step.details).classes('text-slate-400 italic break-all opacity-80')
            
            # Auto-scroll log to bottom
            if self.log_scroll:
                self.log_scroll.scroll_to(percent=1.0)
        except:
            pass

    def add_message(self, text: str, sent: bool = False):
        """Add a message to the chat container with refined alignment"""
        if not self.chat_container or not self.chat_container.client.connected:
            return
            
        try:
            with self.chat_container:
                avatar = None if sent else 'https://api.dicebear.com/7.x/bottts/svg?seed=MetaForge'
                with ui.row().classes(f'w-full {"justify-end" if sent else "justify-start"}'):
                    ui.chat_message(
                        text, 
                        sent=sent, 
                        avatar=avatar, 
                        stamp=datetime.datetime.now().strftime("%H:%M")
                    ).classes('max-w-[85%]')
            
            # Auto-scroll to bottom
            if self.scroll_area:
                self.scroll_area.scroll_to(percent=1.0)
        except:
            pass

    def send_message(self):
        """Handle sending chat message"""
        text = self.chat_input.value
        if not text: return
        
        self.chat_input.value = ''
        self.add_message(text, sent=True)
            
        # Trigger parent callback
        if hasattr(self, 'on_chat_message') and self.on_chat_message:
            # We can't await here directly if it's not async context, 
            # but NiceGUI button handlers support async.
            # Make sure to handle it correctly.
            # We'll pass it to a background task or just call it if main handles it.
            # Main.py handle_chat_message is async.
            import asyncio
            # If on_chat_message is async, proper way in NiceGUI is just call it?
            # on_click supports async. but send_message is bound to on_click.
            # If send_message is async, we can await.
            # Let's check signature. I defined send_message as sync.
            # I should make it async or use background task.
            pass
            
        # Hack: In Main.py I bound it. But wait, I need to actually call it.
        # I will store the callback.
        
        if hasattr(self, 'on_chat_message'):
             # Create task if async
             import asyncio
             if asyncio.iscoroutinefunction(self.on_chat_message):
                 # NiceGUI background task
                 from nicegui import background_tasks
                 background_tasks.create(self.on_chat_message(text))
             else:
                 self.on_chat_message(text)
