#!/usr/bin/python
# coding=utf-8

"""
__time__ = '2018/7/3 15:16'
__author__ = 'Kexin Xu'
__desc__ = ''
"""

'''
爬取游民星空中的一些图片
将解说文字放入到文件名称中
-----------------------
情况1. 
    对于page_1,页面最上面会有一段解说
情况2.
    解说文字会在图片下方.
    一段解说文字对应一个图片
情况3.
    一段解说文字对应多个图片
'''

url = r'http://www.gamersky.com/ent/201805/1046795.shtml'
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


# 获取全部图片的网址
# 为了获取其下面的文字,这里先不取网址
all_img = [x for x in soup.find_all('img', 'picact')]

# 获取图片下方的文字
# 并提取img中的src,转换成网址
def get_img_comments(all_img):
    d = {}
    for tag in all_img:
        # 这个并不准确,需要修改
        temp_content = str(tag.next_element.next_element)
        # 删除 \n,\xa0等一些其它标识
        d[tag['src']] = ''.join(temp_content.split()) + os.path.splitext(tag['src'])[1]
    return d

# 下载图片,图片的名称为其值
d_pic = get_img_comments(all_img)

# 判断路径是否存在
assert all_img[0], '图片不存在,无法创建路径'

ts = all_img[0]['src'].split('/')
img_path = os.path.join(img_root_path, ts[3]+ts[4])

# 删除文件夹下的内容
def delete_path_files(path):
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    else:
        os.makedirs(img_path)

delete_path_files(img_path)

for k, v in d_pic.items():
    temp_path = os.path.join(img_path,v)
    img_contents = requests.get(k).content
    with open(temp_path, 'wb') as f:
        f.write(img_contents)

# 关于名称,应该按照页数,第几张,注释 进行命名
# 还存在图片没有注释的情况
# 那么 tag.next_element.next_element 这个就需要进行修改








