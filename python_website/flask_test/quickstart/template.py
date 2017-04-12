#encoding=utf-8
"""
Created on 2016/3/15 14:51
author: iKexinLL
"""

from flask import render_template, Flask

app = Flask(__name__)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name = None):
    #return 'abc'
    #这个 hello.html 寻找同级目录下的tempaltes
    return render_template('hello.html', name = name)

@app.route('/')
def index():
    return 'adf'


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='127.0.0.1', port=4166)