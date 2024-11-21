import unittest
from flask import json
from app import create_app, db


class TestMessageRoute(unittest.TestCase):
        
    def setUp(self):
        """
            Setup function for tests. creates a test app and a database
        """
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Clean up function for tests. Remove the db and app context
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_all_messages(self):
        """
            Test fetching all messages
        """
        response = self.client.get('api/notifications')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['notifications']), 1)