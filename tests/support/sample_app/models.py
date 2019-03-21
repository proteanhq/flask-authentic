""" Schemas used by the sample app"""
from authentic.entities import Account
from authentic.entities import Session
from protean.impl.repository.dict_repo import DictModel

from .entities import Human


class AccountModel(DictModel):
    """ Schema for the Account Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = Account
        schema_name = 'accounts'


class SessionModel(DictModel):
    """ Schema for the Session Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = Session
        schema_name = 'sessions'


class HumanModel(DictModel):
    """ Schema for the Human Entity"""

    class Meta:
        """ Meta class for schema options"""
        entity = Human
        schema_name = 'humans'
