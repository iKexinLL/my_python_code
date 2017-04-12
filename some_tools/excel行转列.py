'''
这个是专门输出<产品维--亚信数据>的脚本
只针对表四
'''

# ~!!!! 确定 月份
month_id = '201611'

'''
第三列
'''
head_columns = '''手机上网			数据卡			飞信（对端号：12520/161）			139邮箱（对端号：10658139）			无线音乐（对端号：12530）			手机报			和阅读（对端号：10658080）			和游戏			和视频			和动漫			和包（支付）			手机电视			12580			农信通			BLACKBERRY(个人版)			和通讯录			移动MM			和地图			和视界			12590（语音杂志）			12585			和工作			和包（NFC）			车务通		'''.split()

'''
第二列
'''
head_rows = '''PE-42 	GPRS上网-省内
PE-43 	GPRS上网-省际漫游出访
PE-44 	GPRS上网-省际漫游来访
PE-45 	GPRS上网-国际漫游出访
PE-46 	GPRS上网-国际漫游来访
PE-64 	平台短信-上行
PE-65 	平台短信-下行
PE-68 	梦网彩信-上行
PE-69 	梦网彩信-下行
PE-72 	平台彩信-上行
PE-73 	平台彩信-下行
PE-81 	梦网短信-上行
PE-82 	梦网短信-下行'''.split('\n')
#读取整理好的数据
path = r'E:\my_work\工作\database_result\产品维_亚信整理后结果.txt'

with open(path, encoding = 'utf-8') as f:
    tp = f.read().split('\n')

#然后对读取的数据进行分割
head_data = []

for head_col_num in range(len(head_columns)):
    for head_row_num in range(len(head_rows)):
        head_data.append(head_rows[head_row_num] + '\t' 
                            + head_columns[head_col_num] + '\t' 
                            + tp[head_row_num].split()[head_col_num * 3])

# 将结果输出到Excel

import pandas as pd


fr = pd.DataFrame([x.split('\t') for x in head_data],columns=['code','code_name','code_type','value'])
wr = pd.ExcelWriter(r'e:\temp\产品维_亚信结果总表.xlsx')
fr.to_excel(wr, index=False, columns=None)
wr.save()

# 在数据库中读取表4

# import database.direct_connect as dc 
import sys
sys.path.append(r'E:\code\python\some_tools\database')
import direct_connect as dc

conn = dc.ConnectGP()

sql = ''' select * from DWA_M_RPT_A_NONVOICE_PE_BUSI
		  where acct_date = '%s' and nonvoice_pe_type = '总'
		  order by 2  limit 20 ; ''' % month_id

conn.execute(sql)
print('--查询完毕--输出中---')

mid_res = conn.fetchall(if_format=False)
res = [x[5:] for x in mid_res]

conn.close()

# 将结果进行输出
head_database_data = []


for head_col_num in range(len(head_columns)):
    for head_row_num in range(len(head_rows)):
        final_data = res[head_row_num][head_col_num * 2]
        head_database_data.append(final_data if final_data else 0)
