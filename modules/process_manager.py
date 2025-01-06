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

    def check_local_processes(self):
        """
        Check the status of monitored processes in the local environment.
        Returns a dictionary with process names and their running status.
        """
        powershell_command = """
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
            # Execute PowerShell command and capture output
            result = subprocess.run(
                ['powershell', '-Command', powershell_command],
                capture_output=True,
                text=True
            )
            
            # Parse the JSON output
            self.process_statuses = json.loads(result.stdout)
            return self.process_statuses
            
        except Exception as e:
            print(f"Error checking processes: {str(e)}")
            return {proc: "Error" for proc in self.monitored_processes}

    def get_process_statuses(self):
        """
        Get the current process statuses.
        Returns a dictionary of process names and their status.
        """
        return self.process_statuses
