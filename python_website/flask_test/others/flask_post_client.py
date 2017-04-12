#encoding=utf-8
"""
Created on 2016/2/24 11:06
author: iKexinLL
"""

import urllib
import json
import requests

json_data = json.dumps(['a:b'])

url = 'http://127.0.0.1:4166/'\

res = requests.post(url, json=json_data)

print(res)
