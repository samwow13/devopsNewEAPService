"""
PowerShell routes module
Handles all PowerShell-related HTTP routes
"""

from flask import Blueprint, request, jsonify, g
from .ps_session import PSRemoteSession
from .ps_command import PSCommandExecutor

def get_ps_session():
    """Get or create PSRemoteSession instance"""
    if not hasattr(g, 'ps_session'):
        g.ps_session = PSRemoteSession()
    return g.ps_session

def get_ps_executor():
    """Get or create PSCommandExecutor instance"""
    if not hasattr(g, 'ps_executor'):
        g.ps_executor = PSCommandExecutor()
    return g.ps_executor

# Create blueprint
ps_bp = Blueprint('ps', __name__, url_prefix='/ps')

@ps_bp.route('/test-connection', methods=['POST'])
def test_connection():
    """Handle PowerShell test connection requests"""
    try:
        data = request.get_json()
        if not data or 'computer_name' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Computer name is required',
                'command': 'No command executed',
                'raw_output': 'Missing computer name in request'
            }), 400

        # Test the connection using session from request context
        ps_session = get_ps_session()
        result = ps_session.test_connection(data['computer_name'])
        return jsonify(result)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'command': 'Error executing command',
            'raw_output': str(e)
        }), 500

@ps_bp.route('/execute-command', methods=['POST'])
def execute_command():
    """Handle PowerShell command execution requests"""
    try:
        data = request.get_json()
        if not data or 'command' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Command is required',
                'output': 'Missing command in request'
            }), 400

        # Execute the command using executor from request context
        ps_executor = get_ps_executor()
        result = ps_executor.execute_command(data['command'])
        
        return jsonify({
            'status': result['status'],
            'output': result['output']
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'output': f'Error executing command: {str(e)}'
        }), 500
