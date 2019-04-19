import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.urandom(12)
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'mysql://user:password@10.1.0.102/crm_db'

class Prod(Config):
    DATABASE_URI = os.environ.get('DATABASE_URI')

class Dev(Config):
    DEBUG = True

class Test(Config):
    TESTING = True