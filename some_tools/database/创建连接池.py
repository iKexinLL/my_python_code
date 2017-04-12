'''
    连接池方式,这个方法可以在同一线程内分享连接池
'''

import psycopg2 as psy
from psycopg2 import pool as psypool


class ConnectGP(object):

    '''创建连接池'''
    def __init__(self):
        #初始化

        # 连接信息
        minconn = 1 # 最小连接数
        maxconn = 5 # 最大连接数
        database = 'jlbdbi' 
        host = '10.163.170.33'
        user = 'dwa'
        password = 'D#wa29bonc' 
        port = '5432'

        self.connect_pool = psypool.SimpleConnectionPool(
            minconn,
            maxconn,
            database = database,
            host = host,
            user = user,
            password = password,
            port = port
        )

    def execute(self,sql):
        '''
            执行SQL
        '''
        try:
            conn = connect_pool.getconn()
            cur = conn.cursor()
            cur.execute(sql)
        except Exception as e:
            print(e)
            self.conn.rollback()
            
    def fetchall(self):
        '''
            返回所有的查询结果
        '''
        res = self.cursor.fetchall()
        return self.formatting_result(res)

    def fetchmany(self,size):
        '''
            返回size长度的查询结果
            并不等同于limit, limit为限制数据库的查询个数,
            这个为限制查询结果的个数
        '''
        res = self.cursor.fetchmany(size)
        return self.formatting_result(res)
        

    def close_all():
        self.connect_pool.close_all()

        

