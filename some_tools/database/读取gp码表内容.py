#encoding=utf-8
"""
Created on 2016/8/18 9:50
author: iKexinLL
"""

import psycopg2 as psy
import database.connect_gp as connect_gp
import re
import pandas as pd
import pandas.io.sql as pdsql


conn = connect_gp.Connect()

sql = '''
SELECT   schemaname, tablename    FROM   pg_tables
WHERE   tablename   NOT   LIKE   'pg%'
AND tablename NOT LIKE 'sql_%'
and tablename like 'dim%'
and tablename not like '%external'
ORDER   BY   tablename;
'''

conn.execute(sql)
res = conn.fetchall()



# d_table_name = {}
# with open(r'e:\my_work\bonc\temp\mabiao.txt',encoding = 'utf-8') as f:
#     for lines in f.readlines():
#         en_name,cn_name = lines.split('\t')
#         d_table_name[en_name] = cn_name

sql = '''select * from %s.%s limit 20'''
for r in res:
    #if r[1] in('dim_channel_b', 'dim_channel_his', 'dim_compete_phone'):
        #print(r[1])
        #continue
    try:
        fr = pd.read_sql(sql%(r[0],r[1]), conn.return_conn())
    except pdsql.DatabaseError as e:
    #print(str(Exception))
        print(e)
        continue
    path = r'E:\my_work\bonc\temp_del_anytime\%s.txt'%r[1]
    fr.to_csv(path, index = False, encoding = 'utf-8')





conn.close()

#----------
# 读取文件内容
import os
import pandas as pd

path =r'e:\my_work\bonc\temp'
the_file = []
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('txt') and not file.startswith('ma'):
            the_file.append(path + '\\' + file)


for i in the_file:
    fr = pd.read_csv(i, encoding='utf-8')
    print(fr)
    print('-' * 20 + i)
    a = input()
    if a != 'z':
        continue
    else:
        break
