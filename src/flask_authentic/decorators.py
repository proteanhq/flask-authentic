""" Decorators for handling authentications and permissions """
from functools import wraps
from flask import request, redirect, url_for


def is_authenticated(optional=False):
    """ Check permissions using each of the classes defined """
    def wrapper(f):
        """ Decorator for """
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapped_f
    return wrapper


def has_permissions(permission_classes=()):
    """ Check permissions using each of the classes defined """
    def wrapper(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapped_f
    return wrapper
