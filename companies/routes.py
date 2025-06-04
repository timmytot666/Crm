from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from companies.models import Company
from companies.forms import CompanyForm
from contacts.models import Contact # For listing contacts of a company
from urllib.parse import quote_plus
from common.utils import generate_entity_email_body

companies_bp = Blueprint('companies', __name__, template_folder='../templates/companies')

@companies_bp.route('/')
@login_required
def list_companies():
    companies = Company.query.filter_by(user_id=current_user.id).all()
    return render_template('list_companies.html', companies=companies, title='Companies')

@companies_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_company():
    form = CompanyForm()
    if form.validate_on_submit():
        company = Company(
            name=form.name.data,
            industry=form.industry.data,
            website=form.website.data,
            address=form.address.data,
            primary_contact_name=form.primary_contact_name.data,
            user_id=current_user.id
        )
        db.session.add(company)
        db.session.commit()
        flash('Company created successfully!', 'success')
        return redirect(url_for('companies.list_companies'))
    return render_template('create_edit_company.html', form=form, title='Create Company')

@companies_bp.route('/<int:company_id>/view')
@login_required
def view_company(company_id):
    company = Company.query.get_or_404(company_id)
    # Add check for user_id if necessary for authorization

    email_subject = f"CRM Company Information: {company.name}"
    email_body = generate_entity_email_body(company)
    mailto_link = f"mailto:?subject={quote_plus(email_subject)}&body={quote_plus(email_body)}".replace('+', '%20')

    return render_template('view_company.html', company=company, title=company.name, mailto_link=mailto_link)

@companies_bp.route('/<int:company_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_company(company_id):
    company = Company.query.get_or_404(company_id)
    # Add check for user_id
    form = CompanyForm(obj=company)
    if form.validate_on_submit():
        company.name = form.name.data
        company.industry = form.industry.data
        company.website = form.website.data
        company.address = form.address.data
        company.primary_contact_name = form.primary_contact_name.data
        db.session.commit()
        flash('Company updated successfully!', 'success')
        return redirect(url_for('companies.view_company', company_id=company.id))
    return render_template('create_edit_company.html', form=form, title='Edit Company', company=company)

@companies_bp.route('/<int:company_id>/delete', methods=['POST'])
@login_required
def delete_company(company_id):
    company = Company.query.get_or_404(company_id)
    # Add check for user_id
    if company.contacts.count() > 0:
        flash('Cannot delete company: it has associated contacts. Please reassign or delete them first.', 'danger')
        return redirect(url_for('companies.list_companies'))
    # Add similar check for deals associated with company if that relationship exists and is important
    # if company.deals.count() > 0:
    #     flash('Cannot delete company: it has associated deals. Please reassign or delete them first.', 'danger')
    #     return redirect(url_for('companies.list_companies'))
    db.session.delete(company)
    db.session.commit()
    flash('Company deleted successfully!', 'success')
    return redirect(url_for('companies.list_companies'))
