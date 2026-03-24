from functools import wraps
from flask import Blueprint, redirect, url_for, render_template, session, flash
from app.models import Member, Ministry

main_bp = Blueprint('main', __name__)


def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login_form'))
        return f(*args, **kwargs)
    return decorated


@main_bp.route('/')
def index():
    """Redirect root to dashboard or login."""
    if session.get('admin_id'):
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login_form'))


@main_bp.route('/dashboard')
@require_admin
def dashboard():
    """Admin dashboard with summary stats."""
    total_members  = Member.query.count()
    active_members = Member.query.filter_by(status='Active').count()
    total_ministries = Ministry.query.count()
    return render_template(
        'dashboard.html',
        admin_username=session.get('admin_username', 'Admin'),
        total_members=total_members,
        active_members=active_members,
        total_ministries=total_ministries
    )
