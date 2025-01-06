from flask import Flask, render_template
import os

# Initialize Flask application
app = Flask(__name__)

# Configure session
app.secret_key = os.urandom(24)  # Generate a random secret key for session management

# Import routes after Flask app initialization to avoid circular imports
from modules.auth.auth_routes import auth_bp

# Register blueprints
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
