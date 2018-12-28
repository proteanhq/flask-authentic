""" Blueprint for registering with a flask application """
from flask import Blueprint

from .views import ChangePasswordResource
from .views import CreateAccountResource
from .views import DeleteAccountResource
from .views import ListAccountResource
from .views import LoginResource
from .views import LogoutResource
from .views import ResetPasswordResource
from .views import SendResetPasswordEmailResource
from .views import ShowAccountResource
from .views import UpdateAccountResource


def create_blueprint(
        pk_name='identifier', pk_type='string',
        create_view=CreateAccountResource,  update_view=UpdateAccountResource,
        list_view=ListAccountResource, show_view=ShowAccountResource,
        delete_view=DeleteAccountResource):
    """ Create the blueprint for the account views"""
    account_bp = Blueprint('accounts', __name__)

    account_bp.add_url_rule(
        '/accounts', methods=['POST'],
        view_func=create_view.as_view('create_account'))

    account_bp.add_url_rule(
        f'/accounts/<{pk_type}:{pk_name}>', methods=['PUT'],
        view_func=update_view.as_view('update_account'))

    account_bp.add_url_rule(
        '/accounts', methods=['GET'],
        view_func=list_view.as_view('list_accounts'))

    account_bp.add_url_rule(
        f'/accounts/<{pk_type}:{pk_name}>', methods=['GET'],
        view_func=show_view.as_view('show_account'))

    account_bp.add_url_rule(
        f'/accounts/<{pk_type}:{pk_name}>', methods=['DELETE'],
        view_func=delete_view.as_view('delete_account'))

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
    return account_bp
