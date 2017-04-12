#encoding=utf-8
"""
Created on 2016/2/25 16:02
author: iKexinLL
"""

from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return 'adf'

@app.route('/login')
def login():
    pass

@app.route('/user/<username>')
def profile(username):
    pass

#url_for('serer', profile='f')

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='XuKexin'))
    #print(url_for('serer'))


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='127.0.0.1', port=4168)