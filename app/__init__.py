#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:16546
# datetime:2021/7/5 9:03
# software: PyCharm
'''
this is functiondescription
'''
# import module your need
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_migrate import Migrate
from flask_moment import Moment
import pymysql
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# 数据库报错问题
pymysql.install_as_MySQLdb()

# 读取配置文件的配置信息
app.config.from_pyfile('E:\Web_Flask\config\config.py')
db = SQLAlchemy(app)
manager = Manager(app)
bt = Bootstrap(app)
migrate = Migrate(app, db)
moment = Moment(app)

# 配置日志信息
# 设置日志的记录等级

logging.basicConfig(level=logging.DEBUG)

# 创建日志记录器，指明日志保存的路径，每个日志文件的最大大小，保存日志文件个数上限
file_log_handler = RotatingFileHandler("E:\Web_Flask\logs/logs", maxBytes=1024 * 1024 * 100, backupCount=10)

# 创建日志记录格式
formatter = logging.Formatter('%(asctime)s-%(levelname)s %(filename)s:%(lineno)d %(message)s')

# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)

# 为全局的日志工具对象(flask app使用的)添加日志记录器
logging.getLogger().addHandler(file_log_handler)

