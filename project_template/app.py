from the_project import app, db

from flask import render_template, redirect, request, url_for, flash, abort, jsonify, session # Add jsonify import
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from the_project.models import logged_out_user, Registered_user, Pages_info, CartItem # Import Pages_info model
from the_project.forms import CheckoutForm, RegistrationForm, LoginForm
from sqlalchemy.exc import SQLAlchemyError
from the_project.models import Pages_info, logged_out_user
lower_limit = 0
upper_limit = 12
# # @app.route('/')
# def index():
#     sql_book = Pages_info.query.with_entities(Pages_info.book_url, Pages_info.star_url).all()
#     apple = logged_out_user.query.with_entities(logged_out_user.email).all()
#     return render_template('home.html', sql_book=sql_book, apple=apple)

@app.route('/')
def home():
    global lower_limit
    sql_book = Pages_info.query.all()

    cart_table = CartItem.query.all()
    # sql_book = Pages_info.query.with_entities(Pages_info.quantity_count).all()
    apple = logged_out_user.query.with_entities(logged_out_user.email).all()


    if 'cart' in session:
        cart_items = session.get('cart', [])
        return render_template('home.html', sql_book=sql_book, apple=apple, lower_limit = str(lower_limit), cart_items = cart_items)


    return render_template('home.html', sql_book=sql_book, apple=apple, lower_limit = str(lower_limit))
        


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
    
    if 'cart' in session:
        cart_items = session.get('cart', [])
        return render_template('checkout.html', form = form, cart_items = cart_items)

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
@login_required
def list_database():
    with db.engine.connect() as connection:
        books = connection.execute("SELECT * FROM books;")
        result = connection.execute("SELECT * FROM customer;")
        tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
        registerd_users = connection.execute("SELECT * FROM registered_users;")

        return render_template('show_table_items.html', books = books, result = result, tables = tables, registerd_users = registerd_users)


@app.route('/login', methods = ['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        #looks for this specific email in the database
        registered_user = Registered_user.query.filter_by(email = form.email.data).first()

        
        if registered_user is not None:
            if registered_user.check_password(form.password.data):
                print(registered_user)
                login_user(registered_user)
                flash('Logged In')

                next = request.args.get('next')
                
                if next == None or not next[0] == '/':
                    next = url_for('welcome_user')

                return redirect(next)
    return render_template('login.html', form = form)


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
        result = connection.execute("""SELECT * FROM customer WHERE email = :email;""", email=current_user.email)

        return render_template('/order_history.html', result = result)
    





@app.route('/api/books')
def get_books():
    upper_limit = 12
    lower_limit = 0
    try:
        # # Get the 'limit' and 'offset' query parameters from the request
        # limit = int(request.args.get('limit', upper_limit))  # Default to 12 if 'limit' is not provided
        # offset = int(request.args.get('offset', lower_limit))  # Default to 0 if 'offset' is not provided

        lower_limit = int(request.args.get('lower_limit', 0))  # Default lower limit to 0 if not provided
        upper_limit = int(request.args.get('upper_limit', 12))  # Default upper limit to 20 if not provided

        # Query the database to get book information within the specified range
        books = Pages_info.query.offset(lower_limit).limit(upper_limit - lower_limit)

        # # Query the database to get book information with the specified limit and offset
        # books = Pages_info.query.offset(offset).limit(limit).all()

        # Convert the list of book objects to a list of dictionaries
        book_data = []
        for book in books:
            book_data.append({
                'image': book.book_url,
                'title': book.text,
                'ratings': 5,  # You might want to modify this if you have book ratings in your database
                'price': f"${book.price_dollars}",
                'stock': book.quantity_count
            })

        return jsonify(book_data)
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/about_us')
def about_us_page():
    return render_template('about_us.html')


@app.route('/contact_us')
def contact_us_page():
    return render_template('contact_us.html')


@app.route('/update', methods=['POST'])
def update_count():
    global lower_limit  # Access the global variable
    lower_limit += 1
    return render_template ("home.html", lower_limit = str(lower_limit)) 


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    image = data.get('image')
    stock = data.get('stock')
    ratings = data.get('ratings')
    price = data.get('price')
    
    print(data)

    if image:
        if 'cart' not in session:
            session['cart'] = []

        book_details = {
            "image": image,
            "stock": stock,
            "ratings": ratings,
            "price": price
    
        }
        session['cart'].append(book_details)
        session.modified = True

        return jsonify({'message': 'Book added to cart', 'book': book_details})

    return jsonify({'message': 'No book ID provided'}), 400


# # To get all of the book data at once - Matt 9/15/2023
# @app.route('/api/books')
# def get_books():
#     # Query the database to get book information
#     books = Pages_info.query.all()

#     # Convert the list of book objects to a list of dictionaries
#     book_data = []
#     for book in books:
#         book_data.append({
#             'image': book.book_url,
#             'title': book.text,
#             'ratings': 5,  # You might want to modify this if you have book ratings in your database
#             'price': f"${book.price_dollars}",
#             'stock': book.quantity_count
#         })

#     return jsonify(book_data)



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




