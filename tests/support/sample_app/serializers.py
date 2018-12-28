""" Serializers used by the sample app """
from authentic.entities import Account
from protean.context import context
from protean_flask.core.serializers import EntitySerializer
from protean_flask.core.serializers import ma

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
        if context.account:
            return context.account.id
        else:
            return None

    class Meta:
        entity = Human
