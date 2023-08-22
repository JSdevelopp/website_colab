from the_project import db
from flask_login import UserMixin


class logged_out_user(db.Model, UserMixin):
    __tablename__ = 'customer'
    
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(64),  unique = True, index = True)
    last_name = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(64), unique = True, index = True)
    address = db.Column(db.String(64), unique = True, index = True)

    def __init__(self, email, first_name, last_name, address):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.address = address


