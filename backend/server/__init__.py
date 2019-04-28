import os

from flask import Flask, jsonify, g, redirect, url_for, request
from flask_cors import CORS, cross_origin

import config

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

import sys




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


    from server.helpers.db_helper import get_table
    from server.models.user import User

  
       
    # A simple page that says server status
    @app.route('/')
    @cross_origin()
    def home():
        return jsonify('The server is running!!')
    
    # Import the blueprints
    from .users import users
    app.register_blueprint(users.users)
    from .auth import auth
    app.register_blueprint(auth.auth)

    # A simple page that says server status
    @app.route('/image', methods=['POST'])
    @cross_origin()
    def image():
        # print(request.get_json())
        req = request.get_json()
        image = req.get('image', None)
        if image:
            from .helpers.images import upload_image
            try:
                print(upload_image(image, 'image/png', '.psng'))
            except Exception as e:
                print(e)
         

        return jsonify('The server is running!!')
    

   
    return app


