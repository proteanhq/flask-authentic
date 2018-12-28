""" Decorators for handling authentications and permissions """
from functools import wraps

from authentic.utils import get_auth_backend
from flask import request
from protean.conf import active_config
from protean.context import context
from protean.core.exceptions import ConfigurationError
from protean.core.repository import repo
from protean.core.tasklet import Tasklet
from protean.utils.importlib import perform_import


def perform_authentication():
    """ Perform the authentication of the request """

    # Get the authorization header and build payload
    auth_header = request.headers.get('Authorization', '').split()
    auth_payload = {}
    if auth_header and len(auth_header) == 2:
        auth_payload['auth_scheme'] = auth_header[0]
        auth_payload['credentials'] = auth_header[1]

    # Get the schema and the current backend
    if not active_config.ACCOUNT_SCHEMA_CLS:
        raise ConfigurationError(
            '`ACCOUNT_SCHEMA_CLS` has not been set in the config.')
    account_schema = perform_import(active_config.ACCOUNT_SCHEMA_CLS)
    auth_backend = get_auth_backend()

    # Perform the task and check the response
    response = Tasklet.perform(
        repo, account_schema, auth_backend.AuthenticationUseCase,
        auth_backend.AuthenticationRequestObject, auth_payload)
    return response


def is_authenticated(optional=False):
    """ Decorator for checking if the request is authenticated """
    def wrapper(f):
        """ Wrapper function of the decorator """
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            """ Actual function for checking authentication """
            # Perform the authentication
            response = perform_authentication()

            # If the task failed and authentication is not optional
            # then return unauthorized
            if not response.success and not optional:
                renderer = perform_import(active_config.DEFAULT_RENDERER)
                return renderer(response.value, 401, {})

            # Set the account on the request and call the actual function
            context.set_context({
                'account': response.value if response.success else None
            })
            return f(*args, **kwargs)

        return wrapped_f
    return wrapper


def authenticated_viewset():
    """ Decorator for handling authentication of viewsets .
    GET methods are optionally authenticated and mandatory in others
    """

    def wrapper(f):
        """ Wrapper function of the decorator """

        @wraps(f)
        def wrapped_f(*args, **kwargs):
            """ Actual function for checking authentication """
            # Perform the authentication
            response = perform_authentication()

            # If the task failed and authentication is not optional
            # then return unauthorized
            if not response.success and request.method != 'GET':
                renderer = perform_import(active_config.DEFAULT_RENDERER)
                return renderer(response.value, 401, {})

            # Set the account on the request and call the actual function
            context.set_context({
                'account': response.value if response.success else None
            })
            return f(*args, **kwargs)

        return wrapped_f

    return wrapper
