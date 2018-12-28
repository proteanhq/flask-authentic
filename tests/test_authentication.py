""" Test the authentication mechanism of authentic flask """
import base64

from passlib.hash import pbkdf2_sha256
from protean.core.repository import repo
from tests.support.sample_app import app


class TestAuthentication:
    """Class to test authentication mechanism"""

    @classmethod
    def setup_class(cls):
        """ Setup for this test case"""
        # Create the test client
        cls.client = app.test_client()

        # Create a test account
        cls.account = repo.AccountSchema.create({
            'email': 'johndoe@domain.com',
            'username': 'johndoe',
            'name': 'John Doe',
            'password': pbkdf2_sha256.hash('duMmy@123'),
            'phone': '90080000800',
            'roles': ['ADMIN']
        })

    @classmethod
    def teardown_class(cls):
        """ Teardown for this test case """
        repo.AccountSchema.delete_all()

    def test_authenticated_class_view(self):
        """ Test the authenticated class based view """
        rv = self.client.get(f'/accounts/{self.account.id}')
        assert rv.status_code == 401
        assert rv.json == {
            'code': 422,
            'message': {'auth_scheme': 'Authentication scheme is mandatory',
                        'credentials': 'Credentials is mandatory'}}

        # Test with incorrect credentials
        headers = {
            'Authorization': b'Basic ' + base64.b64encode(b'johndoe:dummy@123'),
        }
        rv = self.client.get(f'/accounts/{self.account.id}', headers=headers)
        assert rv.status_code == 401
        assert rv.json == {
            'code': 422, 'message': {'password': 'Password is not correct.'}}

        # Test with correct credentials now
        headers = {
            'Authorization': b'Basic ' + base64.b64encode(b'johndoe:duMmy@123'),
        }
        rv = self.client.get(f'/accounts/{self.account.id}', headers=headers)
        assert rv.status_code == 200
        assert rv.json == {
            'account':  {'email': 'johndoe@domain.com',
                         'id': self.account.id,
                         'is_active': True,
                         'is_locked': False,
                         'is_verified': False,
                         'name': 'John Doe',
                         'phone': '90080000800',
                         'timezone': None,
                         'title': None,
                         'username': 'johndoe'}
        }

    def test_authenticated_func_view(self):
        """ Test the authenticated function based view """
        # Test with correct credentials now
        headers = {
            'Authorization': b'Basic ' + base64.b64encode(b'johndoe:duMmy@123'),
        }
        rv = self.client.get('/accounts/current', headers=headers)
        assert rv.status_code == 200
        assert rv.json == {'account': 'johndoe'}

        # Test with no credentials
        rv = self.client.get('/accounts/current')
        assert rv.status_code == 200
        assert rv.json == {'account': 'anonymous'}
