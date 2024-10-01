#!/usr/bin/python3
""" configures the auth """
from api.auths import auth
from flask import current_app, make_response, jsonify, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from hashlib import md5
from models import storage
import jwt


@auth.route('/login',
            methods=['POST'],
            strict_slashes=False)
def login():
    """ Login the user """

    try:
        credentials = request.get_json()
    except Exception:
        abort(401, 'Not a valid json')

    login_type = credentials.get('type')
    email = credentials.get('email')
    password = credentials.get('password')

    all_objs = storage.all(login_type)
    user = None
    for obj in all_objs.values():
        if obj.email == email:
            md5_hash = md5()
            md5_hash.update(password.encode("utf-8"))
            password_hash = md5_hash.hexdigest()
            if obj.password == password_hash:
                user = obj
                break
            else:
                response = jsonify({'message': 'Incorrect Password'})
                return make_response(response, 401)

    if user:
        login_user(user)
        token = jwt.encode(
            {'user_id': user.id, 'user_type': login_type},
            current_app.config['SECRET_KEY'],
            algorithm='HS256')

        user_dict = user.to_dict()
        user_dict['type'] = login_type
        response = make_response(jsonify({'message': 'Login successful',
                                          'user': user_dict,
                                          'type': login_type}), 200)
        response.set_cookie('token', token, httponly=False)
        return response
    else:
        return make_response(jsonify({'message': 'user not found'}), 404)


@auth.route('/logout',
            strict_slashes=False)
@login_required
def logout():
    """ Log the user out """

    logout_user()

    response = jsonify({'message': 'Logout successful'})
    response.delete_cookie('token')
    return response


@auth.route('/auth_status',
            strict_slashes=False)
def auth_status():
    """ Checks the authentication status """

    if current_user.is_authenticated:
        user_dict = current_user.to_dict()
        user_dict['type'] = current_user.__class__.__name__
        return jsonify({'authenticated': True, 'user': user_dict})
    return jsonify({'authenticated': False})


@auth.route('/verify-recovery/<id>',
            methods=['POST'],
            strict_slashes=False)
def verify_recovery(id):
    """ Checks and verifies recovery_answer for a user """

    try:
        data = request.get_json()
    except Exception:
        abort(401)

    answer = str(data.get('answer'))

    models = ['Student', 'Teacher', 'Admin']
    for model in models:
        user = storage.get(model, id)
        if user:
            answer = answer.lower()
            md5_hash = md5()
            md5_hash.update(answer.encode("utf-8"))
            answer_hash = md5_hash.hexdigest()
            if answer_hash == user.recovery_answer:
                return jsonify({'verified': True})
            else:
                return jsonify({'verified': False})

    abort(404)
