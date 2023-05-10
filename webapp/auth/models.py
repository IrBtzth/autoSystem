from . import bcrypt, AnonymousUserMixin
from .. import db
from datetime import datetime
from ..system.models import Portfs, ProjectData

roles_users = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

portfs_users = db.Table(
    'portfs_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    
    db.Column('portfs_id', db.Integer, db.ForeignKey('portfs.id')))


class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    name = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))

    projectdata= db.relationship('ProjectData', backref='users')

    portfs = db.relationship('Portfs',
                                secondary=portfs_users, 
                                backref='portfs')

    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref='roles')
    

    def __repr__(self):
        return self.name

    def has_role(self, name):
        for role in self.roles:
            if role.name == name:
                return True
        return False

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False
    def get_id(self):
        return str(self.id)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return self.name

