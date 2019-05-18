import json
import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase


def add_user(username,email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user

class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        with self.client:
            response = self.client.post('/users',
            data = json.dumps(
                {
                'username': 'test',
                'email': 'test@test.com'
                }),
            content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,201)
            self.assertIn('test@test.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        with self.client:
            response = self.client.post('/users',
            data = json.dumps(
                {}),
            content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_key(self):
        with self.client:
            response = self.client.post('/users',
            data = json.dumps({'email': 'test@test.com'}),
            content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        with self.client:
            response = self.client.post('/users',
            data = json.dumps(
                {
                'username': 'test',
                'email': 'test@test.com'
                }),
            content_type = 'application/json'
            )
            response = self.client.post('/users',
            data = json.dumps(
                {
                'username': 'test',
                'email': 'test@test.com'
                }),
            content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,400)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])
    
    def test_get_single_user(self):
        user = add_user('test', 'test@test.com')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,200)
            self.assertIn('test', data['data']['username'])
            self.assertIn('test@test.com', data['data']['email'])
            self.assertIn('success', data['status'])
    
    def test_get_all_users(self):
        add_user('test0', 'test0@test.com')
        add_user('test1', 'test1@test.com')
        with self.client:
            response = self.client.get(f'/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('test0', data['data']['users'][0]['username'])
            self.assertIn('test0@test.com', data['data']['users'][0]['email'])
            self.assertIn('test1', data['data']['users'][1]['username'])
            self.assertIn('test1@test.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])


    def test_get_single_user_no_id(self):
        with self.client:
            response = self.client.get(f'/users/nonexistent')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,404)
            self.assertIn('User does not exits', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_single_user_invalid_id(self):
        with self.client:
            response = self.client.get(f'/users/-1')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,404)
            self.assertIn('User does not exits', data['message'])
            self.assertIn('fail', data['status'])



if __name__ == '__main__':
    unittest.main()