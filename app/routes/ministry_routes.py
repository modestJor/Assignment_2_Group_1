from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.repositories.ministry_repository import MinistryRepository
from app.decorators import require_admin

ministry_bp = Blueprint('ministries', __name__)
repo = MinistryRepository()


@ministry_bp.route('/')
@require_admin
def list_ministries():
    ministries = repo.find_all()
    return render_template('ministries.html', ministries=ministries)


@ministry_bp.route('/new', methods=['GET'])
@require_admin
def new_ministry_form():
    return render_template('add_ministry.html')


@ministry_bp.route('/new', methods=['POST'])
@require_admin
def create_ministry():
    name         = request.form.get('name', '').strip()
    description  = request.form.get('description', '').strip()
    leader_name  = request.form.get('leader_name', '').strip()
    leader_contact = request.form.get('leader_contact', '').strip()

    if not name:
        flash('Ministry name is required.', 'error')
        return render_template('add_ministry.html')

    repo.save(name, description, leader_name, leader_contact)
    flash(f'Ministry "{name}" created successfully.', 'success')
    return redirect(url_for('ministries.list_ministries'))


@ministry_bp.route('/<int:ministry_id>/delete', methods=['POST'])
@require_admin
def delete_ministry(ministry_id):
    ministry = repo.find_by_id(ministry_id)
    if ministry:
        repo.delete(ministry_id)
        flash(f'Ministry "{ministry.name}" deleted.', 'success')
    else:
        flash('Ministry not found.', 'error')
    return redirect(url_for('ministries.list_ministries'))