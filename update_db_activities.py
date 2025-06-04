from app import app, db
from activities.models import Activity

with app.app_context():
    print('Creating activity table...')
    db.create_all()
    print('Activity table check/creation complete.')
