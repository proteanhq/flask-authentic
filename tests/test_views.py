""" Test the account views of authentic flask """
import json
from protean.core.repository import repo

from tests.support.sample_app import app


class TestViews:
    """Class to test Generic API Resource functionality and methods"""

    @classmethod
    def setup_class(cls):
        """ Setup for this test case"""

        # Create the test client
        cls.client = app.test_client()

    def test_create(self):
        """ Test creating an entity using CreateAPIResource """

        # Create a dog object
        account_info = {
            'username': 'johnny',
            'email': 'johnny@domain.com',
            'name': 'John Doe',
            'password': 'heLLo@123',
            'confirm_password': 'heLLo@123',
        }
        rv = self.client.post(
            '/auth/accounts', data=json.dumps(account_info),
            content_type='application/json')
        assert rv.status_code == 201

        expected_resp = {
            'account':  {'email': 'johnny@domain.com',
                         'id': 1,
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

