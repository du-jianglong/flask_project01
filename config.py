import os
from datetime import timedelta

# 开启调试模式
DEBUD = True

# 设置　24　位的　SECRET_KEY
SECRET_KEY = os.urandom(24)

# 设置　7　天 session 保存记录
# 如果不设置　PERMANENT_SESSION_LIFETIME　那么　session.permanent = True　默认为保存　31　天
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'myblogdb'
USERNAME = 'root'
PASSWORD = 'dujianglong'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False
