from flask import Flask, request, jsonify, Blueprint
from datetime import datetime, timedelta
import random
from .otp_handler import generate_otp, verify_otp, send_otp
from .models import OTP 
from app import db

bp = Blueprint('main', __name__)

#M pesa call back endpoint
@bp.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
	data = request.json()
	if not data:
		return jsonify({"error":"Invalid data"}), 400


	#extract payment details
	phone_number = data.get('phone_number')

	if not phone_number:
		return jsonify({"error": "Phone number is required"}), 400

	#Generate otp and store in the dp

		otp_code = generate_otp()
		otp = OTP(phone_number=phone_number, otp_code=otp_code)
		db.session.add(otp)
		db.session.commit()
		
		send_otp(phone_number, otp_code)

		return jsonify({"message": "OTP sent successfuly"}), 200

 #Route for OTP verification
@bp.route('/verify-otp', methods=['POST'])
def verify_otp_route():
 	data = request.json
 	phone_number = data.get('phone_number')
 	otp_code = data.get('otp_code')

 	if not phone_number or not otp_code:
 		return jsonify({"error": "phone_number and otp_code required"}), 400

 	otp = OTP.query.filter_by(phone_number=phone_number, otp_code=otp_code).first()

 	if not otp:
 		return jsonify({"error": "Invalid otp"}), 400

 	if otp.is_verified:
 		return jsonify({"error": "otp already used"}), 400

 	if otp.is_expired():
 		return jsonify({'error': 'otp has expired'}), 400

 	otp.is_verified = True
 	db.session.commit()

 	return jsonify({'message': 'otp successfuly verified'}), 200

