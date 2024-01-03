from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class DateForm(FlaskForm):
    year = StringField('year', validators=[DataRequired()])
    month = StringField('month', validators=[DataRequired()])