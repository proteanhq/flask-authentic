""" Schemas used by the sample app"""
from protean.core.repository import repo
from protean.impl.repository.dict_repo import DictSchema

from authentic.entities import Account


class AccountSchema(DictSchema):
    """ Schema for the Account Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = Account
        schema_name = 'accounts'


repo.register(AccountSchema)
