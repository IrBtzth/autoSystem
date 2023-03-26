from flask_wtf import FlaskForm
from wtforms import TimeField, DateField,StringField, SubmitField, PasswordField, BooleanField, ValidationError,TextAreaField, FormField,FieldList
from wtforms.validators import DataRequired, EqualTo, Length
from datetime import datetime

class EventsForm(FlaskForm):
    event = StringField('Event', validators=[DataRequired()])
    module = StringField('Module', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    hour = TimeField('Hour', format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PortForm(FlaskForm):

    description = StringField('Description', validators=[DataRequired()])
    portfStart = DateField('Start', format='%Y-%m-%d', validators=[DataRequired()])
    portFinish = DateField('Finish',format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')
    





