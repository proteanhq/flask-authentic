""" Test the account views of authentic flask """
import base64
import json

import pytest
from authentic.utils import get_account_entity
from passlib.hash import pbkdf2_sha256

from .support.sample_app import app

Account = get_account_entity()


class TestViews:
    """Class to test all the account blueprint views"""

    @pytest.fixture(scope="function", autouse=True)
    def client(self):
        """ Setup client for test cases """
        yield app.test_client()

    @pytest.fixture(scope="function", autouse=True)
    def auth_header(self):
        """ Setup auth header for test cases """
        header = {
            'Authorization': b'Basic ' +
                             base64.b64encode(b'janedoe:duMmy@123')
        }
        yield header

    @pytest.fixture(scope="function", autouse=True)
    def account(self):
        """ Setup dummy account for test cases """

        new_account = Account.create({
            'email': 'janedoe@domain.com',
            'username': 'janedoe',
            'name': 'Jane Doe',
            'password': pbkdf2_sha256.hash('duMmy@123'),
            'phone': '90080000800',
        })
        yield new_account

    def test_create(self, client, auth_header):
        """ Test creating an account """

        # Create an account object
        account_info = {
            'username': 'johnny',
            'email': 'johnny@domain.com',
            'name': 'John Doe',
            'password': 'heLLo@123',
            'confirm_password': 'heLLo@123',
        }
        rv = client.post(
            '/auth/accounts', data=json.dumps(account_info),
            headers=auth_header, content_type='application/json')
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

    def test_update(self, client, auth_header, account):
        """ Test updating an existing account """

        # update an account object
        update_info = {
            'phone': '9007007007',
        }
        rv = client.put(
            f'/auth/accounts/{account.id}', data=json.dumps(update_info),
            headers=auth_header, content_type='application/json')
        assert rv.status_code == 200
        expected_resp = {
            'account': {'email': 'janedoe@domain.com',
                        'id': account.id,
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

    def test_show(self, client, auth_header, account):
        """ Test showing an existing account """

        rv = client.get(
            f'/auth/accounts/{account.id}', headers=auth_header)
        assert rv.status_code == 200
        expected_resp = {
            'account': {'email': 'janedoe@domain.com',
                        'id': account.id,
                        'is_active': True,
                        'is_locked': False,
                        'is_verified': False,
                        'name': 'Jane Doe',
                        'phone': '90080000800',
                        'timezone': None,
                        'title': None,
                        'username': 'janedoe'}
        }
        assert rv.json == expected_resp

    def test_login(self, client, auth_header):
        """ Test logging in using account credentials """

        # Create an account object
        account_info = {
            'username': 'johnny',
            'email': 'johnny@domain.com',
            'name': 'John Doe',
            'password': 'heLLo@123',
            'confirm_password': 'heLLo@123',
        }
        rv = client.post(
            '/auth/accounts', data=json.dumps(account_info),
            headers=auth_header, content_type='application/json')
        assert rv.status_code == 201

        # Send the login request
        credentials = {
            'username_or_email': 'johnny',
            'password': 'heLLo@79',
        }
        rv = client.post(
            f'/auth/login', data=json.dumps(credentials),
            content_type='application/json')
        assert rv.status_code == 422
        assert rv.json == {'code': 422,
                           'message': {'password': 'Password is not correct.'}}

        # Try using the right credentials
        credentials['password'] = 'heLLo@123'
        rv = client.post(
            f'/auth/login', data=json.dumps(credentials),
            content_type='application/json')
        assert rv.status_code == 200
        assert rv.json['username'] == 'johnny'

    def test_logout(self, client, auth_header):
        """ Test logging out of the application """

        # Send the logout request
        rv = client.post(
            '/auth/logout', data=json.dumps({}), headers=auth_header,
            content_type='application/json')

        assert rv.status_code == 200
        assert rv.json == {'message': 'success'}

    def test_update_password(self, client, auth_header):
        """ Test updating password of an account """

        # update an account object
        password_update = {
            'current_password': 'duMmy@123',
            'new_password': 'duMmy@456',
            'confirm_password': 'duMmy@456',
        }
        rv = client.post(
            '/auth/accounts/change-password', data=json.dumps(password_update),
            headers=auth_header, content_type='application/json')
        assert rv.status_code == 200

        expected_resp = {'message': 'Success'}
        assert rv.json == expected_resp

    def test_reset_password(self, client, account):
        """ Test resetting the password for an account """

        # Send a reset password request
        rv = client.post(
            '/auth/accounts/reset-password',
            data=json.dumps({'email': 'janedoe@domain.com'}),
            content_type='application/json')
        assert rv.status_code == 200

        expected_resp = {'message': 'Success'}
        assert rv.json == expected_resp

        # Get the verification token for the account
        account = Account.get(account.id)
        assert account.verification_token is not None

        # Send the reset password request
        password_update = {
            'new_password': 'duMmy@789',
            'confirm_password': 'duMmy@789',
        }
        rv = client.post(
            f'/auth/accounts/reset-password/{account.verification_token}',
            data=json.dumps(password_update),
            content_type='application/json')
        assert rv.status_code == 200

        expected_resp = {'message': 'Success'}
        assert rv.json == expected_resp

    def test_delete(self, client, account):
        """ Test deleting an existing account """
        auth_header = {
            'Authorization': b'Basic ' +
                             base64.b64encode(b'janedoe:duMmy@123')
        }
        rv = client.delete(
            f'/auth/accounts/{account.id}', headers=auth_header)
        assert rv.status_code == 204
