#!/usr/bin/python3
""" Teachers route for database """
from models.teacher import Teacher
from models import storage
from api.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route(
    '/teachers',
    methods=['GET', 'POST'],
    strict_slashes=False)
@swag_from('documentation/teachers/teachers.yml', methods=['GET'])
@swag_from('documentation/teachers/new_teachers.yml', methods=['POST'])
def teachers():
    """
        Configures GET and POST methods for the teachers route
    """

    if request.method == 'GET':
        email = request.args.get('email')
        all_teachers = storage.all('Teacher').values()

        if email:
            for teacher in all_teachers:
                # to get the id of a particular teacher with email address
                if email and teacher.email == email:
                    if teacher.password:
                        password = True
                    else:
                        password = False
                    teacher_dict = teacher.to_dict()
                    teacher_dict['password'] = password
                    return jsonify(teacher_dict)

            abort(404)

        list_teachers = []
        for teacher in all_teachers:
            teacher_dict = teacher.to_dict()
            department = storage.get('Department', teacher.department_id)
            teacher_dict['department'] = department.name
            list_teachers.append(teacher_dict)
        return jsonify(list_teachers)
    else:
        if not request.get_json():
            abort(400, description="Not a valid JSON dict")
        required = ['first_name',
                    'last_name',
                    'department_id',
                    'email']
        for parameter in required:
            if parameter not in request.get_json():
                abort(400,
                      description="Missing required parameter: {}".format(
                          parameter))

        data = request.get_json()
        instance = Teacher(**data)
        storage.new(instance)
        storage.save()
        return make_response(jsonify(instance.to_dict()), 201)


@app_views.route(
    '/teachers/<teacher_id>',
    methods=['GET', 'PUT', 'DELETE'],
    strict_slashes=False)
@swag_from('documentation/teachers/teacher.yml', methods=['GET'])
@swag_from('documentation/teachers/delete_teacher.yml', methods=['DELETE'])
@swag_from('documentation/teachers/update_teacher.yml', methods=['PUT'])
def teacher(teacher_id):
    """
        Configures GET, PUT and DELETE for the teacher route
    """

    teacher = storage.get('Teacher', teacher_id)
    if not teacher:
        abort(404)

    if request.method == 'GET':
        teacher_dict = teacher.to_dict()
        department = storage.get('Department', teacher.department_id)
        teacher_dict['department'] = department.name
        return jsonify(teacher_dict)
    elif request.method == 'PUT':
        if not request.get_json():
            abort(400, description="Not a valid JSON")

        ignore = ['id', 'created_at']
        data = request.get_json()
        for key, value in data.items():
            if key not in ignore:
                setattr(teacher, key, value)

        storage.new(teacher)
        storage.save()
        return make_response(jsonify(teacher.to_dict()), 200)
    else:
        storage.delete(teacher)
        storage.save()
        return make_response(jsonify({}), 200)
