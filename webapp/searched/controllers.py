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
        current_page=request.form['page']

        models={1:Customers,2:Events,3:Cars,4:Portfs}
        pages={1:'system.customers',2:'system.events',3:'system.cars',4:'system.portfs'}

        for key_model in models:
            model = models[key_model]

            for key_page in pages:
                page=pages[key_page]

                if (len(str(searched))> 1) and (current_page==page) and (key_model == key_page): 
            
                    
                    attrs= dir(model.query.first())          
                    attrs_filtered = list(filter(lambda x: x.find('_')<0 and not(any([x in ['registry','query','metadata']])), attrs))

                    model_attrs = [[model.query.filter(getattr(model, i).like('%' +searched+'%' )),getattr(model(),i)]
                                    for i in attrs_filtered 
                                    if model.query.filter(getattr(model, i).like('%' + searched +'%' )).first() != None]
                    
                    len_model_attrs=[len(i[0].all()) for i in model_attrs]
                    max_index=len_model_attrs.index(max(len_model_attrs))

                    models_filtered = model_attrs[max_index][0].order_by(model_attrs[max_index][1])


                    
                    return render_template(
                                                'Search.html',
                                                form=form,
                                                models_filtered=models_filtered,
                                                attrs_filtered =attrs_filtered,
                                                getattr=getattr
                                          )
                
            


        
            

        
    return 'hola' +str(customers) 