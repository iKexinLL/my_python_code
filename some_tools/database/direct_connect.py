'''
直连方式, 这样的结果为每个过程创建一个连接
'''

import psycopg2 as psy
import warnings
import pandas as pd 

class ConnectGP(object):

    def __init__(self):
        '''
        '''
        database = 'jlbdbi' 
        host = '10.163.170.33'
        user = 'dwa'
        password = 'D#wa29bonc' 
        port = '5432'

        self.conn = psy.connect(
            database = database,
            host = host,
            user = user,
            password = password,
            port = port)
        self.cursor = self.conn.cursor()

    def execute(self,sql):
        '''
            执行SQL
        '''
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            self.conn.rollback()

    def pandas_fetchall(self, sql):
        '''
            直接将结果传入到pandas
        '''
        fr = pd.read_sql(sql, self.conn)
        return fr
    
    def write_pandas_result(self, fr, path_out, index=False):
        wr = pd.ExcelWriter(path_out)
        fr.to_excel(wr, path_out, index=index)
        wr.save()

    def fetchall(self, if_format = True):
        '''
            返回所有的查询结果
        '''
        warnings.simplefilter('always', UserWarning)
        res = self.cursor.fetchall()
        self.raise_warning()
        if if_format:
            return self.formatting_result(res) 
        else:
            return res
        
    def fetchmany(self,size):
        '''
            返回size长度的查询结果
            并不等同于limit, limit为限制数据库的查询个数,
            这个为限制查询结果的个数
        '''
        warnings.simplefilter('always', UserWarning)
        res = self.cursor.fetchmany(size)
        self.raise_warning()
        return self.formatting_result(res)
    
    def formatting_result(self, res):
        '''
            格式化数据输出结果
            样式:
                [
                    {'month_id':'201704','user_id':'001'}
                    {'month_id':'201704','user_id':'002'}
                ]
        '''
        formated_res = []
        description = [x[0] for x in self.cursor.description] # 列名

        for data in res:
            formated_res.append(dict(zip(description, data)))
        
        return formated_res

    def close(self):
        '''
            关闭连接语句
            在程序最后必须加这条语句,否则Python会一直占据GP的连接个数
        '''
        self.cursor.close()
        self.conn.close()

    def raise_warning(self):
        warnings.warn('\n do you need close the connect? **.close()?')
