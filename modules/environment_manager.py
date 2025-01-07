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
        Select an environment and establish a PowerShell session if needed.
        
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
            
        # Check if we already have an active session
        if self.session_manager.has_active_session(server_name):
            self._log_ps_action(server_name, "Using Existing Session")
            return True, None
            
        # Create new session if credentials provided
        if username and password:
            self._log_ps_action(server_name, "Creating New Session", 
                              details=f"Username: {username}, Password: {password} [TEST MODE - Remove in production]")
            success, ps_script, actual_command = self.session_manager.create_session(server_name, username, password)
            if not success:
                error_msg = self.session_manager.get_last_error()
                self._log_ps_action(server_name, "Session Creation Failed", 
                                  error=error_msg)
                return False, f"Failed to create session: {error_msg}"
            
            # Log both the PowerShell script and actual command
            self._log_ps_action(server_name, "PowerShell Script", 
                              details=f"Script to execute:\n{ps_script}")
            self._log_ps_action(server_name, "Actual Command", 
                              details=f"Command executed:\n{actual_command}")
            
            # Check JBoss services after successful connection
            success, output = self.session_manager.check_services(server_name)
            if success:
                self._log_ps_action(server_name, "Service Check", details=output)
            else:
                self._log_ps_action(server_name, "Service Check Failed", error=output)
                
            return True, None
            
        self._log_ps_action(server_name, "Session Creation Failed", 
                          error="Credentials required for remote connection")
        return False, "Credentials required for remote connection"
    
    def get_current_environment(self):
        """Returns the currently selected environment."""
        return self.current_environment
    
    def get_session_status(self):
        """
        Returns the status of the current environment's session.
        
        Returns:
            dict: Session information if exists, None otherwise
        """
        if not self.current_environment:
            return None
            
        server_name = self.get_server_name(self.current_environment)
        if server_name == 'localhost':
            return {'status': 'local', 'server': 'localhost'}
            
        session = self.session_manager.get_session(server_name)
        if session:
            return {
                'status': 'connected',
                'server': server_name,
                'created_at': session['created_at']
            }
        return {'status': 'disconnected', 'server': server_name}
    
    def close_session(self):
        """
        Closes the current environment's session if it exists.
        
        Returns:
            bool: True if session was closed successfully or didn't exist, False otherwise
        """
        if not self.current_environment:
            return True
            
        server_name = self.get_server_name(self.current_environment)
        if server_name == 'localhost':
            return True
            
        return self.session_manager.remove_session(server_name)
