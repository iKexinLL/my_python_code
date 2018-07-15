#!/usr/bin/python
# coding=utf-8

"""
__time__ = '2018/7/15 10:33'
__author__ = 'Kexin Xu'
__desc__ = 添加一个简单的GUI用于输入网址
"""

import easygui as eg
import re



# 判断 gamersky_url是否为 gamersky/ent/六位数字/一堆数字.shtml

p = re.compile(r'gamersky\.com/ent/\d{6}/\d+\.shtml')

def judge_url():

    gamersky_url = eg.enterbox(msg='输入网址')

    if re.search(p, gamersky_url):
        return gamersky_url
    else:
        raise ValueError("URL地址非gamersky.com\ent有效地址")
