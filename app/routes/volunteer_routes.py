from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.repositories.volunteer_repository import VolunteerRepository
from app.decorators import require_admin

volunteer_bp = Blueprint('volunteers', __name__)
repo = VolunteerRepository()


# ── Activity Routes ──────────────────────────────────────────

@volunteer_bp.route('/')
@require_admin
def list_activities():
    activities = repo.find_all_activities()
    return render_template('volunteers/activities.html', activities=activities)


@volunteer_bp.route('/new', methods=['GET'])
@require_admin
def new_activity_form():
    return render_template('volunteers/add_activity.html')


@volunteer_bp.route('/new', methods=['POST'])
@require_admin
def create_activity():
    title       = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    date_str    = request.form.get('date', '').strip()
    location    = request.form.get('location', '').strip()

    if not title:
        flash('Title is required.', 'error')
        return render_template('volunteers/add_activity.html')

    repo.save_activity(title, description, date_str, location, max_volunteers=0)
    flash(f'Activity "{title}" created successfully!', 'success')
    return redirect(url_for('volunteers.list_activities'))


@volunteer_bp.route('/<int:activity_id>/delete', methods=['POST'])
@require_admin
def delete_activity(activity_id):
    activity = repo.find_activity_by_id(activity_id)
    if activity:
        repo.delete_activity(activity_id)
        flash(f'Activity "{activity.title}" deleted successfully!', 'success')
    else:
        flash('Activity not found.', 'error')
    return redirect(url_for('volunteers.list_activities'))


# ── Signup Routes ─────────────────────────────────────────────

@volunteer_bp.route('/<int:activity_id>/registrations')
@require_admin
def view_registrations(activity_id):
    """View signups for an activity."""
    activity = repo.find_activity_by_id(activity_id)
    if not activity:
        flash('Activity not found.', 'error')
        return redirect(url_for('volunteers.list_activities'))
    signups = activity.signups
    return render_template('volunteers/registrations.html',
                            activity=activity, signups=signups)


@volunteer_bp.route('/<int:activity_id>/signup', methods=['POST'])
@require_admin
def signup_for_activity(activity_id):
    volunteer_name = request.form.get('volunteer_name', '').strip()
    contact_info   = request.form.get('contact_info', '').strip()

    if not volunteer_name:
        flash('Volunteer name is required.', 'error')
        return redirect(url_for('volunteers.view_registrations', activity_id=activity_id))

    try:
        repo.signup_for_activity(activity_id, volunteer_name, contact_info)
        flash(f'"{volunteer_name}" signed up successfully!', 'success')
    except Exception:
        flash('An error occurred while signing up. Please try again.', 'error')
    return redirect(url_for('volunteers.view_registrations', activity_id=activity_id))


@volunteer_bp.route('/<int:activity_id>/unregister', methods=['POST'])
@require_admin
def unregister_from_activity(activity_id):
    volunteer_name = request.form.get('volunteer_name', '').strip()
    try:
        repo.unregister_from_activity(activity_id, volunteer_name)
        flash(f'"{volunteer_name}" has been removed.', 'success')
    except Exception:
        flash('An error occurred while unregistering. Please try again.', 'error')
    return redirect(url_for('volunteers.view_registrations', activity_id=activity_id))