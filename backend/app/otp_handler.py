import random
import string
from datetime import datetime, timedelta
from app.models import OTP 
from app import db


def generate_otp(length=6):
	otp_code = ''.join(random.choices(string.digits, k=length))
	return otp_code

otp_data = {} #Temporaru Otp storage


#Send OTP
def send_otp(phone_number, otp_code):

	#SMS integration place_holder
	print(f"Sending OTO {otp_code} to phone_number {phone_number}")
	pass

#Funtion for verifying otp
def verify_otp(phone_number, otp_code):
	otp = OTP.query.filter_by(phone_number=phone_number, otp_code=otp_code).first()
	if otp and not otp.is_verified and not otp.is_expired():
		otp.is_verified = True
		db.session.commit()
		return True
	return False