#encoding=utf-8
"""
Created on 2016/3/28 8:59
author: iKexinLL
测试python对于文件的处理能力
原始文件:  E:\data\2010分省行业互投.csv  2.53MB
生成文件:  E:\data\test_file.csv
循环 2000次,  4.95G
循环 10000次, 24G
"""

import pandas as pd

path_in = 'E:\\data\\2010分省行业互投.csv'
path_out = r'E:\data\test_file.csv'

f = open(path_in)

#data_f = iter(f.readlines())
columns = f.readlines(1)

data = f.read()

f.close()

with open(path_out,'a') as f:
    for i in columns[0]:
        f.write(i)

    for i in range(10000):
        f.write(data)



#按照下面提供的方法读取数据
#http://www.open-open.com/lib/view/open1424831028171.html

reader = pd.read_csv(path_out, sep = '\t', iterator=True)
#这个耗时 57.6s
try:
    #--->我说的~ 这个只跑了 100000000 条数据
    #所以还是要用下面的方法读取全部数据
    df = reader.get_chunk(100000000)
except StopIteration:
    print ("Iteration is stopped.")


#读取全部数据需要三分
##这个竟然跑了三分钟?!!,可能还需要进行一些测试,
#windows的磁盘100%真是个很大问题,
#在跑数的时候,什么都没法做
reader = pd.read_csv(path_out, sep = '\t', iterator=True)
loop = True
chunkSize = 100000
chunks = []
while loop:
    try:
        chunk = reader.get_chunk(chunkSize)
        chunks.append(chunk)
    except StopIteration:
        loop = False
        print ("Iteration is stopped.")
df = pd.concat(chunks, ignore_index=True)