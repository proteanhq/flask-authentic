"""Module to test Protected Viewset functionality and features"""
import base64
import json

from passlib.hash import pbkdf2_sha256
from protean.core.repository import repo
from tests.support.sample_app import app


class TestGenericAPIResourceSet:
    """Class to test GenericAPIResourceSet functionality and methods"""

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

    def test_set_show(self):
        """ Test retrieving an entity using the resource set"""
        # Create a human object
        repo.HumanSchema.create(id=1, name='John')

        # Fetch this human by ID
        rv = self.client.get('/humans/1')
        assert rv.status_code == 200
        expected_resp = {
            'human': {'contact': None, 'id': 1, 'name': 'John',
                      'current_account': None}
        }
        assert rv.json == expected_resp

        # Fetch again with authentication
        rv = self.client.get('/humans/1', headers=self.auth_header)
        assert rv.status_code == 200
        expected_resp = {
            'human': {'contact': None, 'id': 1, 'name': 'John',
                      'current_account': self.account.id}
        }
        assert rv.json == expected_resp

        # Delete the human now
        repo.HumanSchema.delete(1)

    def test_set_list(self):
        """ Test listing an entity using the resource set"""
        # Create Human objects
        repo.HumanSchema.create(id=2, name='Jane')
        repo.HumanSchema.create(id=3, name='Mary')

        # Get the list of humans
        rv = self.client.get('/humans?order_by[]=id')
        assert rv.status_code == 200
        assert rv.json['total'] == 2
        assert rv.json['humans'][0] == {'id': 2, 'name': 'Jane',
                                        'contact': None, 'current_account': None}

        # Fetch again with authentication
        rv = self.client.get('/humans?order_by[]=id', headers=self.auth_header)
        assert rv.status_code == 200
        assert rv.json['total'] == 2
        assert rv.json['humans'][0] == {'id': 2, 'name': 'Jane',
                                        'contact': None, 'current_account': self.account.id}

    def test_set_create(self):
        """ Test creating an entity using the resource set """
        # Create a human object
        rv = self.client.post('/humans',
                              data=json.dumps(
                                  dict(id=1, name='John')),
                              content_type='application/json')
        assert rv.status_code == 401

        # Send again with authentication
        rv = self.client.post('/humans',
                              headers=self.auth_header,
                              data=json.dumps(
                                  dict(id=1, name='John')),
                              content_type='application/json')
        assert rv.status_code == 201
        expected_resp = {
            'human': {'contact': None, 'id': 1, 'name': 'John',
                      'current_account': self.account.id}
        }
        assert rv.json == expected_resp

        # Delete the human now
        repo.HumanSchema.delete(1)

    def test_set_update(self):
        """ Test updating an entity using the resource set """

        # Create a human object
        repo.HumanSchema.create(id=1, name='John')

        # Update the human object
        rv = self.client.put('/humans/1',
                             data=json.dumps(dict(contact='9000900090')),
                             content_type='application/json')
        assert rv.status_code == 401

        # Send again with authentication
        rv = self.client.put('/humans/1',
                             headers=self.auth_header,
                             data=json.dumps(dict(contact='9000900090')),
                             content_type='application/json')
        expected_resp = {
            'human': {'contact': '9000900090', 'id': 1, 'name': 'John',
                      'current_account': self.account.id}
        }
        assert rv.json == expected_resp

        # Delete the human now
        repo.HumanSchema.delete(1)

    def test_set_delete(self):
        """ Test deleting an entity using the resource set """

        # Create a human object
        repo.HumanSchema.create(id=1, name='John')

        # Delete the dog object
        rv = self.client.delete('/humans/1')
        assert rv.status_code == 401

        # Send again with authentication
        rv = self.client.delete('/humans/1', headers=self.auth_header)
        assert rv.status_code == 204
        assert rv.data == b''
