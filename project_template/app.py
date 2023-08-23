from the_project import app, db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from the_project.models import logged_out_user, Registered_user
from the_project.forms import CheckoutForm, RegistrationForm
from sqlalchemy.exc import SQLAlchemyError


@app.route('/')
def home():

    return render_template('home.html')


@app.route('/checkout', methods =['GET', 'POST'])
def checkout():

    form = CheckoutForm()

    if form.validate_on_submit():
        
        user = logged_out_user(first_name = form.first_name.data,
                               last_name = form.last_name.data,
                               email =  form.email.data,
                               address = form.address.data
                               )
        
        with app.app_context():

            db.session.add(user)
            db.session.commit()
            
        return redirect(url_for('thank_you'))


    return render_template('checkout.html', form = form)






@app.route('/register', methods =['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = Registered_user(first_name = form.first_name.data,
                                          last_name = form.last_name.data,
                                          email = form.email.data,
                                          password = form.password.data)
        try:
            with app.app_context():
                db.session.add(user)
                db.session.commit()
                print('User added successfully')
                return redirect(url_for('thank_you'))
        except SQLAlchemyError as e:
            
            db.session.rollback()  # Rollback the session to prevent partial data insert
            print('Error adding user to the database:', str(e))
            print('User details:', user.first_name, user.last_name, user.email, user.password_hash)
            print('User not added')

        return redirect(url_for('thank_you'))


    return render_template('register.html', form = form)




@app.route('/show_table_items')
def list_database():
    with db.engine.connect() as connection:
        result = connection.execute("SELECT * FROM customer;")
        tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
        registerd_users = connection.execute("SELECT * FROM registered_users;")


        return render_template('show_table_items.html', result = result, tables = tables, registerd_users = registerd_users)




@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/travel')
# def travel():
#     return render_template('travel.html')


# @app.route('/Mystery')
# def mystery():
#     return render_template('mystery.html')


# @app.route('/Historical_fiction')
# def Historical_fiction():
#     return render_template('Historical_fiction.html')

# @app.route('/Sequential_Art')
# def mystSequential_Artery():
#     return render_template('Sequential_Art.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)




