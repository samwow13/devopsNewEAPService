"""
Module for managing PowerShell remote commands.
This module handles execution of PowerShell commands on remote servers.
"""
import subprocess
from typing import Optional, Dict, Tuple
from datetime import datetime

class PSSessionManager:
    def __init__(self):
        """Initialize PSSessionManager."""
        self._last_error = None
        self._credentials = {}

    def store_credentials(self, server_name: str, username: str, password: str) -> None:
        """
        Store credentials for a server.
        
        Args:
            server_name (str): Name of the server
            username (str): Username for authentication
            password (str): Password for authentication
        """
        self._credentials[server_name] = {
            'username': username,
            'password': password
        }

    def execute_command(self, server_name: str, command: str) -> Tuple[bool, str, str]:
        """
        Executes a PowerShell command on a server using stored credentials.
        
        Args:
            server_name (str): Name of the server to execute command on
            command (str): PowerShell command to execute
            
        Returns:
            Tuple[bool, str, str]: (Success status, Command output, Error message if any)
        """
        if server_name not in self._credentials:
            return False, "", "No credentials stored for server"

        creds = self._credentials[server_name]
        try:
            # Create PowerShell script that establishes connection and executes command
            ps_script = f'''
            $password = ConvertTo-SecureString "{creds['password']}" -AsPlainText -Force
            $cred = New-Object System.Management.Automation.PSCredential ("{creds['username']}", $password)
            
            $result = Invoke-Command -ComputerName {server_name} -Credential $cred -ScriptBlock {{
                {command}
            }}
            $result
            '''
            
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return True, result.stdout.strip(), ""
            else:
                return False, "", result.stderr.strip()
                
        except Exception as e:
            self._last_error = str(e)
            return False, "", str(e)

    def check_jboss_services(self, server_name: str) -> Tuple[bool, str]:
        """
        Check JBoss services on the specified server.
        
        Args:
            server_name (str): Name of the server to check services on
            
        Returns:
            Tuple[bool, str]: (Success status, Error message if any)
        """
        try:
            command = '''
            Get-Service -Name "*jboss*" | Select-Object Name, Status | Format-Table -AutoSize | Out-String
            '''
            
            success, output, error = self.execute_command(server_name, command)
            if success:
                print(f"JBoss Services Status:\n{output}")  # Log services status
                return True, ""
            else:
                error_msg = f"Error checking services: {error}"
                self._last_error = error_msg
                print(error_msg)  # Log error to console
                return False, error_msg
                
        except Exception as e:
            error_msg = str(e)
            self._last_error = error_msg
            print(f"Exception checking services: {error_msg}")  # Log exception to console
            return False, error_msg

    def get_last_error(self) -> Optional[str]:
        """Returns the last error message if any."""
        return self._last_error
