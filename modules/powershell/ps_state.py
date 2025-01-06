"""
PowerShell State Manager Module
Manages the state of PowerShell execution mode (local vs remote)
"""

class PSStateManager:
    def __init__(self):
        """Initialize the PowerShell State Manager"""
        self._remote_session = None
        self._is_remote_mode = False
        
    @property
    def is_remote_mode(self):
        """Check if currently in remote mode"""
        return self._is_remote_mode and self._remote_session is not None
    
    def set_remote_session(self, session):
        """Set the remote session and switch to remote mode"""
        self._remote_session = session
        self._is_remote_mode = True if session else False
        
    def clear_remote_session(self):
        """Clear the remote session and switch to local mode"""
        self._remote_session = None
        self._is_remote_mode = False
        
    def get_session(self):
        """Get the current remote session if it exists"""
        return self._remote_session
        
    def get_execution_mode(self):
        """Get the current execution mode as a string"""
        return "Remote" if self.is_remote_mode else "Local"
