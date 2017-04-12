#encoding=utf-8
"""
Created on 2016/8/5 10:42
author: iKexinLL
"""

import pandas as pd
import collections
import re

path = r'E:\\工作\\东方国信\\多维价值分析系统定报指标比对_汇总.xlsx'
fr = pd.read_excel(path)

p = '[a-z|A-Z]{3}\\.[A-Z|_|\\d]+'

c = []
for i in fr.指标技术口径.dropna().values:
    c.append(re.findall(p, i))


def flatten(input_word): #利用递归返回input中所有的iterable

    for i in input_word:
        if isinstance(i, collections.Iterable) and not isinstance(i, str):
            for sub in flatten(i):
                yield sub
        else:
            yield i


st = set(flatten(c))

#由于SQL中使用的都是表分区,xxx_1_PRT_M201602_2_PRT_D29,所以需要重新弄一下


