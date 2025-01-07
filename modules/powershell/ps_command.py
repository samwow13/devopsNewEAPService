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
            str: Command execution output
        """
        try:
            # Store the command
            self.last_command = command
            
            # Execute PowerShell command
            process = subprocess.Popen(
                ['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', command],
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
                
            # Store the output
            self.last_output = output
            return output.strip()
            
        except Exception as e:
            error_msg = f"Error executing PowerShell command: {str(e)}"
            self.last_output = error_msg
            raise Exception(error_msg)
