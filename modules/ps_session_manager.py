"""
Module for managing PowerShell remote sessions.
This module handles creation, storage, and management of PowerShell remote sessions.
"""
import subprocess
from typing import Optional, Dict
from datetime import datetime

class PSSessionManager:
    def __init__(self):
        self._active_sessions: Dict[str, dict] = {}
        self._last_error = None
    
    def create_session(self, server_name: str, username: str, password: str) -> bool:
        """
        Creates a new PowerShell session for the specified server.
        
        Args:
            server_name (str): Name of the server to connect to
            username (str): Username for authentication
            password (str): Password for authentication
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create PowerShell script for session creation
            ps_script = f'''
            $password = ConvertTo-SecureString "{password}" -AsPlainText -Force
            $cred = New-Object System.Management.Automation.PSCredential ("{username}", $password)
            $session = New-PSSession -ComputerName {server_name} -Credential $cred
            if ($session) {{
                Write-Output "SUCCESS"
                Write-Output $session.Id
            }} else {{
                Write-Output "FAILED"
            }}
            '''
            
            # Execute PowerShell script
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                text=True
            )
            
            # Process the output
            output_lines = result.stdout.strip().split('\n')
            if len(output_lines) >= 2 and output_lines[0].strip() == "SUCCESS":
                session_id = output_lines[1].strip()
                self._active_sessions[server_name] = {
                    'session_id': session_id,
                    'created_at': datetime.now(),
                    'server': server_name
                }
                self._last_error = None
                return True
            
            self._last_error = result.stderr if result.stderr else "Failed to create session"
            return False
            
        except Exception as e:
            self._last_error = str(e)
            return False
    
    def get_session(self, server_name: str) -> Optional[dict]:
        """
        Returns the active session for the specified server if it exists.
        
        Args:
            server_name (str): Name of the server
            
        Returns:
            Optional[dict]: Session information if exists, None otherwise
        """
        return self._active_sessions.get(server_name)
    
    def remove_session(self, server_name: str) -> bool:
        """
        Removes and closes the session for the specified server.
        
        Args:
            server_name (str): Name of the server
            
        Returns:
            bool: True if session was successfully removed, False otherwise
        """
        if server_name not in self._active_sessions:
            return False
            
        try:
            session_id = self._active_sessions[server_name]['session_id']
            ps_script = f"Remove-PSSession -Id {session_id}"
            
            subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                text=True
            )
            
            del self._active_sessions[server_name]
            return True
            
        except Exception as e:
            self._last_error = str(e)
            return False
    
    def get_last_error(self) -> Optional[str]:
        """Returns the last error message if any."""
        return self._last_error
    
    def has_active_session(self, server_name: str) -> bool:
        """
        Checks if there's an active session for the specified server.
        
        Args:
            server_name (str): Name of the server
            
        Returns:
            bool: True if active session exists, False otherwise
        """
        return server_name in self._active_sessions
