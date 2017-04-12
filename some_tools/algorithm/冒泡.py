#encoding=utf-8
"""
Created on 2016/4/12 11:28
author: iKexinLL
"""


li = [1, 7, 8, 2, 9, 6, 5, 10, 4, 3]


#从大到小
for i in range(len(li)):
    for j in range(i + 1, len(li)):
        if li[i] < li[j]:
            li[i], li[j] = li[j], li[i]


#从小到大
for i in range(len(li)):
    for j in range(i + 1, len(li)):
        if li[i] > li[j]:
            li[i], li[j] = li[j], li[i]