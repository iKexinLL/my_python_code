'''
    1.可以利用 converters = {'District_code': str, 'Code_t': str}
      pd.read_excel(path_one, converters=converters) 将值转换成str,比如 000000 转换成 '000000'
    2. header=0 表示以第一行为columns
    3. 注意字符编码
    4. wr在调用wr.save()之前可以随意写入
'''

path_csv = r'e:\temp\月指标数据.csv'

import pandas as pd
try:
    fr = pd.read_csv(path_csv, encoding='utf-8')
except UnicodeDecodeError:
    fr = pd.read_csv(path_csv, encoding='gbk')


path_excel_output = r'e:\temp\月指标数据.xlsx'
wr = pd.ExcelWriter(path_excel_output)

fr.to_excel(wr, index = False)

wr.save()


