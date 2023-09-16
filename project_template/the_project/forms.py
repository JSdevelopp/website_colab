from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, validators
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from wtforms.validators import NumberRange, Email,Length

# Added Length, validators library from wtforms




class CheckoutForm(FlaskForm):
    # Added more payment type cards to fill dropbox
    choices_payment = [('Visa', 'Visa'), ('Mastercard', 'Mastercard'),('American Express', 'American Express'),('Discover', 'Discover')]
    month_choices = [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')]
    year_choices = [('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'), ('2031', '2031'), ('2032', '2032'), ('2033', '2033'), ('2034', '2034'), ('2035', '2035'), ('2036', '2036'), ('2037', '2037'), ('2038', '2038'), ('2039', '2039'), ('2040', '2040')]



    first_name = StringField('First: ', validators=[DataRequired()])
    last_name = StringField('Last: ', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address: ', validators=[DataRequired()])
    
    # Apartment field 
    apartment  = StringField('Apartment:', render_kw= {"maxlength": 10, "placeholder": "Apartment/Floor/Suite"})
    
    # City input based on additional fields
    city = StringField('City: ', validators=[DataRequired()])
    
    # US States - GPT automated 
    us_states = [
    ('', 'State *'),
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
    ('DC', 'Washington, D.C.')
]

    # State input field
    state = SelectField('State', choices=us_states, validators=[DataRequired()])
    
    # Zip code input field
    zip_code = StringField('Zip Code:', validators=[DataRequired()])
    
    # customer phone input field - Optional Field
    customer_phone = StringField('Phone Number:')
    
    # Card payments info are not required
    # Name on Card
    card_name = StringField('Name on Card:')
    
    payment_type = SelectField('Select a payment card type ', choices=choices_payment)
    card_number = StringField('Card Number')
    # card_exp_month = SelectField('Exp Month', choices = month_choices, validate_choice=[DataRequired()])
    # card_exp_year = SelectField('Exp Year', choices = year_choices, validate_choice=[DataRequired()])
    
    # Users wanting to manually enter the exp month and year
    card_expiry = StringField('Card Expiration (MM/YY)', [
        validators.Length(min=5, max=5),
        validators.Regexp(regex="^(0[1-9]|1[0-2])\/?([0-9]{2})$", message="Invalid date format.")
    ])
    
    # cvv = IntegerField('CVV', validators=[DataRequired(), NumberRange(min=100, max=999)])
    
    cvv = StringField('CVV', [
        validators.Length(min=3, max=3),
        validators.Regexp(regex="^[0-9]{3}$", message="Invalid CVV format.")
    ])
    submit = SubmitField('Place Order')


class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password:', validators=[DataRequired()])
    submit = SubmitField("Submit:")

    def check_email(self, field):
        if Registered_user.query.filter_by(email = field.data).first():
            raise ValidationError('Your email is already registered!')
        

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
        
    

    