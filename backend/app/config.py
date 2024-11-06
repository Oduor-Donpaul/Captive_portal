import os
from dotenv import load_dotenv

#Load environment varibles from .env file


class Config:
	SECRET_KEY = os.getenv('SECRET_KEY')

	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

	SQLALCHEMY_TRACK_MODIFICATIONS = False
