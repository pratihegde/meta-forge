"""Simple HTTP server for live preview"""
import http.server
import socketserver
import threading
from pathlib import Path
import os


class PreviewServer:
    """Serves generated frontend files for live preview"""
    
    def __init__(self, port: int = 8081):
        self.port = port
        self.server = None
        self.thread = None
        self.directory = None
    
    def start(self, directory: Path):
        """Start the preview server without global chdir"""
        # If already running, restart so we serve the new directory
        if self.server:
            self.stop()

        self.directory = directory
        
        # Create a handler factory that uses the specific directory
        import functools
        handler_class = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
        
        # Allow port reuse
        class ReusableTCPServer(socketserver.TCPServer):
            allow_reuse_address = True
        
        try:
            self.server = ReusableTCPServer(("", self.port), handler_class)
            # Run in thread
            self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.thread.start()
            import sys
            print(f"[INFO] Preview server started on http://localhost:{self.port} serving {directory}")
            sys.stdout.flush()
        except Exception as e:
            import sys
            print(f"[ERROR] Failed to start preview server: {e}")
            sys.stdout.flush()
            raise
    
    def stop(self):
        """Stop the preview server"""
        if self.server:
            try:
                self.server.shutdown()
                self.server.server_close()
            except:
                pass
            self.server = None
            self.thread = None