from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from activities.models import Activity
from activities.forms import ActivityForm
from datetime import datetime

activities_bp = Blueprint('activities', __name__, template_folder='../templates/activities')

@activities_bp.route('/')
@login_required
def list_activities():
    # For MVP, list all activities by user. Could be filtered by open/closed tasks, due date etc. later
    activities = Activity.query.filter_by(user_id=current_user.id).order_by(Activity.due_date.asc().nullslast(), Activity.created_at.desc()).all()
    return render_template('list_activities.html', activities=activities, title='Activities')

@activities_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_activity():
    form = ActivityForm()
    # Pre-fill association if coming from another entity's page
    contact_arg = request.args.get('contact_id', type=int)
    company_arg = request.args.get('company_id', type=int)
    deal_arg = request.args.get('deal_id', type=int)
    if request.method == 'GET':
        if contact_arg: form.contact_id.data = contact_arg
        if company_arg: form.company_id.data = company_arg
        if deal_arg: form.deal_id.data = deal_arg

    if form.validate_on_submit():
        activity = Activity(
            subject=form.subject.data,
            activity_type=form.activity_type.data,
            notes=form.notes.data,
            due_date=form.due_date.data,
            contact_id=form.contact_id.data if form.contact_id.data != 0 else None,
            company_id=form.company_id.data if form.company_id.data != 0 else None,
            deal_id=form.deal_id.data if form.deal_id.data != 0 else None,
            user_id=current_user.id
        )
        db.session.add(activity)
        db.session.commit()
        flash('Activity created successfully!', 'success')
        # Redirect to associated entity or list view
        if activity.deal_id: return redirect(url_for('deals.view_deal', deal_id=activity.deal_id))
        if activity.contact_id: return redirect(url_for('contacts.view_contact', contact_id=activity.contact_id))
        if activity.company_id: return redirect(url_for('companies.view_company', company_id=activity.company_id))
        return redirect(url_for('activities.list_activities'))
    return render_template('create_edit_activity.html', form=form, title='Create Activity')

@activities_bp.route('/<int:activity_id>/view')
@login_required
def view_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    # Add authorization: if activity.user_id != current_user.id: abort(403)
    return render_template('view_activity.html', activity=activity, title=activity.subject)

@activities_bp.route('/<int:activity_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    # Add authorization
    form = ActivityForm(obj=activity)
    if form.validate_on_submit():
        activity.subject = form.subject.data
        activity.activity_type = form.activity_type.data
        activity.notes = form.notes.data
        activity.due_date = form.due_date.data
        activity.contact_id = form.contact_id.data if form.contact_id.data != 0 else None
        activity.company_id = form.company_id.data if form.company_id.data != 0 else None
        activity.deal_id = form.deal_id.data if form.deal_id.data != 0 else None
        db.session.commit()
        flash('Activity updated successfully!', 'success')
        return redirect(url_for('activities.view_activity', activity_id=activity.id))
    return render_template('create_edit_activity.html', form=form, title='Edit Activity', activity=activity)

@activities_bp.route('/<int:activity_id>/delete', methods=['POST'])
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    # Add authorization
    db.session.delete(activity)
    db.session.commit()
    flash('Activity deleted successfully!', 'success')
    return redirect(request.referrer or url_for('activities.list_activities'))

@activities_bp.route('/<int:activity_id>/complete', methods=['POST'])
@login_required
def complete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    # Add authorization
    if activity.completed_at is None:
        activity.completed_at = datetime.utcnow()
        flash(f'Activity "{activity.subject}" marked as complete.', 'success')
    else:
        activity.completed_at = None # Allow un-completing
        flash(f'Activity "{activity.subject}" marked as incomplete.', 'info')
    db.session.commit()
    return redirect(request.referrer or url_for('activities.list_activities'))
