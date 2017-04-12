#encoding=utf-8
"""
Created on 2016/4/7 14:22
author: iKexinLL
"""

import requests
from bs4 import BeautifulSoup as bsp
import re
import threading
import queue
import time


init_url = 'http://quotes.money.163.com/data/caibao/zcfzb_ALL.html?reportdate=20141231&sort=publishdate&order=desc&page=%s'
que = queue.Queue()
p = re.compile(r'\r|\n|\t| ')

d = dict(代码 = [], 净资产 = [], 名称 = [],
         总负债 = [], 总资产 = [], 比上期 = [],
         流动负债 = [], 流动资产 = [], 货币资金 = [],
         公告日期 = [])
class ThreadUrl(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.que = que

    def run(self):
        while(True):
            try:
                url = self.que.get()
                print(url)

                r = requests.get(url)
                sp = bsp(r.text, 'lxml')

                info = sp.find_all('tr')
                for data in info[1:]:
                    res = [m.getText() for m in data.find_all('td')]
                    d['代码'].append(res[1])
                    d['名称'].append(res[2])
                    d['总资产'].append(res[3])
                    d['货币资金'].append(res[4])
                    d['流动资产'].append(res[5])
                    d['总负债'].append(res[6])
                    d['流动负债'].append(res[7])
                    d['净资产'].append(res[8])
                    d['比上期'].append(res[9])
                    d['公告日期'].append(re.sub(p, '', res[10]))

                self.que.task_done()

            except Exception as e:
                print(e)



def export_excel(d):
    import pandas as pd

    fr = pd.DataFrame(d,columns=['代码','名称','总资产','货币资金','流动资产','总负债','流动负债','净资产','比上期'])
    wr = pd.ExcelWriter(r'e:\t.xlsx')
    fr.to_excel(wr,index=False)
    wr.close()


def main():
    #url = 'https://www.itjuzi.com/person?page=1'
    init_url = 'http://quotes.money.163.com/data/caibao/zcfzb_ALL.html?reportdate=20141231&sort=publishdate&order=desc&page='

    urls = [init_url + str(i) for i in range(115)]

    for url in urls:
        que.put(url)


    #开启5个线程
    for i in range(5):
        t = ThreadUrl(que)
        t.setDaemon(True)
        t.start()

    que.join()
    print('end')
    #结束进程后将结果输出成excel
    export_excel(d)

print('start')
start = time.time()
main()
print(time.time() - start)















