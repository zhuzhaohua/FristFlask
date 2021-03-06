# encoding: utf-8

import os

DEBUG = True

# Mysql连接信息
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = '*****'
PASSWORD = '******'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = '********'
# 拼接的数据库链接信息  框架固定格式
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME,
                                                                       PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

# session加密的24位随机字符串
SECRET_KEY = os.urandom(24)
