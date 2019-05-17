import os

from flask import Flask, jsonify, g, redirect, url_for, request
from flask_cors import CORS, cross_origin

import config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import sys


db = SQLAlchemy()
migrate = Migrate()

def create_app(app_config='config.Config'):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(app_config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    
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
    from .admin import admin
    app.register_blueprint(admin.admin)
    
    
    return app


