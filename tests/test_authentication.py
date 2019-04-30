""" Test the authentication mechanism of authentic flask """
import base64

import pytest
from authentic.utils import get_account_entity
from passlib.hash import pbkdf2_sha256
from tests.support.sample_app import app

Account = get_account_entity()


class TestAuthentication:
    """Class to test authentication mechanism"""

    @pytest.fixture(scope="function", autouse=True)
    def client(self):
        """ Setup client for test cases """
        yield app.test_client()

    @pytest.fixture(scope="function", autouse=True)
    def account(self):
        """ Setup dummy account for test cases """

        new_account = Account.create({
            'email': 'johndoe@domain.com',
            'username': 'johndoe',
            'name': 'John Doe',
            'password': pbkdf2_sha256.hash('duMmy@123'),
            'phone': '90080000800',
            'roles': ['ADMIN']
        })
        yield new_account

    def test_authenticated_class_view(self, client, account):
        """ Test the authenticated class based view """
        rv = client.get(f'/accounts/{account.id}')
        assert rv.status_code == 401
        assert rv.json == {
            'code': 401,
            'message': {'_entity': 'Authentication Failed'}}

        # Test with incorrect credentials
        headers = {
            'Authorization': b'Basic ' + base64.b64encode(b'johndoe:dummy@123'),
        }
        rv = client.get(f'/accounts/{account.id}', headers=headers)
        assert rv.status_code == 401
        assert rv.json == {
            'code': 401, 'message': {'_entity': 'Authentication Failed'}}

        # Test with correct credentials now
        headers = {
            'Authorization': b'Basic ' + base64.b64encode(b'johndoe:duMmy@123'),
        }
        rv = client.get(f'/accounts/{account.id}', headers=headers)
        assert rv.status_code == 200
        assert rv.json == {
            'account':  {'email': 'johndoe@domain.com',
                         'id': account.id,
                         'is_active': True,
                         'is_locked': False,
                         'is_verified': False,
                         'name': 'John Doe',
                         'phone': '90080000800',
                         'timezone': None,
                         'title': None,
                         'username': 'johndoe'}
        }

    def test_authenticated_func_view(self, client):
        """ Test the authenticated function based view """
        # Test with correct credentials now
        headers = {
            'Authorization': b'Basic ' + base64.b64encode(b'johndoe:duMmy@123'),
        }
        rv = client.get('/accounts/current', headers=headers)
        assert rv.status_code == 200
        assert rv.json == {'account': 'johndoe'}

        # Test with no credentials
        rv = client.get('/accounts/current')
        assert rv.status_code == 200
        assert rv.json == {'account': 'anonymous'}
