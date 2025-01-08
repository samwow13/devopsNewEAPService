"""
Module for managing environment connections and selections.
"""
from .process_manager import ProcessManager
from .ps_session_manager import PSSessionManager
from datetime import datetime

class EnvironmentManager:
    def __init__(self):
        # Dictionary to store environment connection details (not visible to users)
        self._environments = {
            'Local': {'server': 'localhost'},  # Local environment
            'WPDHSappl84': {'server': 'WPDHSappl84'}  # Production server
        }
        # Initialize managers
        self.process_manager = ProcessManager()
        self.session_manager = PSSessionManager()
        self.current_environment = None
    
    def _log_ps_action(self, server, action, details=None, error=None):
        """Internal method to log PowerShell actions to console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] PowerShell Action on {server}: {action}"
        if details:
            log_msg += f"\nDetails: {details}"
        if error:
            log_msg += f"\nError: {error}"
        print(log_msg)
    
    def get_environments(self):
        """Returns a list of available environment names."""
        return list(self._environments.keys())
    
    def get_server_name(self, environment_name):
        """
        Returns the server name for the specified environment.
        This method should only be used internally by the application.
        """
        env = self._environments.get(environment_name)
        return env['server'] if env else None
    
    def select_environment(self, environment_name, username=None, password=None):
        """
        Select an environment and establish a connection if needed.
        
        Args:
            environment_name (str): Name of the environment to select
            username (str, optional): Username for remote connection
            password (str, optional): Password for remote connection
            
        Returns:
            tuple: (bool, str) - (Success status, Error message if any)
        """
        if environment_name not in self._environments:
            self._log_ps_action("N/A", "Environment Selection Failed", 
                              error="Invalid environment selected")
            return False, "Invalid environment selected"
            
        self.current_environment = environment_name
        server_name = self.get_server_name(environment_name)
        
        # Local environment doesn't need a session
        if server_name == 'localhost':
            self._log_ps_action(server_name, "Local Environment Selected")
            return True, None
            
        # Check if we already have stored credentials
        if self.session_manager.has_credentials(server_name):
            self._log_ps_action(server_name, "Using Existing Credentials")
            return True, None
            
        # Store new credentials if provided
        if username and password:
            self._log_ps_action(server_name, "Storing New Credentials", 
                              details=f"Username: {username}")
            self.session_manager.store_credentials(server_name, username, password)
            
            # Test connection by checking JBoss services
            success, output = self.session_manager.check_jboss_services(server_name)
            if success:
                self._log_ps_action(server_name, "Service Check", details=output)
            else:
                self._log_ps_action(server_name, "Service Check Failed", error=output)
                
            return True, None
            
        self._log_ps_action(server_name, "Connection Failed", 
                          error="Credentials required for remote connection")
        return False, "Credentials required for remote connection"
    
    def get_current_environment(self):
        """Returns the currently selected environment."""
        return self.current_environment
    
    def get_connection_status(self):
        """
        Returns the status of the current environment's connection.
        
        Returns:
            dict: Connection information if exists, None otherwise
        """
        if not self.current_environment:
            return None
            
        server_name = self.get_server_name(self.current_environment)
        if server_name == 'localhost':
            return {'status': 'local', 'server': 'localhost'}
            
        credentials = self.session_manager.get_credentials(server_name)
        if credentials:
            return {
                'status': 'connected',
                'server': server_name,
                'username': credentials['username']
            }
        return {'status': 'disconnected', 'server': server_name}
    
    def remove_credentials(self):
        """
        Removes the current environment's credentials if it exists.
        
        Returns:
            bool: True if credentials were removed successfully or didn't exist, False otherwise
        """
        if not self.current_environment:
            return True
            
        server_name = self.get_server_name(self.current_environment)
        if server_name == 'localhost':
            return True
            
        return self.session_manager.remove_credentials(server_name)
