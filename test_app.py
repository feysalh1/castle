
import unittest
from main import app
from db import db
from models import Parent, Child

class TestChildrensCastle(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_parent_registration(self):
        response = self.client.post('/parent/register', data={
            'username': 'testparent',
            'email': 'test@example.com',
            'password': 'test1234',
            'confirm_password': 'test1234',
            'first_name': 'Test',
            'last_name': 'Parent'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration

if __name__ == '__main__':
    unittest.main()
