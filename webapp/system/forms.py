from flask_wtf import FlaskForm
from wtforms import TimeField, DateField,StringField,EmailField, SelectField, SubmitField,IntegerField, PasswordField, BooleanField, ValidationError,TextAreaField, FormField,FieldList
from wtforms.validators import DataRequired, EqualTo, Length,Regexp
from datetime import datetime

class ProjectDataForm(FlaskForm):
    car = StringField(label= 'Amount:', validators=[DataRequired()])

    amount = StringField(label= 'Amount:', validators=[DataRequired()])
    observations = StringField(label= 'Observations:', validators=[DataRequired()])
    solution = StringField(label= 'Solution:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DepartmentsForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CarsForm(FlaskForm):

    carID = StringField('ID:', validators=[DataRequired()])
    plate = StringField('Plate:', validators=[DataRequired()])
    brand = StringField('Brand:', validators=[DataRequired()])
    model = StringField('Model:', validators=[DataRequired()])
    year= DateField('Year:',format='%Y-%m-%d', validators=[DataRequired()])
    serialBodywork = StringField('Serial Bodywork:', validators=[DataRequired()])
    serialMotor = StringField('Serial Motor:', validators=[DataRequired()]) 
    color = StringField('Color:', validators=[DataRequired()])
    problem = StringField('Problem:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CustomerForm(FlaskForm):

    name = StringField('Name:', validators=[DataRequired()])
    lastName = StringField('Last Name:', validators=[DataRequired()])
    dateBirth = DateField('Date of Birth',format='%Y-%m-%d', validators=[DataRequired()])
    email = EmailField('Email address', validators=[DataRequired()])
    cellNumber = StringField('Phone Number:', validators=[DataRequired()]) 
    customerID = StringField('Customer ID', 
        validators =[Regexp('^[VE]-\d{8}$', message="The ID must contain only letters 'V' or 'E' numbers or underscore"), 
        Length(min=6, max=10, message="Numbre must at least 6 numbers ")])
    description = StringField('description', validators=[DataRequired()])
    submit = SubmitField('Submit')

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
    





