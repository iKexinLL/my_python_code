#encoding=utf-8
"""
Created on 2016/3/21 17:50
author: iKexinLL
还未实现 正常的登陆
"""

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing #因此必须在第一次运行 服务器前创建数据库模式。
import os


app = Flask(__name__)

app.config.update(
        dict(DATABASE = os.path.join(app.root_path, 'my_web_site.db'),
             SECRET_KEY = 'development key',
             DEBUG = True,
             ROOT = 'root',
             ROOT_PASSWORD = '123'))


#连接数据库
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row

    return rv


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('my_web_site.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
    return db


def query_db(query, *args, one = False):
    cur = get_db().cursor()
    rv = cur.execute(query, args).fetchall()
    cur.close()

    return (rv[0] if rv else None) if one else rv


def check_username():
    user = query_db('select username from people_info where username = ?', request.form['username'], one = True)

    return user if user else None


def check_password(username):
    if check_username():
        password = query_db('select password from people_info where username = ?', username['username'], one = True)
        if password['password'] == request.form['password']:

            session['username'] = username['username']
            session['password'] = password['password']
            return True
        else:
            flash('密码不正确')
            return False

    else:
        flash('用户名不存在,请重新输入')
        return False


def check_nickname():
    nickname = query_db('select nickname from people_info where nickname = ?', request.form['nickname'], one = True)

    return nickname if nickname else None


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is None:
        db.close()
    g.db.close()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    flash("Welcome!")
    error = None
    if request.method == 'POST':

        if request.form['username'] == app.config['ROOT'] and request.form['password'] == app.config['ROOT_PASSWORD']:

            session['logged_in'] = True
            #flash('it\'s my pleasure to build this web')

            return redirect(url_for('show_info', methods = ['GET']))
            #return render_template('show_info.html',
                                   #username = request.form['username'], password = request.form['password'])

        else:

            username = check_username()

            if check_password(username):
                return redirect(url_for('show_info', methods = ['GET']))

    return render_template('login.html', error = error)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    flash('Welcome')
    #print(request.method)
    if  request.method == 'POST':

        name = request.form['username']

        password = request.form['password']
        nickname = request.form['nickname']

        register_name = check_username()
        register_nick_name = check_nickname()

        if register_name:
            flash('用户名已经存在,请重新输入')
            print(1)

        elif register_nick_name:
            flash('昵称已经存在,请重新输入')
            print(2)

        else:
            #print(register_nick_name['nickname'])
            query_db('insert into people_info values(?, ?, ?)', name, password, nickname)
            g.db.commit()
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/show_info', methods = ['GET'])
def show_info():

    username = session['username']
    password = session['password']

    return render_template('show_info.html', username = username, password = password)


#在文件末尾添加以单机方式启动服务器的代码
if __name__ == '__main__':
    #app.run(debug=True)
    init_db()
    print(app.config['DATABASE'])
    app.run(host = '127.0.0.1', debug = True, port = 4166)