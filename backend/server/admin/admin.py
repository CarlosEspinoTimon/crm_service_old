from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin

from server.models.user import User

from server.helpers.users_helper import get_admin_id

from server.decorators import check_admin

from datetime import datetime

from server import db



admin = Blueprint('admin', __name__, url_prefix='/admin')
CORS(admin, max_age=30*86400)


@admin.route('/users/', methods=['GET'])
@check_admin
def get_all_users():
    '''
    Function that returns all the users.
    :return users: All the users.
    :rtype: list of users.
    '''
    users = [u.__str__() for u in User.query.all()]
    return jsonify(users), 200


@admin.route('/user/<int:id>', methods=['GET'])
@check_admin
def get_user(id):
    '''
    Function that given an id it returns the user.
    :param int id: the id of the user.
    :return user: The user.
    :rtype: User.
    '''
    user = User.query.get(id)
    return jsonify(user.__str__()), 200


@admin.route('/user', methods=['POST'])
@check_admin
def post_user():
    '''
    Function that given the user data it creates it.
    :param dict data: the data of the user sent in the body of the request.
    :return user: The user.
    :rtype: User.
    '''
    data = request.get_json()
    admin_id = get_admin_id(request.headers.get('username'))
    user = User(
        email = data['email'],
        admin = False,
        admin_privileges_by = admin_id,
        created_at = datetime.now(),
        modified_at = datetime.now(),
        created_by = admin_id,
        modified_by = admin_id
    )
    user.set_password('12345')
    db.session.add(user)
    db.session.commit()

    return jsonify(user.__str__()), 201


@admin.route('/user/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    '''
    Function that given the user data and its user_id it updates it.
    :param int user_id: the id of the user.
    :param dict data: the data of the user sent in the body of the request.
    '''
    data = request.get_json()
    admin_id = get_admin_id(request.headers.get('username'))
    user = User.query.get(user_id)
    user.modified_at = datetime.now()
    user.modified_by = admin_id
    db.session.add(user)
    db.session.commit()
    return jsonify('User updated'), 200


@admin.route('/user/<int:id>', methods=['DELETE'])
@check_admin
def delete_user(id):
    '''
    Function that given the user id it deletes it.
    :param int id: the id of the user.
    '''
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify('User deleted'), 200
    

@admin.route('/user/<int:user_id>/give-admin-privileges', methods=['PUT'])
@check_admin
def give_admin_privileges(user_id):
    '''
    Function that given the user id it can change the user privileges to grant
    or revoque admin privileges.
    :param int user_id: the id of the user.
    :param dict data: the grant/consent of the user sent in the body of the
    request.
    '''
    data = request.get_json()
    admin_id = get_admin_id(request.headers.get('username'))
    user = User.query.get(user_id)
    user.modified_at = datetime.now()
    user.modified_by = admin_id
    user.admin = True
    user.admin_privileges_by = admin_id
    db.session.add(user)
    db.session.commit()
    return jsonify('User updated'), 200


@admin.route('/user/<int:user_id>/revoke-admin-privileges', methods=['PUT'])
@check_admin
def revoke_admin_privileges(user_id):
    '''
    Function that given the user id it can change the user privileges to grant
    or revoque admin privileges.
    :param int user_id: the id of the user.
    :param dict data: the grant/consent of the user sent in the body of the
    request.
    '''
    data = request.get_json()
    admin_id = get_admin_id(request.headers.get('username'))
    user = User.query.get(user_id)
    user.modified_at = datetime.now()
    user.modified_by = admin_id
    user.admin = False
    user.admin_privileges_by = admin_id
    db.session.add(user)
    db.session.commit()
    return jsonify('User updated'), 200


@admin.route('/set-password/<string:password>', methods=['PUT'])
def set_password(password):
    '''
    Function that allows you to change the password of the first user.
    :param str password: the new password.
    request.
    '''
    print("aaa")
    user = User.query.get(1) 
    # print(user)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify('User updated'), 200


