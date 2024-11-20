import eventlet
eventlet.monkey_patch()

from app import create_app
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from app.utils.queue_handler import socketio, start_consumer, app
import threading

#Run the consumer in separate thread to avoid blocking the event loop
def start_rabbitmq_consumer_thread():
	eventlet.spawn(start_consumer)


if __name__ == '__main__':

	start_rabbitmq_consumer_thread()
	#run the app in debug mode
	socketio.run(app, debug=True)