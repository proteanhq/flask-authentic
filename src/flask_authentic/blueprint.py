""" Blueprint for registering with a flask application """
from flask import Blueprint

from flask_authentic.views import (CreateAccountResource, UpdateAccountResource,
                                   ChangePasswordResource, ResetPasswordResource,
                                   SendResetPasswordEmailResource, LoginResource,
                                   LogoutResource)


account_bp = Blueprint('accounts', __name__)

account_bp.add_url_rule(
    '/accounts', methods=['POST'],
    view_func=CreateAccountResource.as_view('create_account'))

account_bp.add_url_rule(
    '/accounts/<int:identifier>', methods=['PUT'],
    view_func=UpdateAccountResource.as_view('update_account'))

account_bp.add_url_rule(
    '/accounts/change-password', methods=['POST'],
    view_func=ChangePasswordResource.as_view('change_password'))

account_bp.add_url_rule(
    '/accounts/reset-password', methods=['POST'],
    view_func=SendResetPasswordEmailResource.as_view('send_reset_password'))

account_bp.add_url_rule(
    '/accounts/reset-password/<token>', methods=['POST'],
    view_func=ResetPasswordResource.as_view('reset_password'))

account_bp.add_url_rule(
    '/login', methods=['POST'], view_func=LoginResource.as_view('login'))

account_bp.add_url_rule(
    '/logout', methods=['POST'], view_func=LogoutResource.as_view('logout'))
