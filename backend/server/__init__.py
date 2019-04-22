import os

from flask import Flask, jsonify, g, redirect, url_for, render_template, request
from flask_cors import CORS, cross_origin

import config

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

import sys


# from functools import wraps
from .decorators import check_token



def create_app(app_config='config.Config'):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(app_config)

    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI']
    db = SQLAlchemy(app)
    app.db = db
    
    app.engine = create_engine(app.config['DATABASE_URI'], pool_pre_ping=True)
    app.metadata = MetaData(bind=app.engine)
    app.Session = sessionmaker(bind=app.engine)

    # from flask_login import LoginManager, login_user, logout_user, current_user, login_required
    # from flask_login import LoginManager, current_user, login_user
    # lm = LoginManager()
    # lm.init_app(app)
    # lm.login_view = 'login'


    from server.helpers.db_helper import get_table
    from server.models.user import User

    # def check_token(func):
    #     @wraps(func)
    #     def decorated_funcion(*args, **kwargs):
    #         # from google.oauth2 import id_token
    #         # from google.auth.transport import requests
    #         import requests
    #         try:
    #             token = request.headers.get('access_token')
    #             url = 'https://www.googleapis.com/plus/v1/people/me?access_token='
    #             res = requests.get(url+token)
    #             if res.status_code == 200:
    #                 email = res.json()['emails'][0]['value']
    #                 user_table = get_table('users')
    #                 user = user_table.select(
    #                                 user_table.c.email == email).execute().first()
    #                 # return True if user else False
    #                 if user:
    #                     return func(*args, **kwargs)
    #                 else:    
    #                     return jsonify('Unauthorized'), 401
    #             # return False
    #             return jsonify('Unauthorized'), 401
    #         except Exception as e:
    #             # Invalid token
    #             print("invalid"  , e)
    #             pass
    #     return decorated_funcion
            
       
    # A simple page that says server status
    @app.route('/server-status/')
    @cross_origin()
    @check_token
    def home():
        # print(request.get_json().get('access_token'))
        # print(request.headers.get('access_token'))
        # # if check_token(request.args.get('access_token')):
        # if check_token(request.headers.get('access_token')):
        #     return jsonify('The server is running!!')
        # else:
        #     return jsonify('Unauthorized'), 401

        return jsonify('The server is running!!')
    
    # Import the blueprints
    from .users import users
    app.register_blueprint(users.bp)
    from .oauth import oauth
    app.register_blueprint(oauth.bp)

    

    # @lm.user_loader
    # def load_user(id):
    #     user_table = get_table('users')
    #     res = user_table.select(user_table.c.id == id).execute().first()
    #     return User({k:v for k, v in res.items()})
            

    from .auth import OAuthSignIn

    @app.route('/authorize/<provider>')
    def oauth_authorize(provider):
        # Flask-Login function
        # if not current_user.is_anonymous:
        #     return redirect(url_for('index'))
        oauth = OAuthSignIn.get_provider(provider)
        return oauth.authorize()

    @app.route('/callback/<provider>')
    def oauth_callback(provider):
        # if not current_user.is_anonymous:
        #     return redirect(url_for('index'))
        oauth = OAuthSignIn.get_provider(provider)
        email, access_token = oauth.callback()
        if email is None:
            # I need a valid email address for my user identification
            # flash('Authentication failed.')
            # return redirect(url_for('index'))
            return jsonify('Authentication failed')
        # Look if the user already exists
        user_table = get_table('users')
        user = user_table.select(user_table.c.email == email).execute().first()
        if user:
            return jsonify('Logged in, your access token is: {}'.format(access_token))
        else:
            return jsonify('User not registered')


   
        

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # if g.user is not None and g.user.is_authenticated():
        #     return redirect(url_for('index'))
        return render_template('login.html',
                            title='Sign In')
    
   
    return app


