from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, Optional, NumberRange, ValidationError


class AffairRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
    workload = IntegerField('Workload', validators=[DataRequired()])
    start_from = IntegerField('Startfrom', validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Submit')

    def validate_start_from(form, field):
        if field.data > form.workload.data:
            raise ValidationError('start_from must less than workload')
