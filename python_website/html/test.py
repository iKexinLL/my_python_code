#encoding=utf-8
"""
Created on 2016/3/22 9:50
author: iKexinLL
"""

from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test_jinja2.html', d = {'a' : 3, 'b': 2}, seq = [1,2,3,4])



if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1', port = 4167)