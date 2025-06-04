from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange
from contacts.models import Contact
from companies.models import Company
from deals.models import PipelineStage

class DealForm(FlaskForm):
    name = StringField('Deal Name', validators=[DataRequired()])
    value = DecimalField('Value', validators=[Optional()])
    expected_close_date = DateField('Expected Close Date', format='%Y-%m-%d', validators=[Optional()])
    probability = IntegerField('Probability (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    pipeline_stage_id = SelectField('Pipeline Stage', coerce=int, validators=[DataRequired()])
    contact_id = SelectField('Associated Contact', coerce=int, validators=[Optional()])
    company_id = SelectField('Associated Company', coerce=int, validators=[Optional()])
    submit = SubmitField('Save Deal')

    def __init__(self, *args, **kwargs):
        super(DealForm, self).__init__(*args, **kwargs)
        self.pipeline_stage_id.choices = [(ps.id, ps.name) for ps in PipelineStage.query.order_by(PipelineStage.order).all()]
        self.contact_id.choices = [(0, '--- Select Contact ---')] + [(c.id, c.name) for c in Contact.query.order_by(Contact.name).all()] # Assuming contacts are global for now, or filter by current_user.id
        self.company_id.choices = [(0, '--- Select Company ---')] + [(c.id, c.name) for c in Company.query.order_by(Company.name).all()] # Same assumption
