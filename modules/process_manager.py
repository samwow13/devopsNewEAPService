"""
Module for managing and monitoring process statuses across different environments.
"""
import subprocess
import json

class ProcessManager:
    def __init__(self):
        """Initialize ProcessManager with default monitored processes."""
        self.monitored_processes = ['notepad', 'SnippingTool', 'calc', 'mspaint']
        self.process_statuses = {}

    def check_processes(self, environment, connection_command=''):
        """
        Check the status of monitored processes in any environment.
        
        Args:
            environment (str): The environment name (Local, Prod 1, etc.)
            connection_command (str): The PowerShell command to connect to the environment
            
        Returns:
            dict: Dictionary with process names and their running status
        """
        # Base PowerShell script for checking processes
        process_check_script = """
        $processes = @('notepad', 'SnippingTool', 'calc', 'mspaint')
        $results = @{}
        foreach ($proc in $processes) {
            if (Get-Process -Name $proc -ErrorAction SilentlyContinue) {
                $results[$proc] = "Running"
            } else {
                $results[$proc] = "Not Running"
            }
        }
        ConvertTo-Json $results
        """
        
        try:
            # For remote environments, wrap the script in the connection command
            if connection_command:
                process_check_script = f"{connection_command}\n{process_check_script}"
            
            # Execute PowerShell command and capture output
            result = subprocess.run(
                ['powershell', '-Command', process_check_script],
                capture_output=True,
                text=True
            )
            
            # Parse the JSON output
            self.process_statuses = json.loads(result.stdout)
            return self.process_statuses
            
        except Exception as e:
            print(f"Error checking processes in {environment}: {str(e)}")
            return {proc: "Error" for proc in self.monitored_processes}

    def get_process_statuses(self):
        """
        Get the current process statuses.
        Returns a dictionary of process names and their status.
        """
        return self.process_statuses
