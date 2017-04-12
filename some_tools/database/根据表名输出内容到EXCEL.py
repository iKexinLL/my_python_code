#encoding=utf-8
"""
Created on 2016/8/17 9:53
author: iKexinLL
"""

import pandas as pd
import psycopg2 as psy
import re

#查找表名
sql = '''
SELECT   tablename   FROM   pg_tables a
WHERE a.tablename like ('%pd_brand_dict')
    or a.tablename like ('%pd_prod_dict')
    or a.tablename like ('%pd_prodbrand_rel')
    or a.tablename like ('%pd_prc_dict')
    or a.tablename like ('%pd_prc_rel')
    or a.tablename like ('%pd_prcdetail_dict')
    or a.tablename like ('%pd_outprc_rel')
    or a.tablename like ('%pd_prcatter_dict')
    or a.tablename like ('%pd_prcclass_dict')
ORDER   BY   tablename;
'''


conn = psy.connect(database = 'jlbdbi',
				   host = '10.163.170.33',
				   user = 'chkuser',
				   password = 'C#hkuser29bonc',
				   port = '5432')
cur = conn.cursor()



cur.execute(sql)
res = cur.fetchall()

wr = pd.ExcelWriter(r'e:\temp\产品1.xlsx')

p = re.compile('dim_pd.*')
for i in res:
    table = re.findall(p, i[0])
    if table:
        fr = pd.read_sql('select * from dim.%s limit 100'%table[0], conn)
        fr.to_excel(wr, index = False, sheet_name = table[0])

wr.save()

cur.close()
conn.close()

