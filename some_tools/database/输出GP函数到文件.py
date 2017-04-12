#encoding=utf-8
"""
Created on 2016/8/5 13:10
author: iKexinLL
"""


import psycopg2 as psy
import os
import datetime
import shutil

the_date = datetime.datetime.now().strftime('%Y%m%d')

out_path = r'E:\my_work\工作\定报\备份\gp_function_%s'%the_date

if os.path.isdir(out_path):
    shutil.rmtree(out_path)
os.makedirs(out_path)

#GP库
conn = psy.connect(database = 'jlbdbi', host = '10.163.170.33', user = 'dwa', password = 'D#wa29bonc', port = '5432')
#hawq库
#conn = psy.connect(database = 'jlbdbi', host = '10.161.4.169', user = 'chkuser', password = '1qaz!QAZ', port = '10432')
# conn = psy.connect(database = 'jlbdbi',
# 				   host = '10.163.170.33',
# 				   user = 'chkuser',
# 				   password = 'C#hkuser29bonc',
# 				   port = '5432')
cur = conn.cursor()

# 查询函数的详细内容 select prosrc from pg_proc 
#                    where proname = 'p_stg_d_cs_userrel_info_dmospmsg'
# 查询函数名称         select distinct p.proname 
#                      from pg_catalog.pg_namespace n 
#                      join pg_catalog.pg_proc p 
#                      on p.pronamespace = n.oid order by 1

sql = '''
select distinct p.proname, p.prosrc
from pg_catalog.pg_namespace n
join pg_catalog.pg_proc p
on p.pronamespace = n.oid
where p.proname like 'p_dwa%' -- 这里修改
order by 1'''

# sql = '''
# SELECT   schemaname, tablename    FROM   pg_tables
# WHERE   tablename   NOT   LIKE   'pg%'
# AND tablename NOT LIKE 'sql_%'
# and tablename like 'dim%'
# and tablename not like '%external'
# ORDER   BY   tablename;
# '''

cur.execute(sql)
res = cur.fetchall()
cur.close()
conn.close()

for r in res:
    #cur.execute('select * from %s.%s limit 10 '%(r[0],res[1]))
    with open(r'%(out_path)s\%(file_name)s.sql'%{'out_path':out_path,'file_name':r[0]}, 'w',encoding='utf-8') as f:
        f.write(r[1])


print('end')