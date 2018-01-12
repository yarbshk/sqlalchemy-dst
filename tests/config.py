import os

DEBUG = os.environ.get('DEBUG')

SERVER_HOST = os.environ.get('SERVER_HOST')
SERVER_PORT = int(os.environ.get('SERVER_PORT'))

SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = True
