#!/usr/bin/python3
# -*- coding: utf-8 -*-



from flask_restful import Api
from . import toDoList_blueprint
from .MemoResource  import ToDoListResource
from .MemoOtherResource import ToDoListOtherResource

api = Api(toDoList_blueprint)

# 首页实验列表信息查询（无需token）
api.add_resource(ToDoListResource, '/memo/list', endpoint="MemoResource")

api.add_resource(ToDoListOtherResource, '/memo/list', endpoint="MemoOtherResource")