from datetime import datetime
from sqlalchemy import desc, func
from flask import render_template, Blueprint, flash, redirect, url_for, current_app, abort, jsonify,request
from flask_login import login_required, current_user
from ..system.models import db, Portfs, Events, Customers, Cars,Departments, ProjectData
from ..auth.models import Users,Role
from ..auth import has_role
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import SearchForm
from ..system.forms import  PortForm, EventsForm, CustomerForm,CarsForm,ProjectDataForm
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

@searched_blueprint.route('/search/<adress>',methods=['GET', 'POST'])
def search(adress): 
    
    form = SearchForm()
        

    if form.validate_on_submit() or True:
        
        searched = form.bar_search.data
        current_page=str(adress)

        

        models={1:Customers,2:Events,3:Cars,4:Portfs,5:Departments, 6:Users, 7:ProjectData}
        pages={1:'system.customers',2:'system.events',3:'system.cars',4:'system.portfs',5:'system.departments',6:'auth.users',7:'system.projectdata'}

        for key_model in models:
            model = models[key_model]

            for key_page in pages:
                page=pages[key_page]

                if (len(str(searched))> 1) and (current_page==page) and (key_model == key_page) and searched != None: 
                   
                    attrs= dir(model.query.first())          
                    

                    
                    if page == 'auth.users':
                        attrs_filtered = list(filter(lambda x: x.find('_')<0 and not(any([x in ['registry','query','metadata','roles']])), attrs))
                        
                        model_attrs = [[model.query.filter(getattr(model, i).like('%' +searched+'%' )),getattr(model, i)]
                                        for i in attrs_filtered 
                                        if model.query.filter(getattr(model, i).like('%' + searched +'%' )).first() != None]                  
                    else:
                        attrs_filtered = list(filter(lambda x: x.find('_')<0 and not(any([x in ['registry','query','metadata']])), attrs))
                        model_attrs = [[model.query.filter(getattr(model, i).like('%' +searched+'%' )),getattr(model, i)]
                                        for i in attrs_filtered 
                                        if model.query.filter(getattr(model, i).like('%' + searched +'%' )).first() != None]
                    
                    
                    len_model_attrs=[len(i[0].all()) for i in model_attrs]
                    max_index=len_model_attrs.index(max(len_model_attrs))

                    the_attr= model_attrs[max_index][1]
                   
                    
                    models_filtered = model_attrs[max_index][0].order_by(the_attr)
                    
                     
                    return render_template('Search.html', our_models=models_filtered,page=page)
                    
                
                elif searched == None and (current_page==page) and (key_model == key_page):

                    attrs= dir(model.query.first())          
                    attrs_filtered = list(filter(lambda x: x.find('_')<0 and not(any([x in ['registry','query','metadata']])), attrs))

                    all_models = model.query.all()
                    all_category=[]
                    for model in all_models:
                        for attr in attrs_filtered:
                            all_category.append(str(getattr(model, attr)))



                    return jsonify(all_category)

   

