"""
Module for managing environment connections and selections.
"""

class EnvironmentManager:
    def __init__(self):
        # Dictionary to store environment connection commands (not visible to users)
        self._connection_commands = {
            'Local': '',  # Local environment doesn't need a connection command
            'Prod 1': 'Enter-PSSession -ComputerName prod1.example.com',
            'Prod 2': 'Enter-PSSession -ComputerName prod2.example.com'
        }
    
    def get_environments(self):
        """Returns a list of available environment names."""
        return list(self._connection_commands.keys())
    
    def get_connection_command(self, environment_name):
        """
        Returns the connection command for the specified environment.
        This method should only be used internally by the application.
        """
        return self._connection_commands.get(environment_name)
