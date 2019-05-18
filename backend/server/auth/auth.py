from flask_cors import CORS, cross_origin

from server.models.user import User
from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin


auth = Blueprint('auth', __name__, url_prefix='/')
CORS(auth, max_age=30*86400)


@auth.route('/login', methods=['POST'])
def login():
    '''
    Function that given a username and a password as headers it checks if there
    is a user in the database and generates a token.
    '''
    username = request.headers.get('username') 
    password = request.headers.get('password')
    user = User.query.filter_by(email=username).first()

    if user and user.check_password(password):
        return jsonify('Token: {}'.format(user.generate_auth_token(1800)))
    else:
        return jsonify('Unauthorized'), 401

