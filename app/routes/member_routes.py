from functools import wraps
from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from app.models import Member, Ministry
from app.repositories.member_repos import MemberRepository
from app.decorators import require_admin

member_bp = Blueprint('members', __name__)
repo = MemberRepository()


@member_bp.route('/')
@require_admin
def list_members():
    """Show all members, with optional name search."""
    search_query = request.args.get('search', '').strip()
    if search_query:
        members = repo.find_by_name(search_query)
    else:
        members = repo.get_all()
    return render_template('members.html', members=members, search_query=search_query)


@member_bp.route('/add', methods=['GET'])
@require_admin
def add_member_form():
    """Show the add member form."""
    ministries = Ministry.query.all()
    return render_template('add_member.html', ministries=ministries)


@member_bp.route('/add', methods=['POST'])
@require_admin
def add_member():
    """Handle add member form submission."""
    ministry_id = request.form.get('ministry_id') or None
    member = Member(
        name=request.form.get('name'),
        contact_info=request.form.get('contact_info'),
        dob=request.form.get('dob') or None,
        address=request.form.get('address'),
        status=request.form.get('status', 'Active'),
        ministry_id=int(ministry_id) if ministry_id else None
    )
    if not member.validate():
        flash('Name and contact info are required.', 'error')
        return redirect(url_for('members.add_member_form'))
    repo.save(member)
    flash(f'Member "{member.name}" added successfully.', 'success')
    return redirect(url_for('members.list_members'))


@member_bp.route('/<int:member_id>/edit', methods=['GET'])
@require_admin
def edit_member_form(member_id):
    """Show the edit member form."""
    member = repo.find_by_id(member_id)
    if not member:
        flash('Member not found.', 'error')
        return redirect(url_for('members.list_members'))
    ministries = Ministry.query.all()
    return render_template('edit_member.html', member=member, ministries=ministries)


@member_bp.route('/<int:member_id>/edit', methods=['POST'])
@require_admin
def update_member(member_id):
    """Handle edit member form submission."""
    ministry_id = request.form.get('ministry_id') or None
    data = {
        'name':         request.form.get('name'),
        'contact_info': request.form.get('contact_info'),
        'dob':          request.form.get('dob') or None,
        'address':      request.form.get('address'),
        'status':       request.form.get('status'),
        'ministry_id':  int(ministry_id) if ministry_id else None
    }
    try:
        member = repo.update(member_id, data)
        flash(f'Member "{member.name}" updated successfully.', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    return redirect(url_for('members.list_members'))


@member_bp.route('/<int:member_id>/delete', methods=['POST'])
@require_admin
def delete_member(member_id):
    """Remove a member record."""
    try:
        member = repo.find_by_id(member_id)
        name = member.name if member else 'Member'
        repo.delete(member_id)
        flash(f'"{name}" has been removed.', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    return redirect(url_for('members.list_members'))