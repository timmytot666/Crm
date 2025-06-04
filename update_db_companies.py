from app import app, db
from companies.models import Company # Ensure Company model is imported
from contacts.models import Contact # Ensure Contact model is imported for relationship update

with app.app_context():
    print('Creating company table and updating contact table for company foreign key...')
    db.create_all() # This should add companies table and modify contacts table (if column type change or new FK)
    print('Company table and contact table update check/creation complete.')
