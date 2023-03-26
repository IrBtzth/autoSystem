from flask_wtf import FlaskForm as Form
from flask_wtf import RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField
from wtforms.validators import DataRequired, Length, EqualTo, URL
from .models import Role



class UsersEditForm(Form):
    
    username = StringField('Username:', validators=[DataRequired()])
    name = StringField('Name:', validators=[DataRequired()])
    lastName = StringField('Last Name:', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password must be the same')])
    password_hash2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')
    role = StringField('Role:', validators=[DataRequired()])

class LoginForm(Form):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])

    
class UsersForm(Form):
    
    username = StringField('Username:', validators=[DataRequired()])
    name = StringField('Name:', validators=[DataRequired()])
    lastName = StringField('Last Name:', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password must be the same')])
    password_hash2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')
    role_button = SelectField(label= 'Role:', choices=[], validators=[DataRequired()])