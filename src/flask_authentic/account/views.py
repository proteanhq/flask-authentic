""" Views for managing accounts and authentication """


from authentic.usecases.core import ChangeAccountPasswordRequestObject
from authentic.usecases.core import ChangeAccountPasswordUseCase
from authentic.usecases.core import CreateAccountRequestObject
from authentic.usecases.core import CreateAccountUseCase
from authentic.usecases.core import LoginRequestObject
from authentic.usecases.core import LoginUseCase
from authentic.usecases.core import LogoutRequestObject
from authentic.usecases.core import LogoutUseCase
from authentic.usecases.core import ResetPasswordRequestObject
from authentic.usecases.core import ResetPasswordUsecase
from authentic.usecases.core import SendResetPasswordEmailRequestObject
from authentic.usecases.core import SendResetPasswordEmailUsecase
from authentic.usecases.core import UpdateAccountRequestObject
from authentic.usecases.core import UpdateAccountUseCase
from flask import request
from protean.conf import active_config
from protean.context import context
from protean.core.entity import Entity
from protean.core.exceptions import ConfigurationError
from protean.utils.importlib import perform_import
from protean_flask.core.views import CreateAPIResource
from protean_flask.core.views import DeleteAPIResource
from protean_flask.core.views import GenericAPIResource
from protean_flask.core.views import ListAPIResource
from protean_flask.core.views import ShowAPIResource
from protean_flask.core.views import UpdateAPIResource

from flask_authentic.decorators import is_authenticated


class AccountViewMixin:
    """ Reusable Mixin for retrieving the schema and serializer classes"""

    def get_schema_cls(self):
        """ Get the schema class from the config """
        if not active_config.ACCOUNT_SCHEMA_CLS:
            raise ConfigurationError(
                '`ACCOUNT_SCHEMA_CLS` has not been set in the config.')
        return perform_import(active_config.ACCOUNT_SCHEMA_CLS)

    def get_serializer_cls(self):
        """ Get the serializer class from the settings"""
        if not active_config.ACCOUNT_SERIALIZER_CLS:
            raise ConfigurationError(
                '`ACCOUNT_SERIALIZER_CLS` has not been set in the config.')
        return perform_import(active_config.ACCOUNT_SERIALIZER_CLS)


class CreateAccountResource(AccountViewMixin, CreateAPIResource):
    """ API View for creating an account """
    request_object_cls = CreateAccountRequestObject
    usecase_cls = CreateAccountUseCase
    decorators = [is_authenticated()]


class UpdateAccountResource(AccountViewMixin, UpdateAPIResource):
    """ API View for updating an account """
    request_object_cls = UpdateAccountRequestObject
    usecase_cls = UpdateAccountUseCase
    decorators = [is_authenticated()]


class ListAccountResource(AccountViewMixin, ListAPIResource):
    """ API View for list an accounts """
    decorators = [is_authenticated()]


class ShowAccountResource(AccountViewMixin, ShowAPIResource):
    """ API View for showing an account """
    decorators = [is_authenticated()]


class DeleteAccountResource(AccountViewMixin, DeleteAPIResource):
    """ API View for deleting an account """
    decorators = [is_authenticated()]


class ChangePasswordResource(AccountViewMixin, GenericAPIResource):
    """ API View for updating the account password """
    request_object_cls = ChangeAccountPasswordRequestObject
    usecase_cls = ChangeAccountPasswordUseCase
    decorators = [is_authenticated()]

    def post(self):
        """Change the password for the account
        """
        payload = {
            'identifier': context.account.id,
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


class LogoutResource(AccountViewMixin, GenericAPIResource):
    """ API View for logging in to the App"""
    request_object_cls = LogoutRequestObject
    usecase_cls = LogoutUseCase
    decorators = [is_authenticated()]

    def post(self):
        """Logout of the application
        """
        return self._process_request(
            self.usecase_cls, self.request_object_cls,
            payload={'account': context.account}, no_serialization=True)
