#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import jsonify, g
from flask_restful import reqparse, fields, Resource
from controller.toDolistController import ToDoListController

from utils import commons
from utils.response_code import RET


class ToDoListResource(Resource):
    # 单条信息查询
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('UserID', type=int, location='args', required=True, help='UserID参数类型不正确或缺失')
        parser.add_argument('UserType', type=int, location='args', required=True, help='UserType参数类型不正确或缺失')
        parser.add_argument('CollegeID', type=int, location='args', required=True, help='CollegeID参数类型不正确或缺失')
        parser.add_argument('ExperimentID', type=int, location='args', required=True, help='ExperimentID参数类型不正确或缺失')
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get("UserID") != g.user.get("UserID"):
            return jsonify(code=RET.PARAMERR, message='用户ID与Token不匹配')
        if kwargs.get("UserType") != g.user.get("UserType"):
            return jsonify(code=RET.PARAMERR, message='用户类型不匹配，权限不开放')

        return ToDoListController.query(**kwargs)

    # 修改
    def put(self):
        # 实验单条信息修改需要输入的字段
        parser = reqparse.RequestParser()
        parser.add_argument('UserID', type=int, location='form', required=True, help='UserID参数类型不正确或缺失')
        parser.add_argument('UserType', type=int, location='form', required=True, help='UserType参数类型不正确或缺失')
        parser.add_argument('CollegeID', type=int, location='form', required=True, help='CollegeID参数类型不正确或缺失')
        parser.add_argument('ExperimentID', type=int, location='form', required=True, help='ExperimentID参数类型不正确或缺失')
        parser.add_argument('ExperimentCourseNumber', type=str, location='form', help='ExperimentCourseNumber参数类型不正确或缺失')
        parser.add_argument('ExperimentName', type=str, location='form', help='ExperimentName参数类型不正确或缺失')
        parser.add_argument('CourseID', type=int, location='form', help='CourseID参数类型不正确或缺失')
        parser.add_argument('ExperimentSummary', type=str, location='form', help='ExperimentSummary参数类型不正确或缺失')
        parser.add_argument('ScoreType', type=int, location='form', help='ScoreType参数类型不正确或缺失')
        parser.add_argument('ChooseStartTime', type=str, location='form', help='ChooseStartTime参数类型不正确或缺失')
        parser.add_argument('ChooseEndTime', type=str, location='form', help='ChooseEndTime参数类型不正确或缺失')
        parser.add_argument('SubmissionEndTime', type=str, location='form', help='SubmissionEndTime参数类型不正确或缺失')
        parser.add_argument('ExperimentPicUrl', type=str, location='form', help='ExperimentPicUrl参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        # 验证UserID和token
        if kwargs.get("UserID") != g.user.get("UserID"):
            return jsonify(code=RET.PARAMERR, message='用户ID与Token不匹配')
        if kwargs.get("UserType") != g.user.get("UserType"):
            return jsonify(code=RET.PARAMERR, message='用户类型不匹配，权限不开放')

        del kwargs['UserID']
        del kwargs['UserType']

        return ToDoListController.put(**kwargs)

    # 删除
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('AutoID', type=int, location='form', required=True, help='AutoID参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        # if kwargs.get("UserID") != g.user.get("UserID"):
        #     return jsonify(code=RET.PARAMERR, message='用户ID与Token不匹配')
        # if kwargs.get("UserType") != g.user.get("UserType"):
        #     return jsonify(code=RET.PARAMERR, message='用户类型不匹配，权限不开放')

        return ToDoListController.delete(**kwargs)

    # 添加
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Title', type=str, location='form', required=True, help='Title参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        # if kwargs.get("UserID") != g.user.get("UserID"):
        #     return jsonify(code=RET.PARAMERR, message='用户ID与Token不匹配')
        # if kwargs.get("UserType") != g.user.get("UserType"):
        #     return jsonify(code=RET.PARAMERR, message='用户类型不匹配，权限不开放')

        # 接口层对返回数据再继续处理，如果有必要的话
        result_dict = ToDoListController.add(**kwargs)
        if result_dict['code'] != '2000':
            return jsonify(code=result_dict['code'], message=result_dict['message'], error=result_dict['error'])
        else:
            return jsonify(code=result_dict['code'], message=result_dict['message'], data=result_dict['data'])
