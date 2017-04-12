#encoding=utf-8
"""
Created on 2016/7/20 13:32
author: iKexinLL
找到ipython中的style
"""

path = r'E:\my_work\bonc\gp_function\dwi下的function'

import os

for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.sql') and not file.startswith('__'):
            with open(os.path.join(root, file), encoding = 'gbk') as f:
                for line in f:
                    if 'ods_d_kh_ca' in line.lower():
                        print(os.path.join(root, file))
