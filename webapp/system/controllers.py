from datetime import datetime
from sqlalchemy import desc, func
from flask import render_template, Blueprint, flash, redirect, url_for, current_app, abort, request
from flask_login import login_required, current_user
from .models import db, Portfs, Events
from ..auth.models import Users,Role
from ..auth import has_role
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import  PortForm, EventsForm


system_blueprint = Blueprint(
    'system',
    __name__,
    template_folder='../templates'
)


@system_blueprint.route('/events/eventDelete/<int:id>',methods=['GET', 'POST'])
def eventDelete(id):
    
    form= EventsForm()
    event_to_delete = Events.query.get_or_404(id)
    
    try:
        db.session.delete(event_to_delete)
        db.session.commit()
        flash("Event Deleted")
        
        our_events=Events.query.order_by(Events.id)
        return render_template("events.html", form=form,our_events=our_events)
    except:
        flash('There was a problem deleting your event')
        return render_template("system/events.html", form=form,our_events=our_events)


@system_blueprint.route('/events/eventAdd',methods=['POST', 'GET'])
def eventAdd():
    
    form=EventsForm()
    
    if form.validate_on_submit():

        event = Events.query.filter_by(module=form.module.data).first()
        if event is None:
            event = Events(event=form.event.data,module=form.module.data, date=form.date.data, 
            hour =form.hour.data)
            db.session.add(event)
            db.session.commit()
            
        module = form.module.data
        form.module.data = ''
        form.date.data = ''
        form.hour.data = ''
        flash("Event added Successfully!")
    return redirect(url_for('system.events')) 


@system_blueprint.route('/events/',methods=['GET', 'POST'])
def events():

    form=EventsForm()
    our_events= Events.query.order_by(Events.id)
    
    return render_template('system/events.html', our_events=our_events, form=form,datetime=datetime)


@system_blueprint.route('/portfs/portfDelete/<int:id>',methods=['GET', 'POST'])
def portfDelete(id):
    
    form= PortForm()
    portf_to_delete = Portfs.query.get_or_404(id)
    
    try:
        db.session.delete(portf_to_delete)
        db.session.commit()
        flash("Portafolio Deleted")
        
        our_portfs=Portfs.query.order_by(Portfs.id)
        return render_template("portfs.html", form=form,our_portfs=our_portfs)
    except:
        flash('There was a problem deleting your user')
        return render_template("system/portfs.html", form=form,our_portfs=our_portfs)


@system_blueprint.route('/portfs/',methods=['GET', 'POST'])
@login_required
@has_role('Admin')
def portfs():
    form=PortForm()
    our_portfs= Portfs.query.order_by(Portfs.id)
    
    
    return render_template('system/portfs.html', our_portfs=our_portfs, form=form,datetime=datetime)

@system_blueprint.route('/portfs/portfAdd',methods=['POST', 'GET'])
def portfAdd():
    
    form=PortForm()
    description=None
    
    if form.validate_on_submit():

        portf = Portfs.query.filter_by(description=form.description.data).first()
        if portf is None:
            portf = Portfs(description=form.description.data, portfStart=form.portfStart.data, 
            portFinish =form.portFinish.data)
            db.session.add(portf)
            db.session.commit()
            
        description = form.description.data
        form.description.data = ''
        form.portfStart.data = ''
        form.portFinish.data = ''
        flash("Portafolio Added Successfully!")
    return redirect(url_for('system.portfs'))      


@system_blueprint.route('/portfs/portfEdit/<int:id>', methods = ['GET', 'POST'])   
def portfEdit(id):
    
    form=PortForm()

    if form.validate_on_submit():

        portf= Portfs.query.get_or_404(id)
        portf.description = form.description.data 
        portf.portfStart = form.portfStart.data  
        portf.portFinish = form.portFinish.data  
       
        db.session.commit()
        return redirect(url_for('system.portfs'))


