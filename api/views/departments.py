#!/usr/bin/python3
""" Departments route for database """
from models.department import Department
from models import storage
from api.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route(
    '/departments',
    methods=['GET', 'POST'],
    strict_slashes=False)
@swag_from('documentation/departments/departments.yml')
def departments():
    """
        Configures GET and POST methods for the departments route
    """

    if request.method == 'GET':
        all_departments = storage.all('Department').values()
        list_departments = [department.to_dict()
                            for department in all_departments]
        return jsonify(list_departments)
    else:
        if not request.get_json():
            abort(400, description="Not a valid JSON dict")
        if 'name' not in request.get_json():
            abort(400,
                  description="Missing required parameter: name")

        data = request.get_json()
        instance = Department(**data)
        storage.new(instance)
        storage.save()
        return make_response(jsonify(instance.to_dict()), 201)


@app_views.route(
    '/departments/<department_id>',
    methods=['GET', 'PUT', 'DELETE'],
    strict_slashes=False)
@swag_from('documentation/departments/department.yml')
def department(department_id):
    """
        Configures GET, PUT and DELETE for the department route
    """

    department = storage.get('Department', department_id)
    if not department:
        abort(404)

    if request.method == 'GET':
        return jsonify(department.to_dict())
    elif request.method == 'PUT':
        if not request.get_json():
            abort(400, description="Not a valid JSON")

        ignore = ['id', 'created_at']
        data = request.get_json()
        for key, value in data.items():
            if key not in ignore:
                setattr(department, key, value)

        storage.new(department)
        storage.save()
        return make_response(jsonify(department.to_dict()), 200)
    else:
        storage.delete(department)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route(
    '/departments/<department_id>/students',
    methods=['GET', 'PUT', 'DELETE'],
    strict_slashes=False)
@swag_from('documentation/departments/department_students.yml')
def department_students(department_id):
    """
        Configures GET, PUT and DELETE for the department route
    """

    department = storage.get('Department', department_id)
    with storage.session_scope() as session:
        department = session.merge(department)
        list_students = []
        for student in department.students:
            student_dict = student.to_dict()
            student_dict['department'] = department.name
            list_students.append(student_dict)
        return jsonify(list_students)
