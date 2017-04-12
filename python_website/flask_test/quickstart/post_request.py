#encoding=utf-8
"""
Created on 2016/3/21 11:18
author: iKexinLL
"""

import requests


url = 'http://127.0.0.1:4166/login'
r = requests.put(url, data = 'xukexin')
print(r.content)