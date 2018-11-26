""" Views for managing accounts and authentication """
from protean.conf import active_config
from protean.core.exceptions import ConfigurationError
from protean.utils.importlib import perform_import

from authentic.usecases.core import \
    (CreateAccountUseCase, CreateAccountRequestObject,
     UpdateAccountUseCase, UpdateAccountRequestObject)

from protean_flask.core.views import CreateAPIResource, UpdateAPIResource


class AccountViewMixin:
    """ Reusable Mixin for retrieving the schema and serializer classes"""

    def get_schema_cls(self):
        """ Get the schema class from the config """
        if not hasattr(active_config, 'ACCOUNT_SCHEMA'):
            raise ConfigurationError(
                '`ACCOUNT_SCHEMA` has not been set in the config.')
        return perform_import(active_config.ACCOUNT_SCHEMA)

    def get_serializer_cls(self):
        """ Get the serializer class from the settings"""
        if not hasattr(active_config, 'ACCOUNT_SERIALIZER'):
            raise ConfigurationError(
                '`ACCOUNT_SERIALIZER` has not been set in the config.')
        return perform_import(active_config.ACCOUNT_SERIALIZER)


class CreateAccountResource(AccountViewMixin, CreateAPIResource):
    """ API View for creating an account """
    request_object_cls = CreateAccountRequestObject
    usecase_cls = CreateAccountUseCase


class UpdateAccountResource(AccountViewMixin, UpdateAPIResource):
    """ API View for updating an account """
    request_object_cls = UpdateAccountRequestObject
    usecase_cls = UpdateAccountUseCase
