#!/usr/bin/python3
"""Index file for app_views"""

from models import storage
from flask import make_response, jsonify
from api.views import app_views
from flasgger.utils import swag_from


@app_views.route("/status", methods=["GET"], strict_slashes=False)
@swag_from("documentation/indexes/status.yml")
def api_state():
    """Returns the status of the API"""
    return make_response(jsonify({"status": "OK"}), 200)


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
@swag_from("documentation/indexes/stats.yml")
def api_stats():
    """Returns important api stats"""

    data = {
        "admins": "Admin",
        "courses": "Course",
        "departments": "Department",
        "students": "Student",
        "teachers": "Teacher",
    }

    db_stats = {}
    for key, value in data.items():
        db_stats[key] = storage.count(value)

    return jsonify(db_stats)
