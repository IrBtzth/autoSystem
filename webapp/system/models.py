from .. import db
from datetime import datetime
from ..auth.models import Users, Role
from ..auth import has_role

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

    def __repr__(self):
        return "<Name '{}'>".format(self.name)

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
    usersId = db.Column(db.Integer(), db.ForeignKey('users.id'))
    state= db.Column(db.Boolean(), unique=False, default=True)
    
    def __repr__(self):
        return "<Name '{}'>".format(self.description)