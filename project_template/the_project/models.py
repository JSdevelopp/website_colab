from the_project import db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash




class logged_out_user(db.Model, UserMixin):
  
    __tablename__ = 'customer'
    
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64), index = True)
    address = db.Column(db.String(64))

    def __init__(self, email, first_name, last_name, address):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.address = address


class Registered_user(db.Model, UserMixin):
    __tablename__ = 'registered_users'

  


    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(64), index = True)
    last_name = db.Column(db.String(64), index = True)
    email = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128), unique = True, index = True)

    def __init__(self,first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        print(password)
        self.password_hash = generate_password_hash(str(password), method='scrypt')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
