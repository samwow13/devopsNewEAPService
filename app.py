from flask import Flask, render_template
import os
from modules.auth.credential_manager import CredentialManager

# Initialize Flask application
app = Flask(__name__)

# Configure session
app.secret_key = os.urandom(24)  # Generate a random secret key for session management

# Initialize CredentialManager
credential_manager = CredentialManager()
credential_manager.init_app(app)
app.credential_manager = credential_manager  # Attach to app

# Import routes after Flask app initialization to avoid circular imports
from modules.auth.auth_routes import auth_bp
from modules.powershell.ps_routes import ps_bp
from modules.environment_routes import environment_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(ps_bp)
app.register_blueprint(environment_bp, url_prefix='/environment')

if __name__ == '__main__':
    app.run(debug=True)
