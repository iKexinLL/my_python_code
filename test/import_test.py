

import psycopg2 as psy
from psycopg2 import pool as psypool


class ConnectGP(object):

    '''创建连接池'''
    def __init__(self):
        #初始化

        # 连接信息
        minconn = 1 # 最小连接数
        maxconn = 2 # 最大连接数
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
        执行语句用SQL
        '''
        conn = connect_pool.getconn()
        cur = conn.cursor()
        cur.execute(sql)

    def close_all():
        self.connect_pool.close_all()


        

