import direct_connect as dc
'''
简单点写的话
'''

temp_conn = dc.ConnectGP()

sql = '''
    select 
        month_id, 
        user_id 
    from dwi.DWI_M_KH_USER_SP_ORDER_1_prt_p_{month} limit 5;
    '''.format( month = '201701' )

temp_conn.execute(sql)

res = temp_conn.fetchall()

'''
res的结果如下:
[{'month_id': '201701', 'user_id': '220730200000782356'},
 {'month_id': '201701', 'user_id': '220780200015108870'},
 {'month_id': '201701', 'user_id': '220120200040931230'},
 {'month_id': '201701', 'user_id': '220760200003085693'},
 {'month_id': '201701', 'user_id': '220780200015195872'}]
 '''

 '''
 复杂的话~ 需要再说吧
 '''