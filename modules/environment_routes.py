"""
Module for handling environment-related routes.
"""
from flask import Blueprint, jsonify, request, session, current_app
from .environment_manager import EnvironmentManager

# Create Blueprint
environment_bp = Blueprint('environment', __name__)

# Initialize environment manager
env_manager = EnvironmentManager()

@environment_bp.route('/select', methods=['POST'])
def select_environment():
    """Handle environment selection."""
    if 'username' not in session or 'encrypted_password' not in session:
        return jsonify({'success': False, 'error': 'User not authenticated'}), 401
        
    data = request.get_json()
    environment = data.get('environment')
    
    if not environment:
        return jsonify({'error': 'No environment specified'}), 400
        
    try:
        # Get decrypted credentials from session
        username = session['username']
        encrypted_password = session['encrypted_password']
        credential_manager = current_app.credential_manager
        password = credential_manager.decrypt_password(encrypted_password)
        
        # Select environment using session credentials
        success, error = env_manager.select_environment(environment, username, password)
        
        if success:
            return jsonify({
                'success': True,
                'environment': environment
            })
        else:
            return jsonify({
                'success': False,
                'error': error
            }), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@environment_bp.route('/status', methods=['POST'])
def get_status():
    """Get current environment connection status."""
    if 'username' not in session:
        return jsonify({'status': 'disconnected', 'error': 'User not authenticated'}), 401
        
    try:
        data = request.get_json()
        environment = data.get('environment')
        
        if not environment:
            return jsonify({'status': 'disconnected'})
        
        # Get connection status for the environment
        status = env_manager.get_connection_status()
        
        if not status:
            return jsonify({'status': 'disconnected'})
            
        # If connected to a remote server, verify connection is still working
        if status.get('status') == 'connected':
            server_name = status.get('server')
            success, _, error = env_manager.session_manager.execute_command(
                server_name,
                "$Host.Version | Select-Object -Property Major,Minor | ConvertTo-Json"
            )
            if not success:
                status['status'] = 'disconnected'
                status['error'] = error
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
