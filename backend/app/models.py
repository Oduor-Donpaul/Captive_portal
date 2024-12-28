from datetime import datetime, timedelta
from app import db
from flask_login import UserMixin


def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(20), nullable=False)
	role = db.Column(db.String(20), nullable=False, default='staff')

	def can_modify(self):
		return self.role == 'admin'

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.role}')"

class OTP(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	otp_code = db.Column(db.String(6), nullable=False)
	phone_number = db.Column(db.String(15), nullable=False)
	expires_at = db.Column(db.DateTime, nullable=False)
	is_verified = db.Column(db.Boolean, default=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	
	def __repr__(self):
		return f"<OTP {self.otp_code}>"


	def is_expired(self):
		
		return datetime.utcnow() > self.expires_at #returns whether otp has expired

#Model for storing devices
class Device(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	mac_address = db.Column(db.String(17), unique=True, nullable=False)
	ip_address = db.Column(db.String(15), nullable=False)
	access_granted_at = db.Column(db.DateTime, default=datetime.utcnow)
	
	def __repr__(self):
		return f"<Device {self.mac_address}>"
	
#Model for storing messages(OTP Notifications)
class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	otp = db.Column(db.String(10), nullable=False)
	phone_number = db.Column(db.String(15), nullable=[False])
	
