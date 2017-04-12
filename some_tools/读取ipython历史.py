#encoding=utf-8
"""
Created on 2016/4/1 10:13
author: iKexinLL
根据Ipython.core.history中的方法进行读取
"""

import sqlite3
path = r'C:\Users\kongp\.ipython\profile_default\history.sqlite'

db = sqlite3.connect(path)
# DB.EXECUTE("""CREATE TABLE IF NOT EXISTS OUTPUT_HISTORY
#                         (SESSION INTEGER, LINE INTEGER, OUTPUT TEXT,
#                         PRIMARY KEY (SESSION, LINE))""")
# DB.EXECUTE("""CREATE TABLE IF NOT EXISTS HISTORY
#                 (SESSION INTEGER, LINE INTEGER, SOURCE TEXT, SOURCE_RAW TEXT,
#                 PRIMARY KEY (SESSION, LINE))""")
# DB.EXECUTE('''CREATE TABLE IF NOT EXISTS SESSIONS (SESSION INTEGER
#                         PRIMARY KEY AUTOINCREMENT, START TIMESTAMP,
#                         END TIMESTAMP, NUM_CMDS INTEGER, REMARK TEXT)''')



cur = db.execute('select session integer, line integer, source text from history')
with open(r'e:/ipython_history.py','w', encoding = 'utf-8') as f:
    for i in cur:
        for c in i:
            if not isinstance(c, str):
                f.write(str(c))
                f.write(str(', '))
            else:
                f.write(c)
        f.write('\n')