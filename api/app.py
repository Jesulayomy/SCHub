#!/usr/bin/python3
""" The main app route for the db storage """

from models import storage
from api.views import app_views
from api.auths import auth
from os import environ, getenv
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from flasgger import Swagger
from flasgger.utils import swag_from
from dotenv.main import load_dotenv


app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

login_manager = LoginManager(app)

CORS(
    auth,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True)

app.register_blueprint(app_views)
app.register_blueprint(auth)

cors = CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True)


@login_manager.user_loader
def load_user(user_id):
    """ Retrieves a user by id """

    user_types = ['Admin', 'Teacher', 'Student']
    for user_type in user_types:
        user = storage.get(user_type, user_id)
        if user is not None:
            return user


@app.teardown_appcontext
def close_db(err):
    """ Closes the storage session on an error """

    storage.close()


@app.errorhandler(404)
def not_found(err):
    """
        404 Error for unused route or path
    ---
    responses:
      200:
        description: A successful response
        examples:
          application/json: Hello World
    """

    response = make_response(jsonify({'Error': 'Not Found'}), 404)
    return response


app.config['SWAGGER'] = {
#    'swagger': '2.0',
#    'openapi': '3.0.2',
    'title': 'SCHub API',
    'uiversion': 3,
    'version': '1.0.0',
    'description': 'API documentation for SCHub',
    'specs_route': '/apidocs/',
    'host': 'app.schub.me',
    'termsOfService': 'None',
    'contact': '{"Name": "Aina Jesulayomi", "email": "Jesulayomi081@gmail.com"\
}, {"Name": "Samuel Iwelumo", "email": "micoliser@gmail.com"}'
}

Swagger(app)


if __name__ == '__main__':
    """ Runs the app with the environment variables """

    load_dotenv()
    app.run(
        host='0.0.0.0',
        port=environ.get('DB_DEV_PORT', default='5000'),
        threaded=True)
