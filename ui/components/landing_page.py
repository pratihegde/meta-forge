from nicegui import ui
from typing import Callable

def create_landing_page(on_generate: Callable[[str], None]):
    """
    Creates the landing page component with Bolt.new inspired theme
    Dark mode, deep blue/black background, glassmorphism
    """
    # Main container with dark deep background and subtle gradient
    with ui.column().classes('w-full min-h-screen items-center justify-center bg-slate-950 text-white p-4 relative overflow-hidden'):
        
        # Background Glow Effects
        ui.element('div').classes('absolute top-0 left-1/4 w-96 h-96 bg-blue-600/20 rounded-full blur-[128px] pointer-events-none')
        ui.element('div').classes('absolute bottom-0 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-[128px] pointer-events-none')

        # Header / Navigation (Simple)
        with ui.row().classes('absolute top-0 w-full p-6 justify-between items-center z-10'):
             with ui.row().classes('items-center gap-2'):
                 ui.icon('bolt', size='24px').classes('text-blue-400')
                 ui.label('MetaForge').classes('text-xl font-bold tracking-tight')
             

        # Hero Content
        with ui.column().classes('max-w-4xl w-full items-center text-center gap-8 z-10 mt-[-80px]'):
            
            # Badge
            with ui.row().classes('bg-slate-800/50 border border-slate-700/50 rounded-full px-4 py-1.5 backdrop-blur-md mb-4'):
                ui.icon('auto_awesome', size='16px').classes('text-blue-400 mr-2')
                ui.label('Introducing MetaForge v1.0').classes('text-xs font-medium text-slate-300')

            # Headline
            with ui.column().classes('gap-2 items-center'):
                ui.html('<h1 class="text-5xl md:text-7xl font-bold tracking-tight text-center">What will you <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">build</span> today?</h1>', sanitize=False)
                ui.label('Create stunning apps & websites by chatting with AI.').classes('text-xl text-slate-400 mt-4 font-light text-center')

            # Input Area (Glassmorphism)
            with ui.column().classes('w-full max-w-2xl bg-slate-900/50 border border-slate-800 rounded-2xl p-2 mt-8 backdrop-blur-xl shadow-2xl relative group focus-within:border-blue-500/50 transition-colors'):
                
                problem_input = ui.textarea(placeholder="Let's build a personal website for a photographer...").classes(
                    'w-full bg-transparent text-lg p-4 text-white focus:outline-none placeholder-slate-600 min-h-[120px]'
                ).props('autofocus spellcheck="false" input-class="resize-none"')
                
                # Add Enter key handler (Correct NiceGUI pattern for generic event args)
                def handle_enter(e):
                    # In NiceGUI GenericEventArguments, the JS event object is in e.args
                    if e.args.get('key') == 'Enter' and not e.args.get('shiftKey'):
                        on_generate(problem_input.value)
                
                problem_input.on('keydown', handle_enter)
                
                with ui.row().classes('w-full justify-between items-center px-4 pb-2'):
                     with ui.button(icon='attach_file').props('round flat').classes('text-slate-500 hover:text-white hover:bg-slate-800'):
                         ui.tooltip('Attach file')
                     
                     with ui.row().classes('items-center gap-4'):
                         
                         ui.button('Build now', icon='send', on_click=lambda: on_generate(problem_input.value)).classes(
                             'bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white rounded-xl px-6 py-2 shadow-lg shadow-blue-900/20 transition-all transform active:scale-95'
                         )
            # Footer
            with ui.column().classes('w-full mt-12 pt-8 border-t border-slate-800 items-center opacity-40'):
                ui.label('Powered by Google ADK & GPT-4o-mini').classes('text-xs text-slate-500 font-medium tracking-wider uppercase')
