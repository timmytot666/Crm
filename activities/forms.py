from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional
from contacts.models import Contact
from companies.models import Company
from deals.models import Deal
from activities.models import Activity # To access ACTIVITY_TYPES

class ActivityForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    activity_type = SelectField('Activity Type', choices=[(at, at) for at in Activity.ACTIVITY_TYPES], validators=[DataRequired()])
    notes = TextAreaField('Notes')
    due_date = DateTimeField('Due Date (YYYY-MM-DD HH:MM:SS)', format='%Y-%m-%d %H:%M:%S', validators=[Optional()])
    # completed = BooleanField('Completed', validators=[Optional()]) # For marking task as done, alternative to completed_at
    contact_id = SelectField('Associated Contact', coerce=int, validators=[Optional()])
    company_id = SelectField('Associated Company', coerce=int, validators=[Optional()])
    deal_id = SelectField('Associated Deal', coerce=int, validators=[Optional()])
    submit = SubmitField('Save Activity')

    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        # Populate choices for association fields
        # Consider filtering these by current_user if applicable or making them searchable for large datasets
        self.contact_id.choices = [(0, '--- None ---')] + [(c.id, c.name) for c in Contact.query.order_by(Contact.name).all()]
        self.company_id.choices = [(0, '--- None ---')] + [(c.id, c.name) for c in Company.query.order_by(Company.name).all()]
        self.deal_id.choices = [(0, '--- None ---')] + [(d.id, d.name) for d in Deal.query.order_by(Deal.name).all()]
