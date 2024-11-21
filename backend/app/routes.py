from flask import Blueprint, request, jsonify
from app.utils.otp_handler import generate_otp, verify_otp, send_otp
from .models import OTP, Message
from app import db
from datetime import datetime, timedelta
from app import create_app
from flask import Blueprint

bp = Blueprint("main", __name__)

#Route for mpesa callback to generate and send OTP
@bp.route('/mpesa-callback', methods=['POST'])
def mpesa_callback():
    data = request.json
    phone_number = data.get('PhoneNumber')

    if not phone_number:
        return jsonify({'Error': 'Phone number is required'})
    otp_code = generate_otp()
    now = datetime.utcnow()
    expires_at = datetime(year=now.year, month=now.month, day=now.day) + timedelta(days=1)
    otp = OTP(phone_number=phone_number, otp_code=otp_code, expires_at=expires_at, is_verified=False)
    db.session.add(otp)
    db.session.commit()

    #Send otp via sms
    send_otp(phone_number, otp_code)

    return jsonify({'message': 'OTP sent successfully'}), 200

#Verify OTP
@bp.route('/verify-otp', methods=['POST'])
def verify_otp_endpoint():
    data = request.json
    phone_number = data.get('phone_number')
    otp = data.get('otp_code')

    from app.utils.queue_handler import publish_otp

    if not phone_number or not otp:
        return jsonify({'Error': 'Phone number and OTP are required'}), 400

    if verify_otp(phone_number, otp):
        publish_otp(otp, phone_number)
        return jsonify({'message': 'OTP verified successfully'}), 200
    else:
        return jsonify({'error': 'Invalid OTP'}), 401
    
#Query notifications based on phone number
@bp.route('/notifications', methods=['GET'])
def single_notifications_endpoint():

    phone_number = request.args.get('phone_number')

    if not phone_number:
        return jsonify({'Error': 'Phone number required'})
    
    try:
        messages = Message.query.filter_by(phone_number=phone_number).all()

        notifications = []
        
        for message in messages:
            notifications.append({
                'id': message.id,
                'otp': message.otp,
                'phone_number': message.phone_number
            })
        
        return jsonify({'notifications': notifications})
    except Exception as e:
        return jsonify({'error': f"error fetching notifications: {str(e)}"}), 500
    
#Query all notifications enspoint
@bp.route('/notifications/all', methods=['GET'])
def get_all_notifications():
    
    try:
        messages = Message.query.all()

        notifications = []

        for message in messages:
            notifications.append({
                'id': message.id,
                'otp': message.otp,
                'phone_number':message.phone_number
            })
        
        return jsonify({'notifications': notifications}, 200)
    except Exception as e:
        return jsonify({'error': f'Error fetching all messages {str(e)}'}), 500
    
