#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:forms.py
# author:16546
# datetime:2021/7/5 14:48
# software: PyCharm
'''
this is functiondescription
'''
# import module your need
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo
# 注册表单
from models.memoModel import User, Category

class RegisterForm(FlaskForm):
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired(),
            Email(),

        ]
    )
    username = StringField(
        label="用户名",
        validators=[
            DataRequired(),

        ],
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired(),
            Length(6, 12, "密码必须是6-12位")
        ]
    )

    repassword = PasswordField(
        label='确认密码',
        validators=[
            EqualTo("password", "密码与确认密码不一致")
        ]
    )

    submit = SubmitField(
        label="注册"
    )

    # *****************************************************
    # 默认情况下validate_username会验证用户名是否正确, 验证的规则写在函数里面
    def validate_username(self, field):
        # filed.data ==== username表单提交的内容
        u = User.query.filter_by(username=field.data).first()
        if u:
            raise ValidationError("用户名%s已经注册" % (u.username))

    def validate_email(self, field):
        u = User.query.filter_by(email=field.data).first()
        if u:
            raise ValidationError("邮箱%s已经注册" % (u.email))


# 登录表单
class LoginForm(FlaskForm):
    username = StringField(
        label="用户名",
        validators=[
            DataRequired(),

        ],
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired(),
            # Length(6, 12, "密码必须是6-12位")
        ]
    )
    submit = SubmitField(
        label="登录"
    )
# 搜索表单
class SearchTodoForm(FlaskForm):
    username = StringField(
        label="输入关键字：",
        validators=[
            DataRequired(),

        ],
    )
    # content = StringField(
    #     label="按内容查询",
    #     validators=[
    #         DataRequired(),
    #
    #     ],
    # )
    submit = SubmitField(
        label="查询"
    )


# 关于任务的基类
class TodoForm(FlaskForm):
    content = StringField(
        label="备忘录内容",
        validators=[
            DataRequired()
        ]
    )
    # 任务类型
    category = SelectField(
        label="备忘录类型",
        coerce=int,
        choices=[(item.id, item.name) for item in Category.query.all()]
    )


class AddTodoForm(TodoForm):
    finish_time = DateTimeField(
        label="创建日期"
    )
    submit = SubmitField(
        label="添加新的内容",
    )


class EditTodoForm(TodoForm):
    submit = SubmitField(
        label="编辑任务",
    )
