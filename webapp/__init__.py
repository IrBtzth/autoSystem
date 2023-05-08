from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy import MetaData


migrate = Migrate()

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))



def page_not_found(error):
    return render_template('404.html'), 404

def create_app(object_name):
    
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

   

  
    from .system import create_module as system_create_module
    from .auth import create_module as auth_create_module
    from .searched import create_module as searched_create_module
    from .main import create_module as main_create_module
    auth_create_module(app)
    system_create_module(app)
    searched_create_module(app)
    main_create_module(app)

    return app