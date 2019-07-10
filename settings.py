import os

ENV = 'production'
DEBUG = False

#  mysql+驱动://用户名:密码@主机:3306/数据库名
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/flask02day5'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'jkdfkldsj7345374^&5'
BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR, 'static/upload')
