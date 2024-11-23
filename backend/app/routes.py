from flask import Blueprint, request, jsonify
from .models import OTP, Message
from app import db
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from flask import Blueprint
from .models import User

bp = Blueprint("main", __name__)
auth_blueprint = Blueprint('auth', __name__)

#checks authorization
def is_authorized(roles):
    user = get_jwt_identity()
    return user['role'] in roles

#Endpoint for admin site view
@auth_blueprint.route('/admin/view', methods=['GET'])
@jwt_required()
def admin_view():
    if not is_authorized(['admin', 'staff']):
        return jsonify({'message': 'access denied'}), 403
    return jsonify({'info': 'admin site access'}), 200

#Endpoint for making modifications to the app, requires admin previlages
@auth_blueprint.route('/admin/modify', methods=['POST'])
@jwt_required()
def admin_modify():
    if not is_authorized(['admin']):
        return jsonify({'message': 'access denied'}), 403
    return jsonify({'message': 'Data modified successfully'}), 200

#Register endpoint
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    #Create a hashed password
    from app.init_utils import bcrypt
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        role=data.get('role', 'staff')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'user created successfully'}), 201

#Log in endpoint
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    #checks the password sent vs hashed password in the db
    from app.init_utils import bcrypt
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify({'access_token': access_token})
    return jsonify({'message': 'Invalid credentials'}), 401

#Route for mpesa callback to generate and send OTP
@bp.route('/mpesa-callback', methods=['POST'])
def mpesa_callback():
    data = request.json
    phone_number = data.get('PhoneNumber')

    if not phone_number:
        return jsonify({'Error': 'Phone number is required'})
    from app.utils.otp_handler import generate_otp
    otp_code = generate_otp()
    now = datetime.utcnow()
    expires_at = datetime(year=now.year, month=now.month, day=now.day) + timedelta(days=1)
    otp = OTP(phone_number=phone_number, otp_code=otp_code, expires_at=expires_at, is_verified=False)
    db.session.add(otp)
    db.session.commit()

    #Send otp via sms
    from app.utils.otp_handler import send_otp
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

    from app.utils.otp_handler import verify_otp
    if verify_otp(phone_number, otp):
        publish_otp(otp, phone_number)
        return jsonify({'message': 'OTP verified successfully'}), 200
    else:
        return jsonify({'error': 'Invalid OTP'}), 401
    
#Query notifications based on phone number
@bp.route('/api/notifications', methods=['GET'])
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
    
