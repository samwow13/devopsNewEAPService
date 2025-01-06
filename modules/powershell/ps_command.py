"""
PowerShell Command Executor Module
Handles direct execution of PowerShell commands and returns their output
"""
import subprocess

class PSCommandExecutor:
    def __init__(self):
        """Initialize the PowerShell Command Executor"""
        self.last_command = None
        self.last_output = None
        
    def execute_command(self, command):
        """
        Execute a PowerShell command and return its output
        
        Args:
            command (str): The PowerShell command to execute
            
        Returns:
            dict: Command execution results including command and raw output
        """
        try:
            # Store the command
            self.last_command = command
            
            # Create a temporary script with the command
            script_content = command
            
            # Execute PowerShell command with proper script block handling
            process = subprocess.Popen(
                ['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', script_content],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Get output and errors
            stdout, stderr = process.communicate()
            
            # Combine output and errors for complete feedback
            output = stdout
            if stderr:
                output = f"{output}\nErrors:\n{stderr}"
            
            self.last_output = output
            
            return {
                'command': command,
                'output': output,
                'status': 'success' if process.returncode == 0 else 'error'
            }
            
        except Exception as e:
            return {
                'command': command,
                'output': f"Error executing command: {str(e)}",
                'status': 'error'
            }
