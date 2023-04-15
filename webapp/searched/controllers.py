from datetime import datetime
from sqlalchemy import desc, func
from flask import render_template, Blueprint, flash, redirect, url_for, current_app, abort, request
from flask_login import login_required, current_user
from ..system.models import db, Portfs, Events, Customers, Cars
from ..auth.models import Users,Role
from ..auth import has_role
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import SearchForm
from ..system.forms import  PortForm, EventsForm, CustomerForm,CarsForm
from sqlalchemy import or_

searched_blueprint = Blueprint(
    'searched',
    __name__,
    template_folder='../templates'
)




@searched_blueprint.context_processor
def base():
    form=SearchForm()
    return dict(form=form)


@searched_blueprint.route('/search',methods=['GET', 'POST'])
def search(): 

    
    customers = Customers.query
    cars = Cars.query

    form = SearchForm()

    if form.validate_on_submit():

        searched = form.searched.data
        page=request.form['page']
 
        if len(str(searched))> 1 and page=='system.addCustomer': 
      
            
            attrs= dir(Customers.query.first())          
            attrs_filtered = list(filter(lambda x: x.find('_')<0 and not(any([x in ['registry','query','metadata']])), attrs))

            customers_attrs = [[Customers.query.filter(getattr(Customers, i).like('%' +searched+'%' )),getattr(Customers,i)] for i in attrs_filtered if Customers.query.filter(getattr(Customers, i).like('%' + searched +'%' )).first() != None]
            
            len_customers_attrs=[len(i[0].all()) for i in customers_attrs]
            max_index=len_customers_attrs.index(max(len_customers_attrs))

            customers = customers_attrs[max_index][0].order_by(customers_attrs[max_index][1])
            return render_template(
                                        'Search.html',
                                        form=form,
                                        search=customers
                                    )
        else:
                return 'puta'
        

        
          
        #events = Events.query.filter(Events.name.like('%' +searched +'%' )).all()
        #cars = Cars.query.filter(Cars.brand.like('%' +searched +'%' )).all()
        return 'heles' +str(str(page=='system.addCustomer'))
        
            

        
    return 'hola' +str(customers) 