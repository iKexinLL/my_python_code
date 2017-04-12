#encoding=utf-8
"""
Created on 2016/4/8 17:33
author: iKexinLL
获取元素说明, 在ipython中执行
"""

import requests
from bs4 import BeautifulSoup as bsp
import re


p = re.compile('<|>')

url = 'http://demo.yanue.net/HTML5element/'

rp = requests.get(url)
spp = bsp(rp.text, 'lxml')

li = []

for i in spp.find_all('td'):
    li.append(i)

d = {}
for i in li:
    if 'h3' in str(i):
        name = re.sub(p, '', i.h3.getText())
        description = i.p.getText()
        d[name] = description