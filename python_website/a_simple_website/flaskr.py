#encoding=utf-8
"""
Created on 2016/3/21 13:39
author: iKexinLL
"""

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing #因此必须在第一次运行 服务器前创建数据库模式。
import os


#create our little application :)
app = Flask(__name__)
#configuration
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key', #secret_key （密钥）用于保持客户端会话安全，请谨慎地选择密钥，并尽可能的使它 复杂而且不容易被猜到
    USERNAME='admin',
    PASSWORD='default'
))
#app.config.from_object(__name__)


#app.config.from_envvar('FALSKR_SETTING', silent = True)
#通常，从一个配置文件中导入配置是比较好的做法
#这样做就可以设置一个 FLASKR_SETTINGS 的环境变量来指定一个配置文件，并 根据该文件来重载缺省的配置。
#silent 开关的作用是告诉 Flask 如果没有这个环境变量 不要报错。



def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()


#装饰的函数会在请求之前调用，且不传递参数
@app.before_request
def before_request():
    g.db = connect_db()


#这个装饰器下的函数在响应对象构建后被调用。
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is None:
        db.close()
    g.db.close()


#显示条目
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries = entries)

#添加条目
@app.route('/add', methods = ['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()

    flash('New entry was successfully posted')

    return redirect(url_for('show_entries'))


#登陆和注销
@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')

            return redirect(url_for('show_entries'))

    return render_template('login.html', error = error)



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))







#在文件末尾添加以单机方式启动服务器的代码
if __name__ == '__main__':
    #app.run(debug=True)
    init_db()
    print(app.config['DATABASE'])
    app.run(host = '127.0.0.1', port = 4167)
