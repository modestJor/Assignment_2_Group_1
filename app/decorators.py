from functools import wraps
from flask import session, flash, redirect, url_for


def require_admin(f):
    """
    Route decorator — redirects to login if no admin session exists.
    Apply to any route that requires authentication.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login_form'))
        return f(*args, **kwargs)
    return decorated