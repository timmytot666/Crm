from app import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    industry = db.Column(db.String(128))
    website = db.Column(db.String(128))
    address = db.Column(db.String(256))
    # For MVP, primary_contact can be a string. Later, it could be a ForeignKey to a Contact.
    primary_contact_name = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # Associated user

    # Relationship: A company can have multiple contacts
    contacts = db.relationship('Contact', backref='company', lazy='dynamic')

    def __repr__(self):
        return f'<Company {self.name}>'
