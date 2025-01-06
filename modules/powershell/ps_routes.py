"""
PowerShell routes module
Handles all PowerShell-related HTTP routes
"""

from flask import Blueprint, request, jsonify, g
from .ps_session import PSRemoteSession

def get_ps_session():
    """Get or create PSRemoteSession instance"""
    if not hasattr(g, 'ps_session'):
        g.ps_session = PSRemoteSession()
    return g.ps_session

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
