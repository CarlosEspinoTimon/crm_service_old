from flask import Blueprint, jsonify, request, abort
from flask_cors import CORS, cross_origin

from server.models.user import User

from server.helpers.db_helper import get_table, get_session
from server.helpers.images import upload_image

from .helper import get_user_by_id, get_admin_id, create_user, update_user, \
                    delete_user_by_id, update_user_status

from server.decorators import check_admin

from werkzeug import exceptions



controlled_exceptions = exceptions.InternalServerError, \
    exceptions.Unauthorized, exceptions.Forbidden 

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
    try:
        user_table = get_table('users')
        res = user_table.select().execute()
        users = [User({k:v for k,v in row.items()}).__str__() \
                                    for row in res]
    except Exception as e:
        print("ERROR: ", e)
        abort(406, 'There has been an error in the server')
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
    try:
        user = get_user_by_id(id)
    except Exception as e: 
        print("ERROR: ", e)
        abort(406, 'There has been an error in the server')
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
    sess = get_session()
    try:
        admin_id = get_admin_id(request.headers.get('access_token'))
        data = request.get_json()
        user = create_user(sess, data, admin_id)
        sess.commit()
    except Exception as e:
        sess.rollback()
        if type(e) in (controlled_exceptions):
            abort(e)
        print("ERROR: ", e)
        abort(406, 'There has been an error in the server')
    return jsonify(user.__str__()), 201


@admin.route('/user/<int:user_id>', methods=['PUT'])
@check_admin
def put_user(user_id):
    '''
    Function that given the user data and its user_id it updates it.
    :param int user_id: the id of the user.
    :param dict data: the data of the user sent in the body of the request.
    '''
    sess = get_session()
    try:
        admin_id = get_admin_id(request.headers.get('access_token'))
        data = request.get_json()
        update_user(sess, user_id, data, admin_id)
        sess.commit()
    except Exception as e:
        sess.rollback()
        if type(e) in (controlled_exceptions):
            abort(e)
        print("ERROR: ", e)
        abort(406, 'There has been an error in the server')
    return jsonify('User updated'), 200


@admin.route('/user/<int:id>', methods=['DELETE'])
@check_admin
def delete_user(id):
    '''
    Function that given the user id it deletes it.
    :param int id: the id of the user.
    '''
    try:
        sess = get_session()
        delete_user_by_id(sess, id)
        sess.commit()
    except Exception as e:
        sess.rollback()
        print("ERROR: ", e)
        abort(406, 'There has been an error in the server')
    return jsonify('User deleted'), 200
    

@admin.route('/user/<int:user_id>/change-admin-status', methods=['PUT'])
@check_admin
def change_admin_status(user_id):
    '''
    Function that given the user id it can change the user privileges to grant
    or revoque admin privileges.
    :param int user_id: the id of the user.
    :param dict data: the grant/consent of the user sent in the body of the
    request.
    '''
    sess = get_session()
    try:
        admin_id = get_admin_id(request.headers.get('access_token'))
        data = request.get_json()
        update_user_status(sess, user_id, data, admin_id)
        sess.commit()
    except Exception as e:
        sess.rollback()
        if type(e) in (controlled_exceptions):
            abort(e)
        print("ERROR: ", e)
        abort(406, 'There has been an error in the server')
    return jsonify('User updated'), 200