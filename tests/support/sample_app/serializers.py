""" Serializers used by the sample app """
from flask import request

from protean_flask.core.serializers import EntitySerializer, ma

from authentic.entities import Account

from .entities import Human


class AccountSerializer(EntitySerializer):
    """ Serializer for Account Entity"""
    id = ma.fields.Integer()

    class Meta:
        entity = Account
        fields = ('id', 'name', 'username', 'email', 'title', 'phone',
                  'timezone', 'is_locked', 'is_active', 'is_verified')


class HumanSerializer(EntitySerializer):
    """ Serializer for Human Entity"""
    current_account = ma.fields.Method('get_current_account')

    def get_current_account(self, obj):
        """ Return the current logged in user """
        if request.account:
            return request.account.id
        else:
            return None

    class Meta:
        entity = Human
