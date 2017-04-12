#encoding=utf-8
"""
Created on 2016/3/8 16:18
author: iKexinLL
"""

import json
import pandas as pd
import numpy as np
import sys


class CJsonEncoder(json.JSONEncoder):
    """
    #格式化对象中的int为字符串
    #默认情况下,有些 数字无法正常解析
    """
    def default(self, obj):
        if isinstance(obj,int):
            return int(obj)
        elif isinstance(obj, np.int64):
            return int(obj)
        else:
            return json.JSONEncoder.default(obj)

def calc_data(province,fr, data_2012):
    data_in = fr.query("district_code == '%s'"%province)

    data_in_code = set(data_in.code_t)

    for i in data_2012:
        if i['code'] in data_in_code:
            info = data_in.ix[data_in.code_t == i['code']]
            i.update({'rca':info.RCA.values[0], 'value':info.usd.values[0]})

    #print(len(data_2012))
    #json_simple = [{'app_type':'casy'},{'item_type':'hs4'},{'title':'test'},{'year':'2012'},{'data':json_data['data']}]
    path_json_simple = r'E:\result\进出口\result2\2012_in_%s.json'
    with open(path_json_simple%province, 'w') as f:
        json.dump(data_2012,f,cls=CJsonEncoder)



f = lambda x: '{0:0>4}'.format(x)
converter = {'district_code': str, 'code_t': f}

#读取自身的数据
path_rca = r'E:\result\进出口\df_rca_进口.csv'

fr = pd.read_csv(path_rca, converters = converter)

code_in = set(fr.code_t)


#读取网上模版数据
path = r'E:\工作\产业森林\2014.json'
with open(path) as f:
    json_data = json.loads(f.read())

attr = json_data['attr']

code_out = set(['{0:0>4}'.format(v['code']) for k,v in attr.items()])

code_joint = code_out.intersection(code_in)

#然后开始替换
country1 = {'name_3char': 'CHN', 'name': 'China'}
#替换data中的rca, value, year
#其中 year 删除除2012外的数据, 并在2012的数据中进行替换
data = json_data['data']
data_2012 = [x for x in data if x['year'] == 2012]
#json_data['data'] = data_2012

f = lambda x: x.update({'rca':0,'value':0})
set(map(f,data_2012))

#获取省份
provinces =  set(fr.district_code)

for province in provinces:
    try:
        print(province)
        calc_data(province, fr, data_2012)
    except Exception as e:
        print(e)
        sys.exit(0)























