import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'thisisapassword'

    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = '991029'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'webtest'
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False