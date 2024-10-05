#!/usr/bin/python3
"""Courses route for database"""

from models.course import Course
from models import storage
from api.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route(
    "/departments/<department_id>/courses",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def courses(department_id):
    """
    Configures GET and POST methods for the courses route
    """

    if request.method == "GET":
        department = storage.get("Department", department_id)
        with storage.session_scope() as session:
            department = session.merge(department)
            list_courses = []
            for course in department.courses:
                course_dict = course.to_dict()
                teacher = storage.get("Teacher", course.teacher_id)
                course_dict["department"] = department.name
                course_dict["teacher"] = (
                    teacher.first_name + " " + teacher.last_name
                )
                list_courses.append(course_dict)
        return jsonify(list_courses)
    else:
        if not request.get_json():
            abort(400, description="Not a valid JSON dict")
        required = ["name", "level", "course_id", "teacher_id"]
        for parameter in required:
            if parameter not in request.get_json():
                abort(
                    400,
                    description="Missing required parameter: {}".format(
                        parameter
                    ),
                )

        data = request.get_json()
        instance = Course(**data)
        instance.department_id = department_id
        storage.new(instance)
        storage.save()
        return make_response(jsonify(instance.to_dict()), 201)


@app_views.route(
    "/departments/<department_id>/courses/<course_id>",
    methods=["GET", "PUT", "DELETE"],
    strict_slashes=False,
)
def course(department_id, course_id):
    """
    Configures GET, PUT and DELETE for the course route
    """

    department = storage.get("Department", department_id)
    course = storage.get("Course", course_id)
    if not department or not course:
        abort(404)

    with storage.session_scope() as session:
        department = session.merge(department)
        if course not in department.courses:
            abort(404)

    if request.method == "GET":
        course_dict = course.to_dict()
        teacher = storage.get("Teacher", course.teacher_id)
        course_dict["department"] = department.name
        course_dict["teacher"] = teacher.first_name + " " + teacher.last_name
        return jsonify(course_dict)
    elif request.method == "PUT":
        if not request.get_json():
            abort(400, description="Not a valid JSON")

        ignore = ["id", "created_at"]
        data = request.get_json()
        for key, value in data.items():
            if key not in ignore:
                setattr(course, key, value)

        storage.save()
        return make_response(jsonify(course.to_dict()), 200)
    else:
        storage.delete(course)
        storage.save()
        return make_response(jsonify({}), 200)
