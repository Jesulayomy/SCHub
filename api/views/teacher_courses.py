#!/usr/bin/python3
"""Courses route for database"""

from models import storage
from api.views import app_views
from flask import abort, jsonify
from flasgger.utils import swag_from


@app_views.route("/teachers/<teacher_id>/courses", strict_slashes=False)
@swag_from("documentation/teacher_courses/teacher_courses.yml")
def teacher_courses(teacher_id):
    """
    Configures GET method for the teacher courses route
    """

    teacher = storage.get("Teacher", teacher_id)
    if not teacher:
        abort(404)
    with storage.session_scope() as session:
        teacher = session.merge(teacher)
        list_courses = [course.to_dict() for course in teacher.courses]

    return jsonify(list_courses)
