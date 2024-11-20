import os
from dotenv import load_dotenv

#Load environment varibles from .env file
load_dotenv()

class Config:
	SECRET_KEY = os.getenv('SECRET_KEY')

	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

	SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

	SQLALCHEMY_TRACK_MODIFICATIONS = False
