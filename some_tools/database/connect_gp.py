#encoding=utf-8
"""
Created on 2016/8/18 10:02
author: iKexinLL
防止没有连接close,导致报警
"""

import psycopg2 as psy
import sys


class Connect(object):
    def __init__(self):

        self.conn = psy.connect(database = 'jlbdbi',
                                host = '10.163.170.33',
                                user = 'chkuser',
                                password = 'C#hkuser29bonc',
                                port = '5432')

        self.cur = self.conn.cursor()

    def execute(self,sql):
        try:
            self.cur.execute(sql)
        except Exception as e:
            self.cur.close()
            self.conn.close()
            print(e)
            sys.exit()

    def fetchall(self):
        try:
            res = self.cur.fetchall()
            return res
        except Exception as e:
            print(e)
            self.cur.close()
            self.conn.close()
            sys.exit()

    def close(self):
        self.cur.close()
        self.conn.close()

    def return_conn(self):
        return self.conn

    def return_cur(self):
        return self.cur