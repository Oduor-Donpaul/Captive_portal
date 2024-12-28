import random
import string
from datetime import datetime, timedelta
from app.models import OTP
from app import db

#Generate random six digit OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

#Check if OTP is expired
def is_otp_expired(otp):
    otp_instance = OTP.query.filter_by(otp_code=otp).first()
    if otp_instance and otp_instance.is_expired():
        return True
    return False

#Send OTP
def send_otp(phone_number, otp):
    print(f"Sending {otp} to {phone_number}")

#Verify OTP
def verify_otp(phone_number, otp):
    otp_instance = OTP.query.filter_by(phone_number=phone_number, otp_code=otp).first()
    if otp_instance and not otp_instance.is_verified and not otp_instance.is_expired():
        otp_instance.is_verified = True
        db.session.commit()
        return True
    return False

#Check if otp is verified
def otp_verification_status(phone_number, otp):
    otp_instance = OTP.query.filter_by(phone_number=phone_number, otp_code=otp).first()

    if otp_instance and otp_instance.is_verified and not otp_instance.is_expired():
        return True
    return False

