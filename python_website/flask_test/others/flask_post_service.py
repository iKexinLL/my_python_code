#encoding=utf-8
"""
Created on 2016/2/24 11:12
author: iKexinLL
"""

import flask

app = flask.Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    kv = flask.request.get_json(force=True)

    print(kv)
    return kv


app.run(host='127.0.0.1', port=4166)

