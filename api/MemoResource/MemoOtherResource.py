#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    :2020/12/14 14:19
# @Author  :daiguoyun
# @Software:PyCharm

from flask_restful import Resource, reqparse

from utils import commons
from utils.response_code import RET


class ToDoListOtherResource(Resource):

    # 代办事宜列表批量查询
    def get(self):
        todolists_get_parser = reqparse.RequestParser()
        todolists_get_parser.add_argument('AutoID', type=int, location='args', help='AutoID参数类型不正确或缺失')
        todolists_get_parser.add_argument('Title', type=str, location='args', help='Title参数类型不正确或缺失')
        todolists_get_parser.add_argument('Page', type=int, location='args', help='Page参数类型不正确或缺失')
        todolists_get_parser.add_argument('Size', type=int, location='args', help='Size参数类型不正确或缺失')

        kwargs = todolists_get_parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        # 查询记录
        # result_dict = ToDoListController.get_all(**kwargs)
        if result_dict['code'] != "2000":
            if result_dict['code'] in [RET.DATAERR, RET.LOGINERR, RET.NODATA]:
                return {'code': result_dict['code'], 'message': result_dict['message']}
            else:
                return {'code': result_dict['code'], 'message': result_dict['message']}
        else:
            return {'code': result_dict['code'], 'message': result_dict['message'], 'data': result_dict['data']}

