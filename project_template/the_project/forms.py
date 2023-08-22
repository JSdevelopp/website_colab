from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

class CheckoutForm(FlaskForm):

    choices = [('visa', 'visa'), ('mastercard', 'mastercard')]


    first_name = StringField('First: ', validators=[DataRequired()])
    last_name = StringField('Last: ', validators=[DataRequired()])
    address = StringField('Address: ', validators=[DataRequired()])
    payment_type = SelectField('Select an option', choices=choices)
    submit = SubmitField('Place Order')