from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from the_project import app, db
from the_project.forms import CheckoutForm






@app.route('/')
def home():
    return render_template('home.html')


@app.route('/checkout', methods =['GET', 'POST'])
def checkout():

    form = CheckoutForm()

    return render_template('checkout.html', form = form)


@app.route('/Thank_you')
def thank_you():
    return render_template('Thank_you.html')


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
    app.run(debug=True)




