"""
Module for handling environment-related routes.
"""
from flask import Blueprint, jsonify, request
from .environment_manager import EnvironmentManager

# Create Blueprint
environment_bp = Blueprint('environment', __name__)

# Initialize environment manager
env_manager = EnvironmentManager()

@environment_bp.route('/select', methods=['POST'])
def select_environment():
    """Handle environment selection."""
    data = request.get_json()
    environment = data.get('environment')
    
    if not environment:
        return jsonify({'error': 'No environment specified'}), 400
        
    try:
        # Select environment and get process statuses if Local
        process_statuses = env_manager.select_environment(environment)
        
        response = {
            'status': 'success',
            'environment': environment,
        }
        
        # Include process statuses if available (for Local environment)
        if process_statuses is not None:
            response['process_statuses'] = process_statuses
            
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
