from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from app.repositories.announcement_repository import AnnouncementRepository

announcement_bp = Blueprint('announcements', __name__)
repo = AnnouncementRepository()


def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login_form'))
        return f(*args, **kwargs)
    return decorated


@announcement_bp.route('/')
@require_admin
def list_announcements():
    """Display all announcements."""
    announcements = repo.find_all()
    return render_template('announcements.html', announcements=announcements)


@announcement_bp.route('/new', methods=['GET'])
@require_admin
def new_announcement_form():
    """Show the create announcement form."""
    return render_template('add_announcement.html')


@announcement_bp.route('/new', methods=['POST'])
@require_admin
def create_announcement():
    """Handle announcement form submission."""
    title   = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    if not title or not content:
        flash('Title and content are required.', 'error')
        return render_template('add_announcement.html')

    posted_by = session.get('admin_username', 'Admin')
    repo.save(title, content, posted_by)
    flash(f'Announcement "{title}" published successfully.', 'success')
    return redirect(url_for('announcements.list_announcements'))


@announcement_bp.route('/<int:announcement_id>/delete', methods=['POST'])
@require_admin
def delete_announcement(announcement_id):
    """Delete an announcement."""
    announcement = repo.find_by_id(announcement_id)
    if announcement:
        repo.delete(announcement_id)
        flash(f'Announcement deleted.', 'success')
    else:
        flash('Announcement not found.', 'error')
    return redirect(url_for('announcements.list_announcements'))