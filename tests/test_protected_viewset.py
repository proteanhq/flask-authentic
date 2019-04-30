"""Module to test Protected Viewset functionality and features"""
import base64
import json

import pytest
from authentic.utils import get_account_entity
from passlib.hash import pbkdf2_sha256

from .support.sample_app import app
from .support.sample_app.entities import Human

Account = get_account_entity()


class TestGenericAPIResourceSet:
    """Class to test GenericAPIResourceSet functionality and methods"""

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

    def test_set_show(self, client, auth_header, account):
        """ Test retrieving an entity using the resource set"""
        # Create a human object
        human = Human.create(id=1, name='John')

        # Fetch this human by ID
        rv = client.get('/humans/1')
        assert rv.status_code == 200
        expected_resp = {
            'human': {'contact': None, 'id': 1, 'name': 'John',
                      'current_account': None}
        }
        assert rv.json == expected_resp

        # Fetch again with authentication
        rv = client.get('/humans/1', headers=auth_header)
        assert rv.status_code == 200
        expected_resp = {
            'human': {'contact': None, 'id': 1, 'name': 'John',
                      'current_account': account.id}
        }
        assert rv.json == expected_resp

        # Delete the human now
        human.delete()

    def test_set_list(self, client, auth_header, account):
        """ Test listing an entity using the resource set"""
        # Create Human objects
        Human.create(id=2, name='Jane')
        Human.create(id=3, name='Mary')

        # Get the list of humans
        rv = client.get('/humans?order_by[]=id')
        assert rv.status_code == 200
        assert rv.json['total'] == 2
        assert rv.json['humans'][0] == {'id': 2, 'name': 'Jane',
                                        'contact': None, 'current_account': None}

        # Fetch again with authentication
        rv = client.get('/humans?order_by[]=id', headers=auth_header)
        assert rv.status_code == 200
        assert rv.json['total'] == 2
        assert rv.json['humans'][0] == {'id': 2, 'name': 'Jane',
                                        'contact': None, 'current_account': account.id}

    def test_set_create(self, client, auth_header, account):
        """ Test creating an entity using the resource set """
        # Create a human object
        rv = client.post('/humans', data=json.dumps(dict(id=1, name='John')),
                         content_type='application/json')
        assert rv.status_code == 401

        # Send again with authentication
        rv = client.post('/humans', headers=auth_header, data=json.dumps(dict(id=1, name='John')),
                         content_type='application/json')
        assert rv.status_code == 201
        expected_resp = {
            'human': {'contact': None, 'id': 1, 'name': 'John',
                      'current_account': account.id}
        }
        assert rv.json == expected_resp

        # Delete the human now
        human = Human.get(1)
        human.delete()

    def test_set_update(self, client, auth_header, account):
        """ Test updating an entity using the resource set """

        # Create a human object
        human = Human.create(id=1, name='John')

        # Update the human object
        rv = client.put('/humans/1', data=json.dumps(dict(contact='9000900090')),
                        content_type='application/json')
        assert rv.status_code == 401

        # Send again with authentication
        rv = client.put('/humans/1', headers=auth_header,
                        data=json.dumps(dict(contact='9000900090')),
                        content_type='application/json')
        expected_resp = {
            'human': {'contact': '9000900090', 'id': 1, 'name': 'John',
                      'current_account': account.id}
        }
        assert rv.json == expected_resp

        # Delete the human now
        human.delete()

    def test_set_delete(self, client, auth_header, account):
        """ Test deleting an entity using the resource set """

        # Create a human object
        Human.create(id=1, name='John')

        # Delete the dog object
        rv = client.delete('/humans/1')
        assert rv.status_code == 401

        # Send again with authentication
        rv = client.delete('/humans/1', headers=auth_header)
        assert rv.status_code == 204
        assert rv.data == b''
