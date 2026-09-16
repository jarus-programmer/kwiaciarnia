from crm_system import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name, surname, age, email, password):
        self.name = name
        self.surname = surname
        self.age = age
        self.email = email
        self.password = password