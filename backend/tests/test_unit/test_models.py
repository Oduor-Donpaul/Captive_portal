import unittest
from app import create_app, db
from app.models import *

class TestMessageModel(unittest.TestCase):
    def setUp(self):
        """
            SetUp function. Creates a test app and a test database
        """
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
            CleanUp function for tests, Removes the database and app context
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_message_creation(self):
        """
            Test fetching all messages from the API
        """
        message = Message(phone_number='1234567890', otp='123456')
        db.session.add(message)
        db.session.commit()
        self.assertEqual(Message.query.count(), 1)