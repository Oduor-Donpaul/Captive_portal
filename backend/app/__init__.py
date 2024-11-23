from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from dotenv import load_dotenv
from app.init_utils import bcrypt, login_manager


#initialize database
db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app():
	#create a flask app instance
	app = Flask(__name__)

	#load confugaration settings
	app.config.from_object(Config)


	#Initialize extensions
	bcrypt.init_app(app)
	login_manager.init_app(app)
	db.init_app(app)
	migrate.init_app(app, db) #initialize migrate instance with app and db

	#register blueprints
	from .routes import bp
	app.register_blueprint(bp)
	
	#app.register_blueprint(main)

	return app
