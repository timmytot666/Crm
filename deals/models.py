from app import db
from datetime import datetime

class PipelineStage(db.Model):
    __tablename__ = 'pipeline_stages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    order = db.Column(db.Integer, nullable=False, default=0) # For ordering stages in pipeline
    deals = db.relationship('Deal', backref='stage', lazy='dynamic')

    def __repr__(self):
        return f'<PipelineStage {self.name}>'

    @staticmethod
    def insert_initial_stages():
        stages = {
            'Lead': 1,
            'Qualified': 2,
            'Proposal Sent': 3,
            'Negotiation': 4,
            'Closed Won': 5,
            'Closed Lost': 6
        }
        for stage_name, stage_order in stages.items():
            stage = PipelineStage.query.filter_by(name=stage_name).first()
            if not stage:
                stage = PipelineStage(name=stage_name, order=stage_order)
                db.session.add(stage)
        db.session.commit()

class Deal(db.Model):
    __tablename__ = 'deals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    value = db.Column(db.Numeric(10, 2)) # Deal value, e.g., 10000.00
    expected_close_date = db.Column(db.Date)
    probability = db.Column(db.Integer)  # Percentage, e.g., 75 for 75%
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pipeline_stage_id = db.Column(db.Integer, db.ForeignKey('pipeline_stages.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    contact = db.relationship('Contact', backref=db.backref('deals', lazy='dynamic'))
    company = db.relationship('Company', backref=db.backref('deals', lazy='dynamic'))

    def __repr__(self):
        return f'<Deal {self.name}>'
