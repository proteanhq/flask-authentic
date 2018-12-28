""" Test the account views of authentic flask """
import base64
import json

from passlib.hash import pbkdf2_sha256
from protean.core.repository import repo
from tests.support.sample_app import app


class TestViews:
    """Class to test all the account blueprint views"""

    @classmethod
    def setup_class(cls):
        """ Setup for this test case"""

        # Create the test client
        cls.client = app.test_client()
        cls.auth_header = {
            'Authorization': b'Basic ' +
                             base64.b64encode(b'janedoe:duMmy@123')
        }

        # Create a test account
        cls.account = repo.AccountSchema.create({
            'email': 'janedoe@domain.com',
            'username': 'janedoe',
            'name': 'Jane Doe',
            'password': pbkdf2_sha256.hash('duMmy@123'),
            'phone': '90080000800',
        })

    @classmethod
    def teardown_class(cls):
        """ Teardown for this test case """
        repo.AccountSchema.delete_all()

    def test_create(self):
        """ Test creating an account """

        # Create an account object
        account_info = {
            'username': 'johnny',
            'email': 'johnny@domain.com',
            'name': 'John Doe',
            'password': 'heLLo@123',
            'confirm_password': 'heLLo@123',
        }
        rv = self.client.post(
            '/auth/accounts', data=json.dumps(account_info),
            headers=self.auth_header, content_type='application/json')
        assert rv.status_code == 201

        expected_resp = {
            'account':  {'email': 'johnny@domain.com',
                         'id': rv.json['account']['id'],
                         'is_active': True,
                         'is_locked': False,
                         'is_verified': False,
                         'name': 'John Doe',
                         'phone': None,
                         'timezone': None,
                         'title': None,
                         'username': 'johnny'}
        }
        assert rv.json == expected_resp

    def test_update(self):
        """ Test updating an existing account """

        # update an account object
        update_info = {
            'phone': '9007007007',
        }
        rv = self.client.put(
            f'/auth/accounts/{self.account.id}', data=json.dumps(update_info),
            headers=self.auth_header, content_type='application/json')
        assert rv.status_code == 200
        expected_resp = {
            'account': {'email': 'janedoe@domain.com',
                        'id': self.account.id,
                        'is_active': True,
                        'is_locked': False,
                        'is_verified': False,
                        'name': 'Jane Doe',
                        'phone': '9007007007',
                        'timezone': None,
                        'title': None,
                        'username': 'janedoe'}
        }
        assert rv.json == expected_resp

    def test_show(self):
        """ Test showing an existing account """

        rv = self.client.get(
            f'/auth/accounts/{self.account.id}', headers=self.auth_header)
        assert rv.status_code == 200
        expected_resp = {
            'account': {'email': 'janedoe@domain.com',
                        'id': self.account.id,
                        'is_active': True,
                        'is_locked': False,
                        'is_verified': False,
                        'name': 'Jane Doe',
                        'phone': '9007007007',
                        'timezone': None,
                        'title': None,
                        'username': 'janedoe'}
        }
        assert rv.json == expected_resp

    def test_login(self):
        """ Test logging in using account credentials """

        # Send the login request
        credentials = {
            'username_or_email': 'johnny',
            'password': 'heLLo@79',
        }
        rv = self.client.post(
            f'/auth/login', data=json.dumps(credentials),
            content_type='application/json')
        assert rv.status_code == 422
        assert rv.json == {'code': 422,
                           'message': {'password': 'Password is not correct.'}}

        # Try using the right credentials
        credentials['password'] = 'heLLo@123'
        rv = self.client.post(
            f'/auth/login', data=json.dumps(credentials),
            content_type='application/json')
        assert rv.status_code == 200
        assert rv.json['username'] == 'johnny'

    def test_logout(self):
        """ Test logging out of the application """

        # Send the logout request
        rv = self.client.post(
            '/auth/logout', data=json.dumps({}), headers=self.auth_header,
            content_type='application/json')

        assert rv.status_code == 200
        assert rv.json == {'message': 'success'}

    def test_update_password(self):
        """ Test updating password of an account """

        # update an account object
        password_update = {
            'current_password': 'duMmy@123',
            'new_password': 'duMmy@456',
            'confirm_password': 'duMmy@456',
        }
        rv = self.client.post(
            '/auth/accounts/change-password', data=json.dumps(password_update),
            headers=self.auth_header, content_type='application/json')
        assert rv.status_code == 200

        expected_resp = {'message': 'Success'}
        assert rv.json == expected_resp

    def test_reset_password(self):
        """ Test resetting the password for an account """

        # Send a reset password request
        rv = self.client.post(
            '/auth/accounts/reset-password',
            data=json.dumps({'email': 'janedoe@domain.com'}),
            content_type='application/json')
        assert rv.status_code == 200

        expected_resp = {'message': 'Success'}
        assert rv.json == expected_resp

        # Get the verification token for the account
        account = repo.AccountSchema.get(self.account.id)
        assert account.verification_token is not None

        # Send the reset password request
        password_update = {
            'new_password': 'duMmy@789',
            'confirm_password': 'duMmy@789',
        }
        rv = self.client.post(
            f'/auth/accounts/reset-password/{account.verification_token}',
            data=json.dumps(password_update),
            content_type='application/json')
        assert rv.status_code == 200

        expected_resp = {'message': 'Success'}
        assert rv.json == expected_resp

    def test_delete(self):
        """ Test deleting an existing account """
        auth_header = {
            'Authorization': b'Basic ' +
                             base64.b64encode(b'janedoe:duMmy@789')
        }
        rv = self.client.delete(
            f'/auth/accounts/{self.account.id}', headers=auth_header)
        assert rv.status_code == 204
