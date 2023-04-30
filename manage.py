import os
from webapp import db, migrate, create_app
from webapp.system.models import Users, Portfs, Events
env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())
#app.app_context().push()

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Users=Users, Portfs=Portfs, Events=Events,
                    migrate=migrate)

'''
from manage import app,db
from webapp.system.models import Users, Portfs, Events,Customers,Cars
from webapp.auth.models import Users, Role
app.app_context().push()
from datetime import datetime
our_users= Users.query.order_by(Users.id).get_or_404()
our_roles= Role.query.order_by(Role.id)
'''