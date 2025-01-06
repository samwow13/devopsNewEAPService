from flask import Blueprint, render_template, request, redirect, url_for, session

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def login():
    """Render the login page"""
    if 'username' in session:
        return redirect(url_for('auth.landing'))
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def handle_login():
    """Handle login form submission and store username in session
    
    Accepts any credentials and redirects to landing page
    """
    # Get form data (not validated as per requirements)
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Store username in session
    session['username'] = username
    
    # Redirect to landing page (no validation required)
    return redirect(url_for('auth.landing'))

@auth_bp.route('/landing')
def landing():
    """Render the landing page with user information"""
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('landing.html', username=session['username'])

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Clear user session and redirect to login page"""
    session.clear()  # Remove all session data
    return redirect(url_for('auth.login'))
