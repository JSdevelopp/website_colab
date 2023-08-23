from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from wtforms.validators import NumberRange, Email





class CheckoutForm(FlaskForm):

    choices_payment = [('visa', 'visa'), ('mastercard', 'mastercard')]
    month_choices = [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')]
    year_choices = [('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'), ('2031', '2031'), ('2032', '2032'), ('2033', '2033'), ('2034', '2034'), ('2035', '2035'), ('2036', '2036'), ('2037', '2037'), ('2038', '2038'), ('2039', '2039'), ('2040', '2040')]



    first_name = StringField('First: ', validators=[DataRequired()])
    last_name = StringField('Last: ', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address: ', validators=[DataRequired()])
    payment_type = SelectField('Select an option', choices=choices_payment)
    card_number = StringField('Card Number', validators=[DataRequired()])
    card_exp_month = SelectField('Exp Month', choices = month_choices, validate_choice=[DataRequired()])
    card_exp_year = SelectField('Exp Year', choices = year_choices, validate_choice=[DataRequired()])
    cvv = IntegerField('CVV', validators=[DataRequired(), NumberRange(min=100, max=999)])
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
        
    

    