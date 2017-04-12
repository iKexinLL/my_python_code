# encoding=utf-8
"""
Created on 2016/8/28 21:15
author: iKexinLL
"""

import re

keywords = {'from', 'inner join', 'where', 'and', 'group by', 'on'}
key_re_words = re.compile(r'from\s*\(|inner join|left join|where|and|\)')
last_key_word = ''


# 传入SQL,并将回车替换成空格
def get_sql(sql):
    p = re.compile(r'\n|\t|\s+')
    sql = re.sub(p, ' ', sql)
    # print(sql)

    return sql.split(' ')  # 返回一个列表


# 添加TAB键,并将关键字前加上回车
def sql_revise(sql):
    level = 0
    for i in range(len(sql)):
        # 第一个select直接添加一个TAB
        # if sql[i].lower == 'select' and last_key_word == '':
        #print(sql[i])
        if sql[i] == 'select':
            level += 1
            sql[i] = '\n' + '\t' * level + sql[i]
            sql[i + 1] = '\n' + '\t' * (level + 1) + sql[i + 1]
        # 忽略注释
        elif '--' in sql[i]:
            break
        #elif sql[i].lower() in keywords:
        elif re.findall(key_re_words,sql[i]):
            #print(1)
            sql[i] = '\n' + '\t' * level + sql[i]

    return sql

def t2(sql):
    sql = ' '.join(sql)
    #print(sql)
    #print(type(sql))
    return re.sub(key_re_words,'\n' ,sql)

sql = '''
select
count(DISTINCT a.device_number)
from
(
select
device_number
from dwv.dwv_d_sy_s_second_gprs_accu_1_PRT_M201607_2_PRT_D31
where TOTAL_FLUX > 0
GROUP BY device_number
)a
left JOIN dwv.dwv_m_kh_s_user_wlw_1_prt_p_201607 b
on a.device_number = b.device_number
left join
(
SELECT
count(DISTINCT a.device_number)
FROM
(
SELECT
device_number,
area_id,
city_id,
row_number()over(partition BY user_id
ORDER BY innet_date DESC)rn
FROM dwv.dwv_d_kh_b_user_info_1_prt_M201607_2_PRT_D30 a
INNER JOIN dim.DIM_PD_PRC_DICT b ON b.prod_prcid = a.prod_prcid
WHERE b.prod_prc_name LIKE '%CPE%'
AND substr(b.exp_date,1,6) >='201607'
AND substr(b.eff_date,1,6) <='201607'
AND user_type <> '02'
)a
INNER JOIN
(
SELECT
device_number
FROM dwv.dwv_d_sy_s_second_gprs_accu_1_PRT_M201607_2_PRT_D31
WHERE resv_code4 <> '0'
AND total_flux > 0
GROUP BY device_number
)b
ON b.device_number = a.device_number
AND rn = 1
)c
on a.device_number = c.device_number
where b.device_number is null
and c.device_number is null
'''

res_sql = get_sql(sql)
res_sql2 = ' '.join(sql_revise(res_sql))
#print(res_sql)
print(t2(res_sql))
print(res_sql2)
