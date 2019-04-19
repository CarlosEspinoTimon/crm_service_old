import os

from flask import Flask, jsonify

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

    # A simple page that says server status
    @app.route('/')
    @cross_origin() 
    def home():
        sess = app.Session()
        users_table = Table('customers', app.metadata, autoload=True)

        stmt = users_table.select()
        res = [{k:v for k,v in row.items()} for row in sess.execute(stmt)]

        return jsonify('Server running and connected to db: {}'.format(res))

    
   
    return app


