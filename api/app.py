#!/usr/bin/python3
"""The main app route for the db storage"""

from os import environ
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from flasgger import Swagger
from dotenv.main import load_dotenv

from models import storage
from api.views import app_views
from api.auths import auth


app = Flask(__name__)
app.config["SECRET_KEY"] = environ.get("SECRET_KEY")

login_manager = LoginManager(app)

CORS(auth, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.register_blueprint(app_views)
app.register_blueprint(auth)

cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


@login_manager.user_loader
def load_user(user_id):
    """Retrieves a user by id"""

    user_types = ["Admin", "Teacher", "Student"]
    for user_type in user_types:
        user = storage.get(user_type, user_id)
        if user is not None:
            return user


@app.teardown_appcontext
def close_db(err):
    """Closes the storage session on an error"""

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

    response = make_response(jsonify({"Error": "Not Found"}), 404)
    return response


app.config["SWAGGER"] = {
    #    'swagger': '2.0',
    #    'openapi': '3.0.2',
    "title": "SCHub API",
    "uiversion": 3,
    "version": "1.0.0",
    "description": "API documentation for SCHub",
    "specs_route": "/apidocs/",
    "host": environ.get("HOST", "127.0.0.1:5000"),
    "termsOfService": "None",
    "contact": '{"Name": "Aina Jesulayomi", "email": "Jesulayomi081@gmail.com"\
}, {"Name": "Samuel Iwelumo", "email": "micoliser@gmail.com"}',
}

Swagger(app)


if __name__ == "__main__":
    """ Runs the app with the environment variables """

    load_dotenv()
    app.run(
        host="0.0.0.0",
        port=environ.get("DEV_PORT", default="5000"),
        threaded=True,
    )
