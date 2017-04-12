#encoding=utf-8
"""
Created on 2016/3/10 22:16
author: iKexinLL
"""
import sqlparse
import collections


def flatten(input): #利用递归返回input中所有的iterable
    for i in input:
        if isinstance(i, collections.Iterable) and not isinstance(i,str):
            for sub in flatten(i):
                yield sub
        else:
            yield i


lt = ['aa',['bb','cc']]


''.join(flatten(lt)) #aabbccrc


def tslow(li): #模拟 collections.Counter, 但效率差很多
    d = {}
    for i in li:
        try:
            d[i] += 1
        except Exception:
            d[i] = 0

    return d


def tfast(li): #模拟 collections.Counter, 但效率差很多
    d = {}
    for i in li:
        d[i] = d.get(i,0) + 1
    return d


#
def count(input):
    sites = {}




#统计行数
path = '...'
with open(path) as f:
    for lineno, line in enumerate(f):
        pass
    print(lineno)

































