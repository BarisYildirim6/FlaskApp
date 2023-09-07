from hashlib import sha256
from project import db

class User(db.Model):
	__tablename__ = 'User'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(128), unique=True, nullable=False)
	firstname = db.Column(db.String(128), unique=False, nullable=False)
	middlename = db.Column(db.String(128), unique=False, nullable=False)
	lastname = db.Column(db.String(128), unique=False, nullable=False)
	birthdate = db.Column(db.Date, nullable=False)
	email = db.Column(db.String(128), unique=True, nullable=False)
	password = db.Column(db.String(128), nullable=False)

	def __init__(self, username, firstname, middlename, lastname, email, birthdate, password):
		self.username = username
		self.firstname = firstname
		self.middlename = middlename
		self.lastname = lastname
		self.email = email
		self.birthdate = birthdate
		self.password = sha256(password.encode()).hexdigest()

class OnlineUsers(db.Model):
    __tablename__ = 'OnlineUsers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), db.ForeignKey("User.username"), nullable=False)
    ipaddress = db.Column(db.String(128), unique=True, nullable=False)
    logindatetime = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref='online_users')