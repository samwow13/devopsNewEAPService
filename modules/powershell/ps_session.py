"""
PowerShell Remote Session Module
Handles the creation and management of PowerShell remote sessions
"""
from flask import session, current_app
import subprocess

class PSRemoteSession:
    _instance = None
    
    def __init__(self):
        """Initialize the PowerShell Remote Session manager"""
        self.active_sessions = {}
        
    def get_credential_manager(self):
        """Get the credential manager from current app context"""
        return current_app.credential_manager
        
    def create_session(self, computer_name):
        """
        Create a new PowerShell remote session to the specified computer
        
        Args:
            computer_name (str): The name or IP of the target computer
            
        Returns:
            dict: Session information including status and connection details
        """
        # TODO: Implement actual PowerShell session creation
        session_info = {
            'computer_name': computer_name,
            'status': 'initialized',
            'session_id': None
        }
        return session_info

    def test_connection(self, computer_name):
        """
        Test PowerShell remote connection to the specified computer using current user credentials
        
        Args:
            computer_name (str): The name or IP of the target computer
            
        Returns:
            dict: Connection test results including status, message, command, and raw output
        """
        try:
            # Get credentials from Flask session
            username = session.get('username')
            encrypted_password = session.get('encrypted_password')
            
            if not username or not encrypted_password:
                return {
                    'status': 'error',
                    'message': 'No credentials found in session',
                    'command': None,
                    'raw_output': 'Authentication required'
                }

            # Create PowerShell credential script
            credential_manager = self.get_credential_manager()
            cred_script = credential_manager.get_ps_credential_script(username, encrypted_password)
            
            # Create PowerShell command
            ps_command = f"""
            {cred_script}
            Test-WSMan -ComputerName {computer_name} -Credential $cred -ErrorAction SilentlyContinue
            """

            # Execute PowerShell command
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True
            )

            success = "Connection Status: Success" in result.stdout
            return {
                'status': 'success' if success else 'error',
                'message': 'Connection successful' if success else 'Connection failed',
                'command': ps_command.strip(),
                'raw_output': result.stdout.strip() or result.stderr.strip()
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'command': ps_command.strip() if 'ps_command' in locals() else 'Command generation failed',
                'raw_output': str(e)
            }
