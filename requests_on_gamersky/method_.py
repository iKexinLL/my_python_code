#!/usr/bin/python
# coding=utf-8

"""
__time__ = '2018/7/12 18:45'
__author__ = 'Kexin Xu'
__desc__ = ''
"""


url = r'http://www.gamersky.com/ent/201805/1046795_2.shtml'


img_root_path = r'e:\temp\img_save'

import requests
import os
import shutil

from bs4 import BeautifulSoup

# 获取内容
r = requests.get(url)

# 解决中文乱码问题
r.encoding = 'utf-8'

# print(r.text)

soup = BeautifulSoup(r.text,'lxml')

'''
想了一下,还是需要使用find_all('p')的方法
这样,只需判断
p.a.img是否存在
tp_.find_all('a')[-1].text是否为"下一页"就好了
-----------
现在有四种情况,一个网页内:
1.图片下面有说明
2.图片最上方有说明
3.有些图片有说明,有些图面没有说明
4.所有图片无说明
这就需要判断p.text是否存在了
思路就是这样判断,我觉得还是要加上四位序号,这样以后翻起来会方便点
-----------
然后就是多线程的问题了,可以在找机会研究一下
记得注意sleep,别被封了IP
'''