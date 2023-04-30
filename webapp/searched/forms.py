from flask_wtf import FlaskForm as Form
from flask_wtf import RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField
from wtforms.validators import DataRequired, Length, EqualTo, URL

class SearchForm(Form):
    
    bar_search = StringField('Searched:', validators=[DataRequired()])
    submit = SubmitField('Submit')