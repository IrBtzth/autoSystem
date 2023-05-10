from flask import (render_template,
                   Blueprint,
                   redirect,
                   url_for,
                   flash)
from .models import db, Users,Role
from .forms import LoginForm, UsersForm,UsersEditForm
from flask_login import login_user, logout_user,LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..searched.forms import SearchForm
from . import has_role
from ..system.models import Portfs

auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='../templates/auth',
    url_prefix="/auth"
)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login Succesfull!')
                
                return redirect(url_for('system.portfs'))
            else:
                flash('Wrong Password - Try Again!')
        else:
            flash('That user doesnt exist!')
            
    return render_template('login.html', form=form)


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	
    logout_user()
    flash("You Have Been Logged Out!  Thanks For Stopping By...")
    
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/userDelete/<int:id>',methods=['GET', 'POST'])
def userDelete(id):
    
    form= formChoices()
    user_to_delete = Users.query.get_or_404(id)
    
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted")
        
        our_users=Users.query.order_by(Users.id)
        return render_template("users.html", form=form,our_models=our_users)
    except:
        flash('There was a problem deleting your user')
        return render_template("users.html", form=form,our_models=our_users)

@auth_blueprint.route('/addUser/userEdit/<int:id>', methods = ['GET', 'POST'])   
def userEdit(id):
    
    form=formChoices()

    if form.validate_on_submit():
        
        theUser= Users.query.get_or_404(id)
        value=int(form.role_button.data)
        role= Role.query.get_or_404(value)

        theUser.name = form.name.data 
        theUser.username = form.username.data   
        hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
        theUser.password_hash = hashed_pw
       
        old_role = Role.query.get(int(theUser.roles.__getitem__(0).id))
        
        theUser.roles.append(role)
        theUser.roles.remove(old_role)
            
        db.session.add(theUser)
        db.session.commit()
        
    return redirect(url_for('auth.users'))
    
    
 
    
@auth_blueprint.route('/userAdd',methods=['GET', 'POST'])
def userAdd():
    
    form = formChoices()
    
    
    if form.validate_on_submit():
        
        value = int(form.role_button.data)
        portfs = form.role_button2.data
        role = Role.query.get_or_404(value)
        

        user = Users.query.filter_by(username=form.username.data).first()
        if user is None:
            
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
            user = Users(username=form.username.data, name=form.name.data, lastName=form.lastName.data, password_hash=hashed_pw)
            
            user.roles.append(role)
            for portf in portfs:
                user.portfs.append(portf)
            
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        form.username.data = ''
        form.name.data = ''
        form.lastName.data = ''
        form.password_hash.data = ''
        flash("User Added Successfully!")


    return redirect(url_for('auth.users'))
    

@auth_blueprint.route('/users',methods=['GET', 'POST'])

def users():

    form = formChoices()
    our_users= Users.query.order_by(Users.id) 
    searchForm=SearchForm() 
    
    return render_template('users.html',form=form,SearchForm=searchForm,our_models=our_users)
    
def formChoices():
    form = UsersForm()
    model_to_choice= [Role, Portfs]
    choices=[]

    for i in  model_to_choice:
        len_choices = range(len(i.query.all()))
        if i==Role:
            choices.append([((j+1,str(i.query.all()[j].name))) for j in len_choices])
            form.role_button.choices=choices[0]
        else:
            form.role_button2.query=i.query.all()



    return form
