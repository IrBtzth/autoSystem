from flask_wtf import FlaskForm as Form
from flask_wtf import RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField, widgets
from wtforms.validators import DataRequired, Length, EqualTo, URL
from .models import Role, Portfs
from  wtforms_alchemy import QuerySelectMultipleField


class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

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
    role_button = SelectField(label= 'Role:', validators=[DataRequired()])
    role_button2 = QuerySelectMultipleFieldWithCheckboxes(label= 'Project:', validators=[DataRequired()])