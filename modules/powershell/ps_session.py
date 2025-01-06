"""
PowerShell Remote Session Module
Handles the creation and management of PowerShell remote sessions
"""
from flask import session
import subprocess

class PSRemoteSession:
    def __init__(self):
        """Initialize the PowerShell Remote Session manager"""
        self.active_sessions = {}
        
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
            password = session.get('password')  # This should be properly encrypted in production

            # Create PowerShell command
            ps_command = f"""
            $cred = New-Object System.Management.Automation.PSCredential (
                "{username}", 
                (ConvertTo-SecureString "{password}" -AsPlainText -Force)
            )
            $result = Test-WSMan -ComputerName {computer_name} -Credential $cred -ErrorAction SilentlyContinue
            if ($?) {{ 
                Write-Output "Connection Status: Success"
                Write-Output "Details:"
                $result | Format-List
            }} else {{ 
                Write-Output "Connection Status: Failed"
                Write-Output "Error: Unable to establish connection"
            }}
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
