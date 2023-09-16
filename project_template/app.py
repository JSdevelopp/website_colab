from the_project import app, db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from the_project.models import logged_out_user, Registered_user
from the_project.forms import CheckoutForm, RegistrationForm, LoginForm
from sqlalchemy.exc import SQLAlchemyError
from the_project.models import Pages_info, logged_out_user

@app.route('/')
def home():
    sql_book = Pages_info.query.all()
    # sql_book = Pages_info.query.with_entities(Pages_info.quantity_count).all()
    apple = logged_out_user.query.with_entities(logged_out_user.email).all()
    return render_template('home.html', sql_book=sql_book, apple=apple)
        


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():

    form = CheckoutForm()

    if form.validate_on_submit():


        # Change this to user data object and create the user class instance into a separate line
        # Added address, apartment, city, state, zip code, phone inputs
        user_data = {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "email": form.email.data,
            "address": form.address.data,
            "apartment": form.apartment.data if form.apartment.data else None, # Check if provided
            "city": form.city.data,
            "state": form.state.data,
            "zip_code": form.zip_code.data,
            "phone": form.customer_phone.data if form.customer_phone.data else None,  # Check if provided
            
        }
        
        # User class instance
        user = logged_out_user(user_data)

        with app.app_context():

            db.session.add(user)
            db.session.commit()

        return redirect(url_for('thank_you'))
    return render_template('checkout.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = Registered_user(first_name=form.first_name.data,
                               last_name=form.last_name.data,
                               email=form.email.data,
                               password=form.password.data)
        try:
            with app.app_context():
                db.session.add(user)
                db.session.commit()
                print('User added successfully')
                return redirect(url_for('thank_you'))
        except SQLAlchemyError as e:

            db.session.rollback()  # Rollback the session to prevent partial data insert
            print('Error adding user to the database:', str(e))
            print('User details:', user.first_name,
                  user.last_name, user.email, user.password_hash)
            print('User not added')

        return redirect(url_for('thank_you'))
    return render_template('register.html', form=form)


@app.route('/show_table_items')
@login_required
def list_database():
    with db.engine.connect() as connection:
        books = connection.execute("SELECT * FROM books;")
        result = connection.execute("SELECT * FROM customer;")
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")
        registerd_users = connection.execute("SELECT * FROM registered_users;")

        return render_template('show_table_items.html', books=books, result=result, tables=tables, registerd_users=registerd_users)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        # looks for this specific email in the database
        registered_user = Registered_user.query.filter_by(
            email=form.email.data).first()

        if registered_user is not None:
            if registered_user.check_password(form.password.data):
                print(registered_user)
                login_user(registered_user)
                flash('Logged In')

                next = request.args.get('next')

                if next == None or not next[0] == '/':
                    next = url_for('welcome_user')

                return redirect(next)
    return render_template('login.html', form=form)



@app.route('/logged_in')
@login_required
def welcome_user():
    return render_template('welcome.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/order_history')
@login_required
def orders():
    with db.engine.connect() as connection:
        result = connection.execute(
            """SELECT * FROM customer WHERE email = :email;""", email=current_user.email)

        return render_template('/order_history.html', result=result)


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
