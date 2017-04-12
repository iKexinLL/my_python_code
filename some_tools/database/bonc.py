#encoding=utf-8
"""
Created on 2016/8/7 19:50
author: iKexinLL
尝试用网络找出业务之间的关联性
"""

import networkx as nx


keywords = []
table_names = []

import pandas as pd


fr = pd.read_excel(r'E:\my_work\bonc\吉林移动大数据平台数据模型V1.4.19_2.xlsx')

table_names = fr.实体名
cn_names = fr.表名称

d = dict(zip(table_names,cn_names))

import re 

def get_name(table_name):
    if '.' in table_name:
        p = '\.[A-Z|a-z|_]+'
    else:
        p = '[A-Z|a-z|_]+'
    res = re.findall(p, table_name)
    #print(p)
    #print(res)
    
    if res:
        start_num = 1 if res[0].startswith('.') else None
        end_num = -1 if res[0].endswith('_') else None
        #print(res[0][start_num:end_num])
        return d.get(res[0][start_num:end_num])
    else:
        print('没有匹配表名 ' + table_name)
        return None



