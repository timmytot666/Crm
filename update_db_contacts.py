from app import app, db
from contacts.models import Contact # Ensure Contact model is imported

with app.app_context():
    print('Creating contact table if it does not exist...')
    db.create_all() # This will create tables that don't exist yet
    print('Contact table check/creation complete.')
