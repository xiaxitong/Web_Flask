#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:commons.py
# author:16546
# datetime:2021/7/5 9:31
# software: PyCharm
'''
this is functiondescription
'''
# import module your need
from datetime import datetime as cdatetime
from datetime import date, time
from werkzeug.routing import BaseConverter
from sqlalchemy import DateTime, Date, Time

# 定义正则转换器
class ReConverter(BaseConverter):
    """"""

    def __init__(self, url_map, regex):
        # 调用父类初始化方法
        super(ReConverter, self).__init__(url_map)

        # 保存正则表达式
        self.regex = regex

def put_remove_none(**args):
    """
    PUT方法更新时，如果参数不是必填，用reqparse检验参数会将数据转为空，
    数据库有的字段可能不允许为空，故用该方法解决
    :param args: 原始数据字典
    :return: 除去None数据的字典
    """
    for key in list(args.keys()):
        if args[key] is None or args[key] == '':
            del args[key]
            continue

    args = dict(args)
    return args
def convert_datetime(value):
    """
    数据库datetime类型转时间字符串
    :param value:
    :return:
    """
    if value:
        if isinstance(value, (cdatetime, DateTime)):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, (date, Date)):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, (Time, time)):
            return value.strftime("%H:%M:%S")
    else:
        return ""