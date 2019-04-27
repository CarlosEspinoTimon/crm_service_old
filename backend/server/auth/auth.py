from flask import Blueprint, jsonify, request, abort, render_template
from flask_cors import CORS, cross_origin

from server.helpers.db_helper import get_table
from server.models.user import User
from flask import Blueprint, jsonify, request, abort
from flask_cors import CORS, cross_origin

from .helper import OAuthSignIn

auth = Blueprint('auth', __name__, url_prefix='/')
CORS(auth, max_age=30*86400)

@auth.route('/authorize/<provider>')
def oauth_authorize(provider):
        oauth = OAuthSignIn.get_provider(provider)
        return oauth.authorize()

@auth.route('/callback/<provider>')
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    email, access_token = oauth.callback()
    
    if email is None:
        return jsonify('Authentication failed')
    user_table = get_table('users')
    user = user_table.select(user_table.c.email == email).execute().first()
    if user:
        return jsonify('Logged in, your access token is: {}'.format(
                                                                access_token))
    else:
        return jsonify('User not registered')



    

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html',
                        title='Sign In')

