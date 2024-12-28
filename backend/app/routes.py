from flask import Blueprint, request, jsonify, Response
from .models import OTP, Message
from app import db
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from flask import Blueprint
from .models import User
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import traceback
from flask_cors import cross_origin

load_dotenv()
bp = Blueprint("main", __name__)
auth_blueprint = Blueprint('auth', __name__)

RADIUS_SERVER=os.getenv("RADIUS_SERVER")
RADIUS_SECRET=b"the-first"
RADIUS_PORT=os.getenv("RADIUS_PORT")


#checks authorization
def is_authorized(roles):
    user = get_jwt_identity()
    return user['role'] in roles

#Role required decorator, sets the role required for the action
def role_required(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not create_user.is_authenticated:
                return jsonify({'message': "Unauthorized"}), 401
            if create_user.role not in role:
                return jsonify({"message": "Forbidden: Insufficient permission"}),403
            return func(*args, **kwargs)
        return wrapper
    return decorator


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

#Endpoint for creating users 
@auth_blueprint.route('/create_user', methods=['POST'])
@role_required(["admin"])
@jwt_required()
def create_user():
    data = request.json
    if not data:
        return jsonify({'message': 'Invalid data'})
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'staff')

    if role not in ['admin', 'staff']:
        return jsonify({'message': 'Invalid role'})
    user = User(username=username, email=email, role=role)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": f"User {username} with rolr {role} created"}), 201

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


#Log in endpoint for admin site
@auth_blueprint.route('/admin/login', methods=['POST'])
@cross_origin(origin='http://localhost:3000')
def admin_login():

    data = request.get_json()
    print(data)

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=data['email']).first()

    #checks the password sent vs hashed password in the db
    from app.init_utils import bcrypt
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify({'access_token': access_token})
    print('Invalid credentials')
    return jsonify({'message': 'Invalid credentials'}), 401

#Route for retrieving OTP
@bp.route('/admin/get-otp', methods=['POST'])
def get_otp():
    data = request.json
    phone_number = data.get('PhoneNumber')

    if not phone_number:
        return jsonify({'message': 'phone number is required'}), 400
    
    otp = OTP.query.filter_by(phone_number=phone_number).order_by(OTP.created_at.desc()).first()
    
    if not otp:
        return jsonify({'message': 'No OTP found for this phone number'}), 404
    
    return jsonify({"otp": otp.otp_code, "created_at": otp.created_at}), 200


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
#Log in endpoint for guests/network access
@auth_blueprint.route('/login', methods=['POST'])
def verify_otp_endpoint():
    data = request.json
    phone_number = data.get('phone_number')
    otp = data.get('otp_code')

    from app.utils.queue_handler import publish_otp

    if not phone_number or not otp:
        return jsonify({'Error': 'Phone number and OTP are required'}), 400

    from app.utils.otp_handler import verify_otp
    if verify_otp(phone_number, otp):
        access_token = create_access_token(
            identity=phone_number,
            expires_delta=timedelta(hours=1)
        )

        publish_otp(otp, phone_number)
        return jsonify({
        'message': 'OTP verified successfully',
        'access_token': access_token
       }), 200
    return jsonify({'error': 'Invalid OTP'}), 401

#athenticate free radius request  
@bp.route('/api/auth/authenticate', methods=['POST']) 
def freeradius_authenticate():
    data = request.get_json()

    print(f"Data: {data}")

    phone_number = data['phone_number']
    otp = data['otp_code']

    from app.utils.otp_handler import otp_verification_status

    if otp_verification_status(phone_number, otp):
        authenticated = "ok"
        return jsonify({'authenticated': authenticated})
    return Response(
        "Authentication Not Allowed",
        status=400,
    )

    
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
    
