import datetime
from sqlalchemy import desc, func
from flask import render_template, Blueprint, flash, redirect, url_for, current_app, abort
from flask_login import login_required, current_user
from .models import db, Users, Portf, Events
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import UsersForm, PortfForm, EventsForm

system_blueprint = Blueprint(
    'system',
    __name__,
    template_folder='../templates'
)


@system_blueprint.route('/add_user',methods=['GET', 'POST'])
def add_users():
    
    name = None
    form = UsersForm()
    
    if form.validate_on_submit():

        user = Users.query.filter_by(username=form.username.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
            user = Users(username=form.username.data, name=form.name.data, lastName=form.lastName.data, rol=form.rol.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        form.username.data = ''
        form.name.data = ''
        form.lastName.data = ''
        form.rol.data = ''
        form.password_hash.data = ''
        flash("User Added Successfully!")
    
    our_users = Users.query.order_by(Users.date_added)
    return render_template(
        'add_users.html',
        form=form,
        name=name,
        our_users=our_users
    )

@system_blueprint.route('/portf',methods=['GET', 'POST'])
def portf():
    
    description = None
    form = PortfForm()
    
    if form.validate_on_submit():

        portf = Portf.query.filter_by(description=form.description.data).first()
        if portf is None:

            portf = Portf(description=form.description.data, began=form.began.data, end=form.end.data)
            db.session.add(portf)
            db.session.commit()

        description = form.description.data
        form.description.data = ''
        form.began.data = ''
        form.end.data = ''
        flash("User Added Successfully!")
    
    our_portf = Portf.query.order_by(Portf.began)
    return render_template(
        'portf.html',
        form=form,
        description=description,
        our_portf=our_portf
    )


