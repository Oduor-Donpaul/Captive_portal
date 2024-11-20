
import json
import pika.exceptions
from app import create_app
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from kombu import Connection, Exchange, Queue

app = create_app()
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000"], async_mode='eventlet', logger=True, engineio_logger=True)

@socketio.on('connect')
def handle_connect():
    print("Client connected")


#channel.queue_declare(queue='notifications_queue')

#Publish notification to the queu
def publish_otp(otp, phone_number):
    message = json.dumps({'otp': otp, 'phone_number': phone_number})
    with Connection('amqp://guest:guest@localhost//') as conn:
        #channel = conn.channel()
        queue = Queue('notifications_queue', exchange=Exchange(''), routing_key='notifications_queue')
        queue.maybe_bind(conn)
        queue.declare()

        producer = conn.Producer()
        print(f"Attempting to publish message: {message}")
        producer.publish(message, routing_key='notifications_queue', declare=[queue])
        print(f"Message: {message} published")

#Deserialize the message to obj:
def otp_notification_callback(body, message):
    notification = json.loads(body)
    otp = notification.get('otp')
    phone_number = notification.get('phone_number')

    print(f"Recieved OTP: {otp} for phone number {phone_number}")

    #Send OTP data to frontend
    socketio.emit('otp_notification', {'otp': otp, 'phone_number': phone_number})
    message.ack()

#Start rabbit mq consumer
def start_consumer():
    with Connection('amqp://guest:guest@localhost//') as conn:
        queue = Queue('notifications_queue', exchange=Exchange(''), routing_key='notifications_queue')
        queue.maybe_bind(conn)
        queue.declare()

        #Consume messages
        with conn.Consumer(queues=[queue], callbacks=[otp_notification_callback]) as consumer:
            print("Waiting for OTP notifications...")
            while True:
                try:
                    while True:
                        conn.drain_events(timeout=1)
                except TimeoutError:
                    print("No messages recieved, waiting for messages..")
