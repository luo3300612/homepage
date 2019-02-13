from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, Optional


class AffairRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
    workload = StringField('Workload', validators=[DataRequired(), Regexp('^[0-9]*$', 0, 'Must be a number')])
    start_from = StringField('Startfrom', validators=[Optional(), Regexp('^[0-9]*$', 0, 'Must be a number')])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Submit')