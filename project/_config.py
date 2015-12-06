import os

basedir = os. path.abspath(os.path.dirname(__file__))

DATABASE = 'cars.db'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'hot_dogs'
DATABASE_PATH = os.path.join(basedir, DATABASE)