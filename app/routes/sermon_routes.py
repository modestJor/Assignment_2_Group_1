from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from app.repositories.sermon_repository import SermonRepository

sermon_bp = Blueprint('sermons', __name__)
repo = SermonRepository()

def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login_form'))
        return f(*args, **kwargs)
    return decorated

@sermon_bp.route('/')
@require_admin
def list_sermons():
    sermons = repo.find_all()
    return render_template('sermon.html', sermons=sermons)

@sermon_bp.route('/new', methods=['GET'])
@require_admin
def new_sermon_form():
    return render_template('add_sermon.html')

@sermon_bp.route('/new', methods=['POST'])
@require_admin
def create_sermon():
    title = request.form.get('title')
    speaker = request.form.get('speaker')
    content = request.form.get('content')
    date_preached = request.form.get('date_preached')
    
    repo.save(title, speaker, content, date_preached)
    flash('Sermon summary published!', 'success')
    return redirect(url_for('sermons.new_sermon_form'))

@sermon_bp.route('/<int:sermon_id>/delete', methods=['POST'])
@require_admin
def delete_sermon(sermon_id):
    sermon = repo.find_by_id(sermon_id)
    if sermon:
        repo.delete(sermon_id)
        flash('Sermon summary deleted.', 'success')
    else:
        flash('Sermon not found.', 'error')
    return redirect(url_for('sermons.list_sermons'))



