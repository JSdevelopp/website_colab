from myproject import app, db
from myproject.__init__ import db, login_manager
from flask import render_template, redirect, request, url_for, flash, abort

from flask_login import login_user, login_required, logout_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
@login_manager.user_loader
def home():
    return render_template('home.html')

##name of the page as usual but the second line sends this function through
##a funciton that requires the user to be logged in to view the page
@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    
    form  = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully')

            #flask saves the request in next
            #so we are grabbing the request from next
            next = request.args.get('next')


            # if next exists or is not equal to /
            if next == None or not next[0] =='/':
                next = url_for('welcome_user')
            #redirects the user to the page/s they are allowed to visit after
            #they have logged in
            return redirect(next)
        
    #if the user fails to loging correctly they are rerouted to the home page
    return render_template('login.html', form = form)

## get and post tells the method it is allowed to retrieve and post data
## to and from the server
@app.route('/register', methods = ['GET', 'POST'])
def register():
    ##takes the registration form from myproject.forms method
    form = RegistrationForm()


    #checks to see if the form has been submitted and the submitted data 
    #passes the validation rules defined in the forms fild's
    if form.validate_on_submit():
      
        user = User(email=form.email.data,
                    username=form.username.data, 
                    password=form.password.data)
        
        #adding a record to the SQLAlchemy database
        #and commiting the information
        with app.app_context():
            db.metadata.create_all(bind=db.engine, tables=[User.__table__])
            
            db.session.add(user)
            

            session_objects = db.session.new   # New objects added to the session
            print("Objects in session: sakura", session_objects)
            print("Username:", user.username)
            print("Email:", user.email)
            db.session.commit()


        #flashes a message to the screen for the user to see
        flash('Thanks for registration!')
        #name of the html file
        return redirect(url_for('login'))
    
    return render_template('register.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)
        
