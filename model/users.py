from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Post(db.Model):
    __tablename__ = 'posts'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, note, image):
        self.userID = id
        self.note = note
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": str(file_encode)
        }


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL

class Transactions(db.Model):
    _tablename_ = 'transactions'
   
    # define the stock schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _symbol = db.Column(db.String(255),unique=False,nullable=False)
    _transaction_type = db.Column(db.String(255),unique=False,nullable=False)
    _quantity = db.Column(db.String(255),unique=False,nullable=False)
    _transaction_amount = db.Column(db.Integer, nullable=False)
    _transaction_date = db.Column(db.Date)
    # constructor of a User object, initializes the instance variables within object (self)

    def _init_(self,uid,symbol,transaction_type,quantity,transaction_amount,transaction_date):
        self._uid = uid
        self._symbol = symbol
        self._transaction_type = transaction_type
        self._quantity = quantity
        self._transaction_amount = transaction_amount
        self._transaction_date = transaction_date
    
    # uid
    @property
    def uid(self):
        return self._uid
    
    @uid.setter
    def uid(self,uid):
        self._uid = uid
        
    # symbol
    @property
    def symbol(self):
        return self._symbol
    
    @symbol.setter
    def symbol(self,symbol):
        self._symbol = symbol
        
    # transaction type
    @property
    def transaction_type(self):
        return self._transaction_type
    
    @transaction_type.setter
    def transaction_type(self,transaction_type):
        self._transaction_type = transaction_type
        
    #quantity
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self,quantity):
        self._quantity = quantity
        
    #transaction amount
    @property
    def transaction_amount(self):
        return self._transaction_amount
    
    @transaction_amount.setter
    def transaction_amount(self,transaction_amount):
        self._transaction_amount = transaction_amount
        
    # transaction
    @property
    def transaction_date(self):
        transaction_date_string = self._transaction_date.strftime('%m-%d-%Y')
        return transaction_date_string
    
    # dob should be have verification for type date
    @transaction_date.setter
    def dob(self, transaction_date):
        self._transaction_date = transaction_date
        
     # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())
    
    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
        
    
    # CRUD update: updates user name, password, phone
    # returns self

    def update(self,uid="",symbol="",transaction_type="",quantity="",transaction_amount=""):
        """only updates values with length"""
        if len(uid) > 0:
            self.uid = uid
        if len(symbol) > 0:
            self.symbol = symbol
        if len(transaction_type) > 0:
            self.transaction_type = transaction_type
        if len(quantity) > 0:
            self.quantity = quantity
        if len(transaction_amount) > 0:
            self.transaction_amount = transaction_amount           
        db.session.commit()
        return self
    
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "transaction_type": self.transaction_type,
            "quantity": self.quantity,
            "transaction_amount": self.transaction_amount,
            "transaction_date": self.transaction_date
        }

    

    
    
class Stocks(db.Model):
    _tablename_ = 'stocks'
    
    # define the stock schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _symbol = db.Column(db.String(255),unique=False,nullable=False)
    _company = db.Column(db.String(255),unique=False,nullable=False)
    _quantity = db.Column(db.Integer,unique=False,nullable=False)
    _sheesh = db.Column(db.Integer,unique=False,nullable=False)
    
    # constructor of a User object, initializes the instance variables within object (self)
    def _init_(self,symbol,company,quantity,sheesh):
        self._symbol = symbol
        self._company = company
        self._quantity = quantity
        self._sheesh = sheesh
# symbol
    @property
    def symbol(self):
        return self._symbol
    
    @symbol.setter
    def symbol(self,symbol):
        self._symbol = symbol
#company
    @property
    def company(self):
        return self._company
    
    @company.setter
    def company(self,company):
        self._company = company
#quantity
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self,quantity):
        self._quantity = quantity

#cost
    @property
    def sheesh(self):
        return self._sheesh
    
    @sheesh.setter
    def sheesh(self,sheesh):
        self._sheesh = sheesh
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())
    
    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
        
     # CRUD update: updates user name, password, phone
    # returns self
    def update(self,symbol="",company="",quantity=None):
        """only updates values with length"""
        if len(symbol) > 0:
            self.symbol = symbol
        #if sheesh > 0:
           # self.sheesh = sheesh
        if len(company) > 0:
            self.company = company
        if quantity is not None:
            self.quantity = quantity
        
        db.session.commit()
        return self
    
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "company": self.company,
            "quantity": self.quantity,
            "sheesh": self.sheesh,
        }
    # Builds working data for testing
    def initUsers():
        with app.app_context():
            """Create database and tables"""
            db.create_all()

        

class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.Date)
    _pnum = db.Column(db.String(255), unique=False, nullable=True)
    _email = db.Column(db.String(255), unique=True, nullable=True)
    _role = db.Column(db.String(255), unique=False, nullable=True)
    _stockmoney = db.Column(db.Integer, unique=False, nullable=False)
    
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, pnum, email, role, stockmoney, password="123qwerty", dob=date.today()):
        self._name = name
        self._uid = uid
        self._stockmoney = stockmoney
        self.set_password(password)
        self._dob = dob
        self._pnum = pnum
        self._email = email
        self.role = role

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
        
    @property
    def stockmoney(self):
        return self._stockmoney
    
    # a setter function, allows name to be updated after initial object creation
    @stockmoney.setter
    def stockmoney(self, stockmoney):
        self._stockmoney = stockmoney
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # update password, this is conventional setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, "pbkdf2:sha256", salt_length=10)

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        dob_string = self._dob.strftime('%m-%d-%Y')
        return dob_string
    
    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    
    @property
    def age(self):
        today = date.today()
        return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))

    @property
    def pnum(self):
        return self._pnum
    
    @pnum.setter
    def pnum(self, pnum):
        self._pnum = pnum

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        self._email = email

    @property
    def role(self):
        return self._role
    
    @role.setter
    def role(self, role):
        self._role = role
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "dob": self.dob,
            "age": self.age,
            "stockmoney": self.stockmoney,
            "pnum": self.pnum,
            "email": self.email,
            "role": self.role,
            "posts": [post.read() for post in self.posts]
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", stockmoney= None, password="", pnum="", email="", role=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        if len(pnum) > 0:
            self.pnum = pnum
        if len(email) > 0:
            self.email = email
        if len(role) > 0:
            self.role = role
        if stockmoney is None:
            self.stockmoney = stockmoney
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()

            