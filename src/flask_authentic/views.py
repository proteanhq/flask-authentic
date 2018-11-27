""" Views for managing accounts and authentication """
from flask import request

from protean.core.entity import Entity
from protean.conf import active_config
from protean.core.exceptions import ConfigurationError
from protean.utils.importlib import perform_import

from authentic.usecases.core import \
    (CreateAccountUseCase, CreateAccountRequestObject,
     UpdateAccountUseCase, UpdateAccountRequestObject,
     ChangeAccountPasswordUseCase, ChangeAccountPasswordRequestObject,
     SendResetPasswordEmailUsecase, SendResetPasswordEmailRequestObject,
     ResetPasswordUsecase, ResetPasswordRequestObject,
     LoginUseCase, LoginRequestObject)

from protean_flask.core.views import (CreateAPIResource, UpdateAPIResource,
                                      GenericAPIResource)


class AccountViewMixin:
    """ Reusable Mixin for retrieving the schema and serializer classes"""

    def get_schema_cls(self):
        """ Get the schema class from the config """
        if not hasattr(active_config, 'ACCOUNT_SCHEMA_CLS'):
            raise ConfigurationError(
                '`ACCOUNT_SCHEMA_CLS` has not been set in the config.')
        return perform_import(active_config.ACCOUNT_SCHEMA_CLS)

    def get_serializer_cls(self):
        """ Get the serializer class from the settings"""
        if not hasattr(active_config, 'ACCOUNT_SERIALIZER_CLS'):
            raise ConfigurationError(
                '`ACCOUNT_SERIALIZER_CLS` has not been set in the config.')
        return perform_import(active_config.ACCOUNT_SERIALIZER_CLS)


class CreateAccountResource(AccountViewMixin, CreateAPIResource):
    """ API View for creating an account """
    request_object_cls = CreateAccountRequestObject
    usecase_cls = CreateAccountUseCase


class UpdateAccountResource(AccountViewMixin, UpdateAPIResource):
    """ API View for updating an account """
    request_object_cls = UpdateAccountRequestObject
    usecase_cls = UpdateAccountUseCase


class ChangePasswordResource(AccountViewMixin, GenericAPIResource):
    """ API View for updating the account password """
    request_object_cls = ChangeAccountPasswordRequestObject
    usecase_cls = ChangeAccountPasswordUseCase

    def post(self, identifier):
        """Change the password for the account
         Expected Parameters:
             identifier = <int/string>, identifies the entity
        """
        payload = {
            'identifier': identifier,
            'data': request.payload
        }
        return self._process_request(
            self.usecase_cls, self.request_object_cls, payload=payload,
            no_serialization=True)


class SendResetPasswordEmailResource(AccountViewMixin, GenericAPIResource):
    """ API View for sending the reset password link """
    request_object_cls = SendResetPasswordEmailRequestObject
    usecase_cls = SendResetPasswordEmailUsecase

    def post(self):
        """Send an email for resetting the account password
        """
        return self._process_request(
            self.usecase_cls, self.request_object_cls,
            payload=request.payload, no_serialization=True)


class ResetPasswordResource(AccountViewMixin, GenericAPIResource):
    """ API View for resetting the account password """
    request_object_cls = ResetPasswordRequestObject
    usecase_cls = ResetPasswordUsecase

    def post(self, token):
        """Reset the password for the account
         Expected Parameters:
             token = <string>, verification token for resetting the password
        """
        payload = {
            'token': token,
            'data': request.payload
        }
        return self._process_request(
            self.usecase_cls, self.request_object_cls, payload=payload,
            no_serialization=True)


class LoginResource(AccountViewMixin, GenericAPIResource):
    """ API View for logging in to the App"""
    request_object_cls = LoginRequestObject
    usecase_cls = LoginUseCase

    def post(self):
        """Login to the application
        """
        response = self._process_request(
            self.usecase_cls, self.request_object_cls,
            payload=request.payload, no_serialization=True)
        if isinstance(response, Entity):
            return response.to_dict()
        return response
