#encoding=utf-8
'''
检查数据库中DWA模式下的表都在哪些DWA过程中出现过
由于只是统计表,所以将所有的表和过程小写
'''

import psycopg2 as psy
import re

#连接GP库
conn = psy.connect(database = '.', host = '.', user = '.', password = '.', port = '.')
cur = conn.cursor()

# 剔除chkuser
sql_get_all_tables = ''' 
select  schemaname||'.'||tablename  as tablename from pg_tables
where schemaname <> 'chkuser';
'''
cur.execute(sql_get_all_tables);
res_get_all_tables = cur.fetchall()

# 获取DWA模式下说有的存储过程
sql_get_all_proc = '''
select distinct p.proname, p.prosrc
from pg_catalog.pg_namespace n
join pg_catalog.pg_proc p
on p.pronamespace = n.oid
where p.proname like 'p_dwa%' -- 这里修改
order by 1'''

cur.execute(sql_get_all_proc)
res_get_all_proc = cur.fetchall()
cur.close()
conn.close()

# 由于这样返回的结果中是带有分区的,比如 XXX_1_prt_.. 所以要处理一下
p_get_real_table = re.compile('_1_prt') #先找 _1_prt 这个

#所有表结果
res_tables = set()
for table in res_get_all_tables:
    partition_loc = re.search(p_get_real_table,table[0])
    if partition_loc:
        res_tables.add(table[0][:partition_loc.span()[0]].lower())
    else:
        res_tables.add(table[0].lower())

d_proc_table = {} # 过程中用到的表
d_table_proc = {} # 表在哪些过程中出现

for table in res_tables:
    d_table_proc[table] = []

#做统计
for proc_info in res_get_all_proc:
    proc_name = proc_info[0].lower()
    proc_content = proc_info[1].lower()
    d_proc_table[proc_name] = []
    for table in res_tables:
        if table in proc_content:
            d_proc_table[proc_name].append(table)
            d_table_proc[table].append(proc_name)
# 写入到文件
with open(r'e:\temp\res_39.txt','w',encoding='utf-8') as f:
    for proc_name,tables in d_proc_table.items():
        for table in tables:
            f.write(proc_name+'\t')
            f.write(table+'\n')

with open(r'e:\temp\res_392.txt','w',encoding='utf-8') as f:
    for table,proc_names in d_table_proc.items():
        if proc_names:
            for proc_name in proc_names:
                f.write(table+'\t') 
                f.write(proc_name+'\n')
        else:
            f.write(table+'\n')

