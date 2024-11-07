from datetime import datetime, timedelta
from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	phone_number = db.Column(db.String(15),unique=True, nullable=False)
	mac_address = db.Column(db.String(17), unique=True, nullable=False)
	#One to many relationship with OTPs
	otp = db.relationship('OTP', backref='user', lazy=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<User {self.phone_number}>"

class OTP(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	phone_number = db.Column(db.String(15), nullable=False)
	otp_code = db.Column(db.String(6), nullable=False)
	expirstion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow()+
		timedelta(minutes=10))

	is_verified = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return f"<OTP {self.otp_code}>"


	def is_expired(self):
		
		return datetime.utcnow() > self.expires_at #returns whether otp has expired

class Device(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	mac_address = db.Column(db.String(17), unique=True, nullable=False)
	ip_address = db.Column(db.String(15), nullable=False)
	access_granted_at = db.Column(db.DateTime, default=datetime.utcnow())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	user = db.relationship('User', backref=db.backref('devices', lazy = True))

	def __repr__(self):
		return f"<Device {self.mac_address}>"