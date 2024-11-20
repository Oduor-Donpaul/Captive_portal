from datetime import datetime, timedelta
from app import db

class OTP(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	otp_code = db.Column(db.String(6), nullable=False)
	phone_number = db.Column(db.String(15), nullable=False)
	expires_at = db.Column(db.DateTime, nullable=False)
	is_verified = db.Column(db.Boolean, default=False)
	
	def __repr__(self):
		return f"<OTP {self.otp_code}>"


	def is_expired(self):
		
		return datetime.utcnow() > self.expires_at #returns whether otp has expired

class Device(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	mac_address = db.Column(db.String(17), unique=True, nullable=False)
	ip_address = db.Column(db.String(15), nullable=False)
	access_granted_at = db.Column(db.DateTime, default=datetime.utcnow)
	
	def __repr__(self):
		return f"<Device {self.mac_address}>"