from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, URL

class CompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    industry = StringField('Industry')
    website = StringField('Website', validators=[Optional(), URL()])
    address = TextAreaField('Address')
    primary_contact_name = StringField('Primary Contact Name')
    submit = SubmitField('Save Company')
