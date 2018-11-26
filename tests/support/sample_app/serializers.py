""" Serializers used by the sample app """
from marshmallow import fields
from protean_flask.core.serializers import EntitySerializer
from authentic.entities import Account


class AccountSerializer(EntitySerializer):
    """ Serializer for Account Entity"""
    id = fields.Integer()

    class Meta:
        entity = Account
        fields = ('id', 'name', 'username', 'email', 'title', 'phone',
                  'timezone', 'is_locked', 'is_active', 'is_verified')
