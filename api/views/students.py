#!/usr/bin/python3
""" Students route for database """
from models.student import Student
from models import storage
from api.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route(
    '/students',
    methods=['GET', 'POST'],
    strict_slashes=False)
@swag_from('documentation/students/students.yml')
def students():
    """
        Configures GET and POST methods for the students route
    """

    if request.method == 'GET':
        level = request.args.get('level')
        email = request.args.get('email')
        all_students = storage.all('Student').values()

        if email:
            for student in all_students:
                # to get the id of a particular student with email address
                if student.email == email:
                    if student.password:
                        password = True
                    else:
                        password = False
                    student_dict = student.to_dict()
                    student_dict['password'] = password
                    return jsonify(student_dict)

            abort(404)

        if level is None:
            list_students = []
            for student in all_students:
                student_dict = student.to_dict()
                department = storage.get('Department', student.department_id)
                student_dict['department'] = department.name
                list_students.append(student_dict)
        else:
            list_students = []
            for student in all_students:
                if student.current_level == int(level):
                    student_dict = student.to_dict()
                    department = storage.get('Department',
                                             student.department_id)
                    student_dict['department'] = department.name
                    list_students.append(student_dict)
        return jsonify(list_students)
    else:
        if not request.get_json():
            abort(400, description='Not a valid JSON dict')
        required = ['first_name',
                    'last_name',
                    'age',
                    'matric_no',
                    'department_id',
                    'start_level',
                    'current_level',
                    'email']
        for parameter in required:
            if parameter not in request.get_json():
                abort(400,
                      description='Missing required parameter: {}'.format(
                          parameter))

        data = request.get_json()
        instance = Student(**data)
        storage.new(instance)
        storage.save()
        return make_response(jsonify(instance.to_dict()), 201)


@app_views.route(
    '/students/<student_id>',
    methods=['GET', 'PUT', 'DELETE'],
    strict_slashes=False)
@swag_from('documentation/students/student.yml')
def student(student_id):
    """
        Configures GET, PUT and DELETE for the student route
    """

    student = storage.get('Student', student_id)
    if not student:
        abort(404)

    if request.method == 'GET':
        student_dict = student.to_dict()
        department = storage.get('Department', student.department_id)
        student_dict['department'] = department.name
        return jsonify(student_dict)
    elif request.method == 'PUT':
        if not request.get_json():
            abort(400, description='Not a valid JSON')

        ignore = ['id', 'created_at', 'start_level']
        data = request.get_json()
        for key, value in data.items():
            if key not in ignore:
                setattr(student, key, value)

        storage.new(student)
        storage.save()
        return make_response(jsonify(student.to_dict()), 200)
    else:
        storage.delete(student)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route(
    '/students/<student_id>/courses',
    methods=['GET'],
    strict_slashes=False)
@swag_from('documentation/students/student_courses.yml')
def studentCourses(student_id):
    """
        Configures GET and POST methods for the student/<id>/courses route
    """

    student = storage.get('Student', student_id)
    department = storage.get('Department', student.department_id)
    with storage.session_scope() as session:
        department = session.merge(department)
        list_courses = [course.to_dict() for course in department.courses]
    return jsonify(list_courses)
