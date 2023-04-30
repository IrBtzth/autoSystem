from datetime import datetime
from sqlalchemy import desc, func
from flask import render_template, Blueprint, flash, redirect, url_for, current_app, abort, request
from flask_login import login_required, current_user
from .models import db, Portfs, Events, Customers, Cars
from ..auth.models import Users,Role
from ..auth import has_role
from werkzeug.security import generate_password_hash, check_password_hash
from ..searched.forms import SearchForm
from .forms import  PortForm, EventsForm, CustomerForm,CarsForm


system_blueprint = Blueprint(
    'system',
    __name__,
    template_folder='../templates'
)

@system_blueprint.route('/cars/carsDelete/<int:id>',methods=['GET', 'POST'])
def carsDelete(id):
    
    form= CarsForm()
    car_to_delete = Cars.query.get_or_404(id)
    
    try:
        db.session.delete(car_to_delete)
        db.session.commit()
        flash("Car data Deleted")
        
        our_cars=Cars.query.order_by(Cars.id)
        return render_template("cars.html", form=form,our_cars=our_cars)
    except:
        flash('There was a problem deleting your car data')
        return render_template("system/cars.html", form=form,our_cars=our_cars)


@system_blueprint.route('/cars/carsEdit/<int:id>', methods = ['GET', 'POST'])   
def carsEdit(id):
    
    form=CarsForm()

    if form.validate_on_submit():
        
        car= Cars.query.get_or_404(id)

        car.carID = form.carID.data 
        car.plate = form.plate.data 
        car.brand = form.brand.data 
        car.model = form.model.data 
        car.year = form.year.data 
        car.serialBodywork = form.serialBodywork.data 
        car.serialMotor = form.serialMotor.data 
        car.color = form.color.data 
        car.problem = form.problem.data 
            
        db.session.add(car)
        db.session.commit()
        
    return redirect(url_for('system.cars'))


@system_blueprint.route('/cars/addCars',methods=['GET', 'POST'])
def addCars():
    
    form = CarsForm()
    
    
    if form.validate_on_submit():

        car = Cars.query.filter_by(username=form.name.data).first()
        if car is None:
        
            car = Cars( 
                carID=form.carID.data, plate=form.plate.data, brand = form.brand.data,
                model=form.model.data,year=form.year.data, serialBodywork=form.serialBodywork.data, 
                serialMotor=form.serialMotor.data, color=form.color.data,
                problem=form.problem.data
            )
            db.session.add(car)
            db.session.commit()

        form.name.data = ''
        form.carID.data = ''
        form.plate.data = ''
        form.brand.data = ''
        form.model.data = ''
        form.year.data = ''
        form.serialBodywork.data = ''
        form.serialMotor.data = ''
        form.color.data = ''
        form.problem.data = ''


        flash("Data car Added Successfully!")

    our_cars = Cars.query.order_by(Cars.id)
    return redirect(url_for('system.cars')) 
    

@system_blueprint.route('/cars/',methods=['GET', 'POST'])
def cars():
    form=CarsForm()
    our_cars = Cars.query.order_by(Cars.id)    

    return render_template('system/cars.html',form=form,our_cars=our_cars)

@system_blueprint.route('/customers/customersDelete/<int:id>',methods=['GET', 'POST'])
def customersDelete(id):
    
    form= CustomersForm()
    customers_to_delete = Customers.query.get_or_404(id)
    
    try:
        db.session.delete(customers_to_delete)
        db.session.commit()
        flash("Customer data Deleted")
        
        our_customers=Customers.query.order_by(Customers.id)
        return render_template("customers.html", form=form,our_customers=our_customers)
    except:
        flash('There was a problem deleting your customers data')
        return render_template("system/customers.html", form=form,our_models=our_customers)

@system_blueprint.route('/customers/customersEdit/<int:id>', methods = ['GET', 'POST'])   
def customersEdit(id):
    
    form=CustomerForm()

    if form.validate_on_submit():

        customer= Customers.query.get_or_404(id)

        customer.name = form.name.data 
        customer.lastName = form.lastName.data 
        customer.dateBirth = form.dateBirth.data 
        customer.description = form.description.data 
        customer.email = form.email.data 
        customer.cellNumber = form.cellNumber.data  
        customer.customerID = form.customerID.data  
       
        db.session.commit()
        return redirect(url_for('system.customers'))

@system_blueprint.route('/customers/addCustomer',methods=['GET', 'POST'])
def addCustomer():
    
    form = CustomerForm()
    
    
    if form.validate_on_submit():

        customer = Customers.query.filter_by(name=form.name.data).first()
        if customer is None:
        
            customer = Customers( 
                name=form.name.data, lastName=form.lastName.data, dateBirth = form.dateBirth.data,
                description=form.description.data,email=form.email.data, cellNumber=form.cellNumber.data,
                customerID=form.customerID.data
            )
            db.session.add(customer)
            db.session.commit()

        form.name.data = ''
        form.lastName.data = ''
        form.dateBirth.data = ''
        form.description.data = ''
        form.email.data = ''
        form.cellNumber.data = ''
        form.customerID.data = ''


        flash("Customer Added Successfully!")

    our_customers = Customers.query.order_by(Customers.id)

    return redirect(url_for('system.customers'))

@system_blueprint.route('/customers/',methods=['GET', 'POST'])
def customers():

    form=CustomerForm()
    searchForm=SearchForm()
    our_customers= Customers.query.order_by(Customers.id)
    
    return render_template('system/customers.html', our_models=our_customers,SearchForm=searchForm, form=form,datetime=datetime)



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
    searchForm = SearchForm()
    our_events= Events.query.order_by(Events.id)
    
    return render_template('system/events.html', our_models=our_events, form=form, SearchForm=searchForm ,datetime=datetime)


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
    searchForm=SearchForm() 
    
    return render_template('system/portfs.html', our_portfs=our_portfs, SearchForm=searchForm, form=form,datetime=datetime)

@system_blueprint.route('/portfs/portfRunButton/<int:id>', methods = ['GET', 'POST'])   
def portfRunButton(id):
    
    portf= Portfs.query.get_or_404(id)
    if portf.state== False:
        portf.state = True
    else:
        portf.state = False
    db.session.add(portf)
    db.session.commit()

    
    return redirect(url_for('system.portfs'))


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


