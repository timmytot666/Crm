from app import db
from datetime import datetime

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # e.g., Call, Email, Meeting, Task
    notes = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=True) # For tasks
    completed_at = db.Column(db.DateTime, nullable=True) # Mark when completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign keys for associations
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    deal_id = db.Column(db.Integer, db.ForeignKey('deals.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # User who logged/owns the activity

    # Relationships
    contact = db.relationship('Contact', backref=db.backref('activities', lazy='dynamic'))
    company = db.relationship('Company', backref=db.backref('activities', lazy='dynamic'))
    deal = db.relationship('Deal', backref=db.backref('activities', lazy='dynamic'))

    def __repr__(self):
        return f'<Activity {self.subject}>'

    ACTIVITY_TYPES = ['Call', 'Email', 'Meeting', 'Task', 'Other'] # Predefined types
