import re
import os 

path = r'e:\temp\rule.txt'
path_res = r'e:\temp\res.txt'

with open(path, encoding = 'utf-8') as f:
    info = f.readlines()

if os.path.exists(path_res):
  os.remove(path_res)

f = open(path_res,'x', encoding = 'utf-8')
f.close()

p1 = re.compile('<=|>=|=|>|<')
p2 = re.compile(r'\+|-|\*|\\')

# case_when = "coalesce(sum(case when kpi_code = '%s' then kpi_value end),0)"
case_when = "sum(case when kpi_code = '%s' then kpi_value end)"


for i in info:
    sql = ''
    temp_info = re.split(p1, i)
    f_sign = re.findall(p1,i)[0]

    s_zhibiao = re.split(p2, temp_info[0])
    s_sign = re.findall(p2,temp_info[0])

    r_zhibiao = re.split(p2, temp_info[1])
    r_sign = re.findall(p2, temp_info[1])


    # 输出sql
    #sql += 'select \n'
    for m in range(len(s_zhibiao)):
        if m < len(s_zhibiao) - 1 :
            sql += case_when%s_zhibiao[m].replace('\n','') + s_sign[m] + '\n'
        else:
            sql += case_when%s_zhibiao[m].replace('\n','') + '\n'
    sql += f_sign + '\n'
    for n in range(len(r_zhibiao)):
        if n < len(r_zhibiao) - 1:
            sql += case_when%r_zhibiao[n].replace('\n','') + r_sign[n] + '\n'
        else:
            sql += case_when%r_zhibiao[n].replace('\n','') + '\n'
    sql += ',\n'
    #sql += "from dwa.dwa_m_zw_s_fin_cwdb_fee_kpi \n where month_id = '201611' union all\n\n"

    with open(path_res,'a', encoding = 'utf-8') as f:
        f.write(sql)

