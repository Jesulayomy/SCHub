#!/usr/bin/python3
"""creates the auth blueprint"""

from flask import Blueprint


auth = Blueprint("auth", __name__, url_prefix="/auth/")


from api.auths.login import *  # noqa
