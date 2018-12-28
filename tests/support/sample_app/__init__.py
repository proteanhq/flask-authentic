""" Sample Protean Flask app for testing"""
from flask import Flask
from flask import jsonify
from protean.context import context
from protean_flask import Protean
from protean_flask.core.views import ShowAPIResource

from flask_authentic.account import create_blueprint
from flask_authentic.decorators import is_authenticated

from .schemas import AccountSchema
from .serializers import AccountSerializer
from .views import HumanResourceSet

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
    if context.account:
        return jsonify({'account': context.account.username})
    else:
        return jsonify({'account': 'anonymous'})


app.register_blueprint(create_blueprint(pk_type='int'), url_prefix='/auth')
app.add_url_rule('/accounts/<int:identifier>',
                 view_func=SomeProtectedView.as_view('show_account'))

app.add_url_rule('/accounts/current', view_func=get_current_account)
api.register_viewset(HumanResourceSet, 'humans', '/humans', pk_type='int')
