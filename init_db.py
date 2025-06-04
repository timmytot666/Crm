from app import app, db
from users.models import insert_roles # Corrected import

with app.app_context():
    print('Creating database tables...')
    db.create_all()
    print('Inserting roles...')
    insert_roles()
    print('Database initialized.')
