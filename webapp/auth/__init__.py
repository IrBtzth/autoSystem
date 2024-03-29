import functools
from flask import flash, redirect, url_for, session, abort
from flask_login import current_user
from flask_login import LoginManager, login_user
from flask_bcrypt import Bcrypt
from flask_login import AnonymousUserMixin

class SystemAnonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"
login_manager.anonymous_user = SystemAnonymous

def create_module(app, **kwargs):
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .controllers import auth_blueprint
    app.register_blueprint(auth_blueprint)


def has_role(name):
    def real_decorator(f):
        def wraps(*args, **kwargs):
            if current_user.has_role(name):
                return f(*args, **kwargs)
            else:
                abort(403)
        return functools.update_wrapper(wraps, f)
    return real_decorator


@login_manager.user_loader
def load_user(userid):
    from .models import Users
    return Users.query.get(userid)


def create_or_login(resp):
    from .models import db, Users
    username = resp.fullname or resp.nickname or resp.email
    if not username:
        flash('Invalid login. Please try again.', 'danger')
        return redirect(url_for('auth.login'))
    user = Users.query.filter_by(username=username).first()
    if user is None:
        user = Users(username)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('main.index'))