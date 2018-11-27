""" Sample Protean Flask app for testing"""
from flask import Flask, request, jsonify

from protean_flask import Protean
from protean_flask.core.views import ShowAPIResource

from flask_authentic.blueprint import account_bp
from flask_authentic.decorators import is_authenticated

from .serializers import AccountSerializer
from .schemas import AccountSchema

app = Flask(__name__)
api = Protean(app)


class SomeProtectedView(ShowAPIResource):
    """ A simple protected class based view """
    schema_cls = AccountSchema
    serializer_cls = AccountSerializer
    decorators = [is_authenticated()]


@ is_authenticated(optional=True)
def get_current_account():
    """ View to test optional authentication """
    if request.account:
        return jsonify({'account': request.account.username})
    else:
        return jsonify({'account': 'anonymous'})


app.register_blueprint(account_bp, url_prefix='/auth')
app.add_url_rule('/accounts/<int:identifier>',
                 view_func=SomeProtectedView.as_view('show_account'))

app.add_url_rule('/accounts/current', view_func=get_current_account)
