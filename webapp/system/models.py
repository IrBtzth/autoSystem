from .. import db
from datetime import datetime

class Events(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    event = db.Column(db.String(255))
    module = db.Column(db.String(255))
    date = db.Column(db.DateTime())
    time = db.Column(db.Time())

    def __init__(self, event=""):
        self.event = event

    def __repr__(self):
        return "<Events '{}'>".format(self.event)

class Portf(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(255))
    began = db.Column(db.DateTime, default=datetime.utcnow)
    end = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return "<Name '{}'>".format(self.description)

class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    name = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    rol = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    portf = db.relationship('Portf', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name {}>'.format(self.name)