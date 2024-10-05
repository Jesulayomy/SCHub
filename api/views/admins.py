#!/usr/bin/python3
"""Admins route for database"""

from models.admin import Admin
from models import storage
from api.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route("/admins", methods=["GET", "POST"], strict_slashes=False)
@swag_from("documentation/admins/admins.yml")
def admins():
    """
    Configures GET and POST methods for the admins route
    """

    if request.method == "GET":
        email = request.args.get("email")
        all_admins = storage.all("Admin").values()

        if email:
            for admin in all_admins:
                # to get the id of a particular admin with email address
                if admin.email == email:
                    return jsonify(admin.to_dict())

            abort(404)

        list_admins = [admin.to_dict() for admin in all_admins]
        return jsonify(list_admins)
    else:
        if not request.get_json():
            abort(400, description="Not a valid JSON dict")
        required = ["first_name", "last_name", "email", "password"]
        for parameter in required:
            if parameter not in request.get_json():
                abort(
                    400,
                    description="Missing required parameter: {}".format(
                        parameter
                    ),
                )

        data = request.get_json()
        instance = Admin(**data)
        storage.new(instance)
        storage.save()
        return make_response(jsonify(instance.to_dict()), 201)


@app_views.route(
    "/admins/<admin_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False
)
@swag_from("documentation/admins/admin.yml")
def admin(admin_id):
    """
    Configures GET, PUT and DELETE for the admin route
    """

    admin = storage.get("Admin", admin_id)
    if not admin:
        abort(404)

    if request.method == "GET":
        return jsonify(admin.to_dict())
    elif request.method == "PUT":
        if not request.get_json():
            abort(400, description="Not a valid JSON")

        ignore = ["id", "created_at"]
        data = request.get_json()
        for key, value in data.items():
            if key not in ignore:
                setattr(admin, key, value)

        storage.new(admin)
        storage.save()
        return make_response(jsonify(admin.to_dict()), 200)
    else:
        storage.delete(admin)
        storage.save()
        return make_response(jsonify({}), 200)
