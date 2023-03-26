from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine

db = SQLAlchemy()
migrate = Migrate()



def page_not_found(error):
    return render_template('404.html'), 404

def create_app(object_name):
    
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    migrate.init_app(app, db,render_as_batch=True)

  
    from .system import create_module as system_create_module
    from .auth import create_module as auth_create_module
    from .main import create_module as main_create_module
    auth_create_module(app)
    system_create_module(app)
    main_create_module(app)

    return app