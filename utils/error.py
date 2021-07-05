#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:error.py
# author:16546
# datetime:2021/7/5 14:51
# software: PyCharm
'''
this is functiondescription
'''
# import module your need
'''
  统一自定义异常处理
'''
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from .response_code import RET


def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    response = jsonify(message=message, **kwargs)
    return response,code


def invalid_token():
    response, code = api_abort(RET.Unauthorized, message='invalid token')
    return response, code


def token_missing():
    response, code = api_abort(RET.Unauthorized, message='token missed')
    return response, code


class ValidationError(ValueError):
    pass

# 简单列了一些，别的类型自己可以根据需要扩展补充

def validation_error(e):
    return api_abort(400, e.args[0])