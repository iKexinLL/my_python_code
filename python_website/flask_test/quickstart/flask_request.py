#encoding=utf-8
"""
Created on 2016/3/21 11:06
author: iKexinLL
"""

from flask import request
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/login', methods = ['POST'])
def login():
    print(request.method)
    error = None
    if request.method == 'POST':
        r = request.get_data()
        print(r)
        return r

    else:
        error('Error')

    return render_template('login.html', error = error)


@app.route('/', methods = ['POST'])
def index():
    return request.get_data()


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='127.0.0.1', port=4166)