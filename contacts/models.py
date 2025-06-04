from app import db
from datetime import datetime

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    phone_primary = db.Column(db.String(20))
    phone_secondary = db.Column(db.String(20))
    address = db.Column(db.String(256))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    tags = db.Column(db.String(256))  # Simple comma-separated tags for MVP
    interaction_history = db.Column(db.Text) # Manual log for MVP
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Foreign key to User who created/owns this contact - basic ownership
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Contact {self.name}>'
