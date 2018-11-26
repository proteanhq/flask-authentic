""" Sample Protean Flask app for testing"""
from flask import Flask

from protean_flask import Protean
from flask_authentic.blueprint import account_bp

app = Flask(__name__)
api = Protean(app)

app.register_blueprint(account_bp, url_prefix='/auth')


