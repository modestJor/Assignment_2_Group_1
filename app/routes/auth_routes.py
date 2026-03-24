from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from app.services.authenticate import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()


@auth_bp.route('/login', methods=['GET'])
def login_form():
    """Show the login page."""
    if session.get('admin_id'):
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')


@auth_bp.route('/login', methods=['POST'])
def login():
    """Handle login form submission."""
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        admin = auth_service.verify_credentials(username, password)
        session['admin_id'] = admin.id
        session['admin_username'] = admin.username
        flash('Login successful. Welcome back!', 'success')
        return redirect(url_for('main.dashboard'))
    except ValueError:
        flash('Invalid username or password.', 'error')
        return redirect(url_for('auth.login_form'))


@auth_bp.route('/logout')
def logout():
    """Clear session and redirect to login."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login_form'))
