from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Optional
from companies.models import Company # Import Company
# from wtforms_sqlalchemy.fields import QuerySelectField # This would be another way

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_primary = StringField('Primary Phone')
    phone_secondary = StringField('Secondary Phone')
    # company_name = StringField('Company Affiliation') # Old field, removed
    company_id = SelectField('Company', coerce=int, validators=[Optional()]) # New field
    address = TextAreaField('Address')
    tags = StringField('Tags (comma-separated)')
    interaction_history = TextAreaField('Interaction History (Manual Log)')
    submit = SubmitField('Save Contact')

    def __init__(self, *args, **kwargs): # To populate choices
        super(ContactForm, self).__init__(*args, **kwargs)
        self.company_id.choices = [(0, '--- No Company ---')] + [(c.id, c.name) for c in Company.query.order_by(Company.name).all()]
        # Ensure the default or existing value is handled correctly if it's 0 or None
        if self.company_id.data is None or self.company_id.data == 0:
             self.company_id.data = 0 # Default to '--- No Company ---' if no specific company is set
        elif isinstance(self.company_id.data, int) and self.company_id.data > 0:
            # if data is already set (e.g. editing an existing contact), keep it
            pass
        else: # Fallback if data is somehow not an int (e.g. on initial form load without obj)
            self.company_id.data = 0
