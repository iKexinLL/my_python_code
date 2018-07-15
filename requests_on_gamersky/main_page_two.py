#!/usr/bin/python
# coding=utf-8

"""
__time__ = '2018/7/13 10:06'
__author__ = 'Kexin Xu'
__desc__ = ''
"""


import requests
import os
import shutil

from bs4 import BeautifulSoup

WEB_ENCODING = 'utf-8'

def get_soup(url, encoding):
    r = requests.get(url)
    # 解决中文乱码问题
    r.encoding = 'utf-8'
    # 剔除\n,方便使用next方法
    soup = BeautifulSoup(r.text.replace('\n',''), 'lxml')
    return soup


def get_url_and_file_name(soup):
    '''
    获取当前网页的所有<p>元素
    对以下情况进行判断

    现在有四种情况,一个网页内:
    1.图片下面有说明
    2.所有图片最上方有说明,下方无说明
    3.有些图片有说明,有些图面没有说明
    4.所有图片无说明
    这就需要判断p.text是否存在了
    思路就是这样判断,我觉得还是要加上四位序号,这样以后翻起来会方便点

    :param soup: 获取的html存储
    :return: 一个字典,存储了图片地址以及图片名称
    '''
    all_p = soup.find_all('p')
    d = {}
    h = lambda x: str(x) if int(x) > 9 else '0' + str(x)

    # 情况2,当有图片没有说明时,且第一个p仅为文字时使用
    upper_title = ''
    if all_p[0].text != '' and not all_p[0].img:
        upper_title = all_p[0].text

    # 确认当前图片是第几页
    pic_page = soup.find('div','page_css').b.text

    # 确认当前图片是第几个
    pic_num = 0

    for temp_p in all_p:

        pic_num += 1

        pre_name = h(pic_page) + h(pic_num)

        if upper_title != '':
            pre_name += '_' + upper_title
        # 情况1 图片下面有说明
        # p.text存在且p.img存在
        if temp_p.img:
            if temp_p.text != '':
                # 删除 \n,\xa0等一些其它标识
                mid_name = pre_name + '_' + ''.join(temp_p.text.split())
            # 情况3,4
            # p.text不存在且p.img存在
            elif temp_p.text == '':
                mid_name = pre_name

            mid_url = temp_p.img['src']
            d[mid_name] = mid_url

    return d

















