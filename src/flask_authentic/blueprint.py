""" Blueprint for registering with a flask application """
from flask import Blueprint

from flask_authentic.views import CreateAccountResource, UpdateAccountResource


account_bp = Blueprint('accounts', __name__)

account_bp.add_url_rule(
    '/accounts', methods=['POST'],
    view_func=CreateAccountResource.as_view('create_account'))

account_bp.add_url_rule(
    '/accounts/<int:identifier>', methods=['PUT'],
    view_func=UpdateAccountResource.as_view('update_account'))
