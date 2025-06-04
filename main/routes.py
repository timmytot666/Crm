from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from contacts.models import Contact
from companies.models import Company
from deals.models import Deal

main_bp = Blueprint('main', __name__, template_folder='../templates/main') # Assuming templates/main for search results

@main_bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    results = {}

    if query:
        search_term = f'%{query}%'
        results['contacts'] = Contact.query.filter(
            Contact.user_id == current_user.id,
            or_(Contact.name.ilike(search_term), Contact.email.ilike(search_term))
        ).all()

        results['companies'] = Company.query.filter(
            Company.user_id == current_user.id,
            Company.name.ilike(search_term)
        ).all()

        results['deals'] = Deal.query.filter(
            Deal.user_id == current_user.id,
            Deal.name.ilike(search_term)
        ).all()
    return render_template('search_results.html', query=query, results=results, title='Search Results')
