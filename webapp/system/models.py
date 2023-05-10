from .. import db
from datetime import datetime
from ..auth import has_role

class ProjectData(db.Model):
    
    id = db.Column(db.Integer(), primary_key=True)

    departments_id= db.Column(db.Integer(), db.ForeignKey('departments.id'))
    
    users_id= db.Column(db.Integer(), db.ForeignKey('users.id'))
    
    cars_id= db.Column(db.Integer(), db.ForeignKey('cars.id'))

    amount = db.Column(db.String(255))

    observations = db.Column(db.String(255))

    solution = db.Column(db.String(255))


    def __repr__(self):
        return self.department_project

class Departments(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(), nullable=False)

    projectdata = db.relationship('ProjectData', backref='departments')

    

    def __repr__(self):
        return self.description

class Cars(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    carID = db.Column(db.String(255))
    plate = db.Column(db.String(255))
    brand= db.Column(db.String(255))
    model = db.Column(db.String(255))
    year = db.Column(db.DateTime)
    serialBodywork = db.Column(db.String(255))
    serialMotor = db.Column(db.String(255))
    color = db.Column(db.String(255))
    problem = db.Column(db.String(255))

    projectdata= db.relationship('ProjectData', backref='cars')
    

    def __repr__(self):
        return self.plate

class Customers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    dateBirth= db.Column(db.DateTime)
    description = db.Column(db.String(255))
    email = db.Column(db.String(255))
    cellNumber = db.Column(db.String(255))
    customerID = db.Column(db.String(255))

    def __repr__(self):
        return "<Name '{}'>".format(self.name)

class Events(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    event = db.Column(db.String(255))
    module = db.Column(db.String(255))
    date = db.Column(db.DateTime())
    hour = db.Column(db.Time())

    def __repr__(self):
        return "<Events '{}'>".format(self.event)

class Portfs(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(), nullable=False)
    portfStart = db.Column(db.DateTime())
    portFinish = db.Column(db.DateTime())
    state= db.Column(db.Boolean(), unique=False, default=True)
    
    def __repr__(self):
        return self.description

