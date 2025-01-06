"""
Module for managing environment connections and selections.
"""
from .process_manager import ProcessManager

class EnvironmentManager:
    def __init__(self):
        # Dictionary to store environment connection commands (not visible to users)
        self._connection_commands = {
            'Local': '',  # Local environment doesn't need a connection command
            'Prod 1': 'Enter-PSSession -ComputerName prod1.example.com',
            'Prod 2': 'Enter-PSSession -ComputerName prod2.example.com'
        }
        # Initialize process manager for monitoring processes
        self.process_manager = ProcessManager()
        self.current_environment = None
    
    def get_environments(self):
        """Returns a list of available environment names."""
        return list(self._connection_commands.keys())
    
    def get_connection_command(self, environment_name):
        """
        Returns the connection command for the specified environment.
        This method should only be used internally by the application.
        """
        return self._connection_commands.get(environment_name)
    
    def select_environment(self, environment_name):
        """
        Select an environment and perform necessary initialization.
        Returns process statuses for the selected environment.
        """
        self.current_environment = environment_name
        # Check processes for any environment
        return self.process_manager.check_processes(environment_name, self.get_connection_command(environment_name))
    
    def get_current_environment(self):
        """Returns the currently selected environment."""
        return self.current_environment
    
    def get_process_statuses(self):
        """Returns the current process statuses for the current environment."""
        if not self.current_environment:
            return None
        return self.process_manager.check_processes(
            self.current_environment, 
            self.get_connection_command(self.current_environment)
        )
