#!/usr/bin/env python

from app import app
import unittest


class FlaskTestCase(unittest.TestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    # Ensure login behaves correctly given correct credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post(
        	'/login',
        	data=dict(username='admin', password='admin'),
        	follow_redirects=True)
        self.assertIn(b'You were just logged in', response.data)

    # Ensure login behaves correctly given incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
        	'/login',
        	data=dict(username='xxx', password='x'),
        	follow_redirects=True)
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client(self)
        response = tester.post(
        	'/login',
        	data=dict(username='admin', password='admin'),
        	follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)

        self.assertIn(b'You were just logged out', response.data)

    # Ensure main page needs login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertTrue(b'You need to login first' in response.data)

    # Ensure logout page needs login
    def test_logout_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'You need to login first' in response.data)

    #Ensure posts appear on main page
    def test_posts_show_up(self):
        tester = app.test_client(self)
        response = tester.post(
        	'/login',
        	data=dict(username='admin', password='admin'),
        	follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)

        self.assertIn(b'Welcome to Flask', response.data)

if __name__ == '__main__':
    unittest.main()