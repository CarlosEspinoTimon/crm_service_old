from flask import Blueprint, jsonify, request, abort, current_app
from flask_cors import CORS, cross_origin

from sqlalchemy import create_engine, MetaData, Table, asc, desc, and_

from server.models.user import User


bp = Blueprint('users', __name__, url_prefix='/')
CORS(bp, max_age=30*86400)

@bp.route('/customers', methods=['GET'])
def get_all_customers():
    try:
        users_table = Table('customers', current_app.metadata, autoload=True)
        res = users_table.select().execute()
        users = [User({k:v for k,v in row.items()}).__str__() for row in res]
    except Exception as e:
        # TODO catch the error to ignore database errors
        print("ERROR: ", e)
        abort(406, 'There has been an error in the server')
    return jsonify(users), 200


@bp.route('/customer/<int:id>', methods=['GET'])
def get_customer(id):
    try:
        users_table = Table('customers', current_app.metadata, autoload=True)
        res = users_table.select(users_table.c.id == id).execute().first()
        user = User({k:v for k,v in res.items()})
    except Exception as e:
        # TODO catch the error to ignore database errors
        print("ERROR: ", e)
        abort(406, 'There has been an error in the server')
    return jsonify(user.__str__()), 200


@bp.route('/customer', methods=['POST'])
def post_customer():
    return jsonify('Create user endpoint'), 501


@bp.route('/customer/<int:id>', methods=['PUT'])
def put_customer(id):
    return jsonify('Update user endpoint'), 501


@bp.route('/customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    return jsonify('Delete user endpoint'), 501

