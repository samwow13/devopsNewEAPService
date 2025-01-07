"""
PowerShell routes module
Handles all PowerShell-related HTTP routes
"""

from flask import Blueprint, request, jsonify, g
from .ps_command import PSCommandExecutor

def get_ps_executor():
    """Get or create PSCommandExecutor instance"""
    if not hasattr(g, 'ps_executor'):
        g.ps_executor = PSCommandExecutor()
    return g.ps_executor

# Create blueprint
ps_bp = Blueprint('ps', __name__, url_prefix='/ps')

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

        # Execute command using executor from request context
        ps_executor = get_ps_executor()
        result = ps_executor.execute_command(data['command'])
        
        return jsonify({
            'status': 'success',
            'output': result,
            'mode': 'Local'  # Always local mode now
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'output': str(e)
        }), 500
