#encoding=utf-8
"""
Created on 2016/4/8 16:42
author: iKexinLL
"""
from flask import render_template, Flask

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def index(name = None):
    return render_template('test_one.html', name = name)


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='127.0.0.1', port=4166)