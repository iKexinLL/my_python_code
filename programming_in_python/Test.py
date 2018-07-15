#!/usr/bin/python
# coding=utf-8

"""
__time__ = '2018/5/12 15:33'
__author__ = 'Kexin Xu'
"""

import Shape

p = Shape.Point(3, 4)

print(p.print_self_value)

print(p.distance_from_origin())
# -----------------------

before = ["Nonmetals",
          "    Hydrogen",
          "    Carbon",
          "    Nitrogen",
          "    Oxygen",
          "Inner Transitionals",
          "    Lanthanides",
          "        Cerium",
          "        Europium",
          "    Actinides",
          "        Uranium",
          "        Curium",
          "        Plutonium",
          "Alkali Metals",
          "    Lithium",
          "    Sodium",
          "    Potassium"]

import re

p = re.compile("^ *")

space_in_word = 0
temp_dict = {}
level_set = set()

old_level_name = []

def add_child(old_level_name):
    mid_code = []

    for i in old_level_name:
        mid_code.append("['%s']" % i)
    the_code = "temp_dict%s = {}" % ''.join(mid_code)
    print(the_code)
    # context = globals().copy()
    #exec(the_code, context)
    exec(the_code)


for i in before:
    '''
        利用层级关系来确认位置
    '''
    # 计算空格数量
    space_in_word = len(re.findall(p, i)[0])
    # 存储空格数量
    level_set.add(space_in_word)
    # 对空格数量进行排序,并作为层级的依据
    sd_level_set = sorted(level_set)
    # 根据空格数量确认层级
    the_level = sd_level_set.index(space_in_word)
    # the_name = 'level_%d' % space_in_word

    if space_in_word == 0:
        old_level_name = []
        temp_dict.setdefault(i,{})
        old_level_name.append(i)
    else:
        # 删除当前层级的变量
        old_level_name = old_level_name[:the_level]
        # 添加当前的变量
        old_level_name.append(i)
        add_child(old_level_name)
        # temp_dict[old_level_name].setdefault(i, {})

# 利用递归对字典中的变量排序输出
res = []
def sort_dict(temp_dict, key=str.lower):
    mid_sort = sorted(temp_dict, key=key)
    # print(mid_sort)

    for k in mid_sort:
        print('k is ' + k)
        res.append(k)
        sort_dict(temp_dict[k])