""" Schemas used by the sample app"""
from authentic.entities import Account
from authentic.entities import Session
from protean.core.repository import repo
from protean.impl.repository.dict_repo import DictSchema

from .entities import Human


class AccountSchema(DictSchema):
    """ Schema for the Account Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = Account
        schema_name = 'accounts'


class SessionSchema(DictSchema):
    """ Schema for the Session Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = Session
        schema_name = 'sessions'


class HumanSchema(DictSchema):
    """ Schema for the Human Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = Human
        schema_name = 'humans'


repo.register(HumanSchema)
repo.register(SessionSchema)
repo.register(AccountSchema)
