from flask import current_app

from sqlalchemy import Table

def get_table(table_name):
    '''
    Function that given a name, it returns the table from the database.
    :param string table_name: the name of the table
    :return table: the table from the database
    '''
    return Table(table_name, current_app.metadata, autoload=True)

def get_session():
    '''
    Function that returns the session of the connection with the database
    :return sess: The session
    '''
    return current_app.Session()