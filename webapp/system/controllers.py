from datetime import datetime
from sqlalchemy import desc, func
from flask import render_template, Blueprint, flash, redirect, url_for, current_app, abort, request
from flask_login import login_required, current_user
from .models import db, Portfs, Events, Customers, Cars, Departments, ProjectData
from ..auth.models import Users,Role
from ..auth import has_role
from werkzeug.security import generate_password_hash, check_password_hash
from ..searched.forms import SearchForm
from .forms import  PortForm, EventsForm, CustomerForm,CarsForm, DepartmentsForm, ProjectDataForm


system_blueprint = Blueprint(
    'system',
    __name__,
    template_folder='../templates'
)


@system_blueprint.route('/projectdata/projectdataDelete/<int:id>',methods=['GET', 'POST'])
def projectdataDelete(id):
    
    form= ProjectDataForm()
    projectdata_to_delete = ProjectData.query.get_or_404(id)
    
    try:
        db.session.delete(projectdata_to_delete)
        db.session.commit()
        flash("Project data deleted")
        
        our_projectdata=ProjectData.query.order_by(ProjectData.id)
        return redirect(url_for('system.projectdata'))
    except:
        flash('There was a problem deleting your event')
        return redirect(url_for('system.projectdata'))


@system_blueprint.route('/projectdata/projectdataAdd',methods=['POST', 'GET'])
def projectdataAdd():
    
    form=ProjectDataForm()
    carid= request.form.get('Cars')
    usersid= request.form.get('Operations Manager')
    deparmentsid= request.form.get('Departments')
    
    if form.validate_on_submit():

        
        
        car = Cars.query.get_or_404(int(carid))
        department = Departments.query.get_or_404(int(deparmentsid))
        user = Users.query.get_or_404(int(usersid))

        projectdata = ProjectData(amount=form.amount.data,observations=form.observations.data, solution=form.solution.data)
        
        car.projectdata.append(projectdata)
        department.projectdata.append(projectdata)
        user.projectdata.append(projectdata)
        
        db.session.add(projectdata)
        db.session.commit()
            
        form.amount.data = ''
        form.observations.data = ''
        form.solution.data = ''
        flash("Project Data added Successfully!")
        return redirect(url_for('system.projectdata')) 
    
    elif carid == None or usersid==None or deparmentsid==None :
        flash("We couldn't add your project data, be sure to add a car, an operation manager and a deparment")
        return redirect(url_for('system.projectdata'))
    
    else:
        flash("We couldn't add your project data, there was a problem")
        return redirect(url_for('system.projectdata'))
   
        

    return redirect(url_for('system.projectdata')) 



@system_blueprint.route('/projectdata/',methods=['GET', 'POST'])
def projectdata():

    form= ProjectDataForm()
    searchForm = SearchForm()

    our_projectdata= ProjectData.query.order_by(ProjectData.id)
    our_cars= Cars.query.order_by(Cars.id)
    our_users= [i for i in Users.query.order_by(Users.id) if str(i.roles)== '[Operations Manager]']
    flash(str(our_projectdata[0].cars.problem))
    our_departments= Departments.query.order_by(Departments.id)
    
    return render_template('system/projectdata.html',our_departments=our_departments,our_users=our_users, our_models=our_projectdata,our_cars=our_cars, form=form, SearchForm=searchForm)


#----------PROJECT DATA----------


@system_blueprint.route('/departments/departmentEdit/<int:id>', methods = ['GET', 'POST'])   
def departmentEdit(id):
    
    form=DepartmentsForm()

    if form.validate_on_submit():
        
        department= Departments.query.get_or_404(id)

        department.description = form.description.data 
        
            
        db.session.add(department)
        db.session.commit()
        
    return redirect(url_for('system.departments'))


@system_blueprint.route('/department/departmentDelete/<int:id>',methods=['GET', 'POST'])
def departmentDelete(id):
    
    form= DepartmentsForm()
    department_to_delete = Department.query.get_or_404(id)
    
    try:
        db.session.delete(department_to_delete)
        db.session.commit()
        flash("Department deleted")
        
        our_deparments=Deparments.query.order_by(Deparments.id)
        return redirect(url_for('system.deparments'))
    except:
        flash('There was a problem deleting your department')
        return redirect(url_for('system.department'))


@system_blueprint.route('/departments/departmentAdd',methods=['POST', 'GET'])
def departmentAdd():
    
    form=DepartmentsForm()
    
    if form.validate_on_submit():

        department = Departments.query.filter_by(description=form.description.data).first()
        if department is None:
            department = Departments(description=form.description.data)
            db.session.add(department)
            db.session.commit()
            
        form.description.data = ''
        flash("Department added Successfully!")
    return redirect(url_for('system.departments'))


@system_blueprint.route('/departments/',methods=['GET', 'POST'])
def departments():

    form=DepartmentsForm()
    searchForm = SearchForm()
    our_departments= Departments.query.order_by(Departments.id)
    
    return render_template('system/departments.html', our_models=our_departments, form=form, SearchForm=searchForm)


#----------DEPARMENTS----------


@system_blueprint.route('/cars/carsDelete/<int:id>',methods=['GET', 'POST'])
def carsDelete(id):
    
    form= CarsForm()
    car_to_delete = Cars.query.get_or_404(id)
    
    try:
        db.session.delete(car_to_delete)
        db.session.commit()
        flash("Car data Deleted")
        
        our_cars=Cars.query.order_by(Cars.id)
        return redirect(url_for('system.cars'))
    except:
        flash('There was a problem deleting your car data')
        return redirect(url_for('system.cars'))


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

        car = Cars.query.filter_by(carID=form.carID.data).first()
        if car is None:
        
            car = Cars( 
                carID=form.carID.data, plate=form.plate.data, brand = form.brand.data,
                model=form.model.data,year=form.year.data, serialBodywork=form.serialBodywork.data, 
                serialMotor=form.serialMotor.data, color=form.color.data,
                problem=form.problem.data
            )
            db.session.add(car)
            db.session.commit()

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
    searchForm=SearchForm()

    return render_template('system/cars.html',form=form, SearchForm=searchForm, our_models=our_cars)


#----------CARS----------


@system_blueprint.route('/customers/customersDelete/<int:id>',methods=['GET', 'POST'])
def customersDelete(id):
    
    form= CustomerForm()
    customers_to_delete = Customers.query.get_or_404(id)
    
    try:
        db.session.delete(customers_to_delete)
        db.session.commit()
        flash("Customer data Deleted")
        
        our_customers=Customers.query.order_by(Customers.id)
        return redirect(url_for('system.customers'))
    except:
        flash('There was a problem deleting your customers data')
        return redirect(url_for('system.customers'))


@system_blueprint.route('/customers/customersEdit/<int:id>', methods = ['GET', 'POST'])   
def customersEdit(id):
    
    form=CustomerForm()
    flash('editando')

    if form.validate_on_submit():

        customer= Customers.query.get_or_404(id)

        customer.name = form.name.data 
        customer.lastName = form.lastName.data 
        customer.dateBirth = form.dateBirth.data 
        customer.description = form.description.data 
        customer.email = form.email.data 
        customer.cellNumber = form.cellNumber.data  
        customer.customerID = form.customerID.data  

        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('system.customers'))


@system_blueprint.route('/customers/customerAdd',methods=['GET', 'POST'])
def customerAdd():
    
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


#----------CUSTOMERS----------


@system_blueprint.route('/events/eventDelete/<int:id>',methods=['GET', 'POST'])
def eventDelete(id):
    
    form= EventsForm()
    event_to_delete = Events.query.get_or_404(id)
    
    try:
        db.session.delete(event_to_delete)
        db.session.commit()
        flash("Event Deleted")
        
        our_events=Events.query.order_by(Events.id)
        return redirect(url_for('system.events'))
    except:
        flash('There was a problem deleting your event')
        return redirect(url_for('system.events'))


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


#----------EVENTS----------


@system_blueprint.route('/portfs/portfDelete/<int:id>',methods=['GET', 'POST'])
def portfDelete(id):
    
    form= PortForm()
    portf_to_delete = Portfs.query.get_or_404(id)
    
    try:
        db.session.delete(portf_to_delete)
        db.session.commit()
        flash("Portafolio Deleted")
        
        our_portfs=Portfs.query.order_by(Portfs.id)
        redirect(url_for('system.portfs'))
    except:
        flash('There was a problem deleting your user')
        redirect(url_for('system.portfs'))


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


@system_blueprint.route('/portfs/',methods=['GET', 'POST'])
@login_required
@has_role('Admin')
def portfs():
    form=PortForm()
    our_portfs= Portfs.query.order_by(Portfs.id) 
    searchForm=SearchForm() 
    
    return render_template('system/portfs.html', our_models=our_portfs, SearchForm=searchForm, form=form,datetime=datetime)


#----------PORTAFOLIOS----------

