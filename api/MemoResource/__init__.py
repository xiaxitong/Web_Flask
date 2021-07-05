#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    :2020/12/14 13:57
# @Author  :daiguoyun
# @Software:PyCharm

from flask import Blueprint

toDoList_blueprint = Blueprint("toDoList", __name__)

from . import urls
