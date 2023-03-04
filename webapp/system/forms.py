from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError,TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

class EventsForm(FlaskForm):
    event = StringField('Event', validators=[DataRequired()])
    module = StringField('Module', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    hour = StringField('Hour', validators=[DataRequired()])

class PortfForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    began = StringField('Began', validators=[DataRequired()])
    end = StringField('Last Name', validators=[DataRequired()])

class UsersForm(FlaskForm):
    
    username = StringField('Username:', validators=[DataRequired()])
    name = StringField('Name:', validators=[DataRequired()])
    lastName = StringField('Last Name:', validators=[DataRequired()])
    rol = StringField('Rol:', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password must be the same')])
    password_hash2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')



