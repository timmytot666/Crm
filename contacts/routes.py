from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from contacts.models import Contact
from contacts.forms import ContactForm
from urllib.parse import quote_plus
from common.utils import generate_entity_email_body

contacts_bp = Blueprint('contacts', __name__, template_folder='../templates/contacts')

@contacts_bp.route('/')
@login_required
def list_contacts():
    contacts = Contact.query.filter_by(user_id=current_user.id).all()
    return render_template('list_contacts.html', contacts=contacts, title='Contacts')

@contacts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone_primary=form.phone_primary.data,
            phone_secondary=form.phone_secondary.data,
            company_id=form.company_id.data if form.company_id.data and form.company_id.data != 0 else None,
            address=form.address.data,
            tags=form.tags.data,
            interaction_history=form.interaction_history.data,
            user_id=current_user.id
        )
        db.session.add(contact)
        db.session.commit()
        flash('Contact created successfully!', 'success')
        return redirect(url_for('contacts.list_contacts'))
    return render_template('create_edit_contact.html', form=form, title='Create Contact')

@contacts_bp.route('/<int:contact_id>/view')
@login_required
def view_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    # Add check: if contact.user_id != current_user.id: abort(403)

    email_subject = f"CRM Contact Information: {contact.name}"
    email_body = generate_entity_email_body(contact)
    mailto_link = f"mailto:?subject={quote_plus(email_subject)}&body={quote_plus(email_body)}".replace('+', '%20')

    return render_template('view_contact.html', contact=contact, title=contact.name, mailto_link=mailto_link)

@contacts_bp.route('/<int:contact_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    # Add check: if contact.user_id != current_user.id: abort(403)
    form = ContactForm(obj=contact)
    if form.validate_on_submit():
        contact.name = form.name.data
        contact.email = form.email.data
        contact.phone_primary = form.phone_primary.data
        contact.phone_secondary = form.phone_secondary.data
        contact.company_id = form.company_id.data if form.company_id.data and form.company_id.data != 0 else None
        contact.address = form.address.data
        contact.tags = form.tags.data
        contact.interaction_history = form.interaction_history.data
        db.session.commit()
        flash('Contact updated successfully!', 'success')
        return redirect(url_for('contacts.view_contact', contact_id=contact.id))
    return render_template('create_edit_contact.html', form=form, title='Edit Contact', contact=contact)

@contacts_bp.route('/<int:contact_id>/delete', methods=['POST']) # POST for safety
@login_required
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    # Add check: if contact.user_id != current_user.id: abort(403)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('contacts.list_contacts'))
