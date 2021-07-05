#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:memoController.py
# author:16546
# datetime:2021/7/5 9:07
# software: PyCharm
'''
this is functiondescription
'''
# import module your need
from functools import wraps
from app import app, db
from utils.response_code import RET
# 网站首页
from app.forms import RegisterForm, LoginForm, AddTodoForm, EditTodoForm, SearchTodoForm
from flask import render_template, flash, redirect, url_for, session, request
from models.memoModel import User, Todo
from flask import current_app, jsonify


def is_login(f):
    """用来判断用户是否登录成功"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        # 判断session对象中是否有seesion['user'],
        # 如果包含信息， 则登录成功， 可以访问主页；
        # 如果不包含信息， 则未登录成功， 跳转到登录界面;；
        if session.get('user', None):
            return f(*args, **kwargs)
        else:
            flash("用户必须登录才能访问%s" % (f.__name__))
            return redirect(url_for('login'))

    return wrapper


# 主页信息
@app.route('/')
def index():
    # return 'hello'
    return redirect(url_for('list'))


# 注册页面
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 1. 从前端获取用户输入的值;
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # 2. 判断用户是否已经存在? 如果返回位None，说明可以注册;
        u = User.query.filter_by(username=username).first()
        if u:
            flash("用户%s已经存在" % (u.username))
            return redirect(url_for('register'))
        else:
            u = User(username=username, email=email)
            u.password = password
            try:
              db.session.add(u)
              db.session.commit()
              flash("注册用户%s成功" % (u.username))
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(e)
                return jsonify(code=RET.DBERR, message='数据库异常，添加失败', error=str(e))
            return redirect(url_for('login'))
    return render_template('register.html',
                           form=form)


# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # 1. 判断用户是否存在?
        u = User.query.filter_by(username=username).first()
        if u and u.verify_password(password):
            try:
              session['user_id'] = u.id
              session['user'] = u.username
              flash("登录成功!")
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(e)
                return jsonify(code=RET.DBERR, message='数据库异常，登录失败', error=str(e))
            return redirect(url_for('index'))
        else:
            flash("用户名或者密码错误!")
            return redirect(url_for('login'))
    return render_template('login.html',
                           form=form)


# 登出页面
@app.route('/logout')
@is_login
def logout():
    session.pop('user_id', None)
    session.pop('user', None)
    return redirect(url_for('login'))


# 查询
@app.route('/memo/search', methods=['GET', 'POST'])
@is_login
def memo_search():
    form = SearchTodoForm()
    if form.validate_on_submit():
        username = form.username.data
        content = form.username.data
        # u = User.query.filter_by(username=username).first()
        try:
          us = User.query.filter(User.username.like("%"+username+"%") if username is not None else "").all()
          for u in us:
              session['user_id'] = u.id
              # session['user'] = u.username
              return redirect(url_for('list3'))
          cs = Todo.query.filter(Todo.content.like("%" + content + "%") if content is not None else "").all()
          for c in cs:
              session['id'] = c.id
              session['content'] = c.content
              session['user_id'] = c.user_id
              return redirect(url_for('list2'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, message='数据库异常，查询失败', error=str(e))
    return render_template('memo/search_memo.html',
                           form=form)

# 添加留言
@app.route('/memo/add', methods=['GET', 'POST'])
@is_login
def memo_add():
    form = AddTodoForm()
    if form.validate_on_submit():
        # 获取用户提交的内容
        content = form.content.data
        category_id = form.category.data
        # 添加到数据库中
        # 用户登录才可以添加任务，
        try:
          todo = Todo(content=content,
                      category_id=category_id,
                      user_id=session.get('user_id'))
          db.session.add(todo)
          db.session.commit()
          flash("留言添加成功")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, message='数据库异常，添加失败', error=str(e))
        # return redirect(url_for('todo_add'))
        return redirect(url_for('index'))
    return render_template('memo/add_memo.html',
                           form=form)


# 编辑留言
@app.route('/memo/edit/<int:id>', methods=['GET', 'POST'])
@is_login
def memo_edit(id):
    form = EditTodoForm()
    # *****重要: 编辑时需要获取原先任务的信息, 并显示到表单里面
    todo = Todo.query.filter_by(id=id).first()
    form.content.data = todo.content
    form.category.data = todo.category_id
    if form.validate_on_submit():
        # 更新时获取表单数据一定要使用request.form方法获取, 而form.content.data并不能获取用户更新后提交的表单内容
        try:
            content = request.form.get('content')
            category_id = request.form.get('category')
            # 更新到数据库里面
            todo.content = content
            todo.category_id = category_id
            db.session.add(todo)
            db.session.commit()
            flash("更新任务成功")
            return redirect(url_for('list'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, message='数据库异常，编辑失败', error=str(e))
    return render_template('memo/edit_memo.html',
                           form=form)


# 删除留言: 根据id删除
@app.route('/memo/delete/<int:id>')
@is_login
def memo_delete(id):
    try:
        todo = Todo.query.filter_by(id=id).first()
        db.session.delete(todo)
        db.session.commit()
        flash("删除成功")
        return redirect(url_for('list'))
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message='数据库异常，编辑失败', error=str(e))



# 查看留言
@app.route('/memo/list')
@app.route('/memo/list/<int:page>/')
@is_login
def list(page=1):

    todoPageObj = Todo.query.filter_by().paginate(page, per_page=app.config[
         'PER_PAGE'])
    return render_template('memo/list_memo.html',
                           todoPageObj=todoPageObj,
                           )

@app.route('/memo/list2')
@app.route('/memo/list2/<int:page>/')
@is_login
def list2(page=1):
    # 任务显示需要分页
    # Todo.query.paginate(page, per_page=5)
    todoPageObj2 = Todo.query.filter_by(content=session.get('content')).paginate(page, per_page=app.config[
        'PER_PAGE'])  # 在config.py文件中有设置
    return render_template('memo/list_two_memo.html',
                           todoPageObj=todoPageObj2,
                           )

@app.route('/memo/list3')
@app.route('/memo/list3/<int:page>/')
@is_login
def list3(page=1):
    # 任务显示需要分页
    # Todo.query.paginate(page, per_page=5)
    todoPageObj3 = Todo.query.filter_by(user_id=session.get('user_id')).paginate(page, per_page=app.config[
        'PER_PAGE'])
    return render_template('memo/list_two_memo.html',
                           todoPageObj=todoPageObj3,
                           )