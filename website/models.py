from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import datetime


class Note(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    text=db.Column(db.String(10000))
    date= db.Column(db.DateTime(timezone=True), default=func.now())
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):        
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    select_field = db.Column(db.String(50))
    telephone = db.Column(db.String(20))
    birthplace = db.Column(db.String(50))
    birthdate = db.Column(db.Date)
    nationality = db.Column(db.String(50))
    address = db.Column(db.String(100))
    cin = db.Column(db.String(10))
    username = db.Column(db.String(50), unique=True, nullable=False)
    notes=db.relationship('Note')

    def to_dict(self):        
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}

    def __init__(self, email, password, first_name, last_name, select_field, telephone, birthplace, birthdate, nationality, address, cin, username, password2):
        self.email = email
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.select_field = select_field
        self.telephone = telephone
        self.birthplace = birthplace
        bd = [int(x) for x in str(birthdate).split("/")]
        self.birthdate = datetime.date(bd[2], bd[1], bd[0])
        self.nationality = nationality
        self.address = address
        self.cin = cin
        self.username = username
        self.password2 = generate_password_hash(password2)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    

class Candidate(db.Model):
    app_candidates = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    select_course = db.Column(db.String(100))
    telephone = db.Column(db.String(50))
    birthdate = db.Column(db.String(50))
    birthplace = db.Column(db.String(50))
    nationality = db.Column(db.String(50))
    cin_passport = db.Column(db.String(50))
    gradelevel = db.Column(db.String(50))
    address = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, firstname, lastname, select_course, telephone, birthdate, birthplace, nationality, cin_passport, gradelevel, address, email):
        self.firstname = firstname
        self.lastname = lastname
        self.select_course = select_course
        self.telephone = telephone
        self.birthdate = birthdate
        self.birthplace = birthplace
        self.nationality = nationality
        self.cin_passport = cin_passport
        self.gradelevel = gradelevel
        self.address = address
        self.email = email

    def to_dict(self):        
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}


class Instructor(db.Model):
    app_instructors= 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    firstname1 = db.Column(db.String(50))
    lastname1 = db.Column(db.String(50))
    select_payment = db.Column(db.String(100))
    telephone1 = db.Column(db.String(50))
    birthdate1 = db.Column(db.String(50))
    birthplace1 = db.Column(db.String(50))
    nationality1 = db.Column(db.String(50))
    cin_passport1 = db.Column(db.String(50))
    course = db.Column(db.String(50))
    address = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, firstname1, lastname1, select_payment, telephone1, birthdate1, birthplace1, nationality1, cin_passport1, course, address, email):
        self.firstname1 = firstname1
        self.lastname1 = lastname1
        self.select_payment = select_payment
        self.telephone1 = telephone1
        self.birthdate1 = birthdate1
        self.birthplace1 = birthplace1
        self.nationality1 = nationality1
        self.cin_passport1 = cin_passport1
        self.course = course
        self.address = address
        self.email = email

    def to_dict(self):        
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}


class Course(db.Model):
    app_course = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    length = db.Column(db.String(50))

    def to_dict(self):        
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}

    def __init__(self, name, length):
        self.name = name
        self.length = length
class expense(db.Model):
    app_expense = 'expense'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    type = db.Column(db.String(50))
    category = db.Column(db.String(50))

    def to_dict(self):        
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}

    def __init__(self, amount, type,category):
        self.amount = amount
        self.type = type
        self.category= category












