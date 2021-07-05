#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:start.py
# author:16546
# datetime:2021/7/5 9:05
# software: PyCharm
'''
this is functiondescription
'''
# import module your need
from app import app

from controller.memoController import *

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=8080)