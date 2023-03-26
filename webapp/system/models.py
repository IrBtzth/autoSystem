from .. import db
from datetime import datetime
from ..auth.models import Users, Role
from ..auth import has_role

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
    
    def __repr__(self):
        return "<Name '{}'>".format(self.description)