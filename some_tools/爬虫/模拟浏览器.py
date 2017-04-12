#encoding=utf-8
'''
Created on 2016年1月14日 上午9:32:38

@author: iKexinLL
'''
import requests
from bs4 import BeautifulSoup as bsp
import re
import threading
import queue
import time
import sys

'''
爬取 www.sanban18.com,
获取 代码,简称,全称,高管姓名,性别,出生日期,职务
由于这个网站使用的是 ajax 动态写入 数据,所以直接 用 requests 读取只能读取前30条数据
经过查找, 决定使用  selenium 进行浏览器模拟登陆,获取每个页面的code,并将每家公司的 代码存入到列表中
'''
from selenium import webdriver

class spider_sanban18(object):
    def __init__(self):
        self.url = 'http://www.sanban18.com/stock/marketing.html?sortField=updnratio&sortType=desc#'
        chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
        self.browser = webdriver.Chrome(executable_path=chrome_path)
        self.set_id = set()

    def get_browser(self,):
        return self.browser.get(self.url)

    def get_id(self):
        try:
            print('get_id')
            t = self.browser.find_elements_by_tag_name('td') #获取 td下的内容
            for k,v in enumerate(t):
                if (k-1) % 15 == 0:
                    self.set_id.add(v.text)

        except Exception as e:
            print(e)
            self.close_browser()

    def click_next_page(self,i):
        try:
            if i < 183:
                next_page = self.browser.find_element_by_link_text('下一页')
                next_page.click()
            else:
                print('无下一页')
        except Exception as e:
            print(e)
            self.close_browser()

    def close_browser(self):
        #self.browser.close()
        #self.browser.quit()
        #sys.exit()
        pass

    def main(self):
        print('第一页')
        self.get_browser()
        self.get_id()
        for i in range(2,183):
            print('点击下一页')
            self.click_next_page(i)
            print('第' + str(i) + '页')
            time.sleep(0.2)
            self.get_id()

        #self.close_browser()
        print(len(self.set_id))
        return self.set_id

p_entname = re.compile(r'"COMPNAME":".*?"', re.UNICODE)

#===============================================================================
#   def get_info(sid):
#       for i in sid:
#           #这里要多线程考虑了
#           url_ent_name = 'http://www.sanban18.com/stock/'+i+'/profile.html'
#           managers = 'http://www.sanban18.com/stock/'+i+'/management.html'
#
#           r = requests.get(url_ent_name)
#           entname = re.findall(p_entname,r.text)[0].split(':')[1][1:-1].
#===============================================================================s



if __name__ == '__main__':
    sid = spider_sanban18().main()
    #至此 已经获取了每家企业的代码
    #已经保存到 E:\工作\新三板企业代码.txt
    #那么 接下来就开始解析 每家企业的 公司概况  和  管理层



#===============================================================================
#
#   #创建队列
#   que = queue.Queue()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#   d = {'index':[],'name':[],'ent':[],'position':[],'intro':[],'start_exprience':[],'work':[],
#   'edu':[],'partner':[]}
#   failed_url = []
#   p = re.compile('\n|\t')
#   num = 0
#   #创建多线程的类
#   class ThreadUrl(threading.Thread):
#       def __init__(self,que):
#           #初始化父类thread
#           threading.Thread.__init__(self)
#           self.que = que
#
#       def run(self):
#           #重写run方法,进行队列分管
#           global num
#           while(True):
#               try:
#                   url = self.que.get()
#                   r = requests.get(url)
#                   sp = bsp(r.text,'lxml')
#                   #开始解析 html 文档
#                   for person in sp.find_all('b','title'):
#
#                       name = person.a.get_text()
#                       personal_url = person.a.get('href')
#
#                       info = person.nextSibling.nextSibling.get_text().split('·')
#                       #ent = info[0]  position = info[1]
#                       #开始解析 个人网页,提取 简介,创业经历,工作经历
#                       rp = requests.get(personal_url)
#                       spp = bsp(rp.text,'lxml')
#
#                       person_info = spp.find_all('div','sec')
#
#                       intro = re.sub(p,'',person_info[0].find('div','block block-v').get_text())
#                       start_ent = [x.get_text() for x in person_info[1].find_all('span','long')]
#                       work = [re.sub(p,'',x.get_text()) for x in person_info[2].find_all('span','right')]
#                       edu = [re.sub(p,'',x.get_text()) for x in person_info[3].find_all('span','right')]
#                       partner = [x.get_text().split('·')[0] for x in person_info[4].find_all('span','right')]
#
#                       print(num)
#                       num += 1
#                       d['index'].append(str(num))
#                       d['name'].append(str(name))
#                       d['ent'].append(str(info[0]))
#                       d['position'].append(str(info[1]))
#                       d['intro'].append(str(intro))
#                       d['start_exprience'].append(str(start_ent))
#                       d['work'].append(str(work))
#                       d['edu'].append(str(edu))
#                       d['partner'].append(str(partner))
#
#               except Exception as e:
#                   print(e)
#                   failed_url.append((url,e))
#
#
#
#               self.que.task_done()
#
#   def export_excel(d):
#       import pandas as pd
#       fr = pd.DataFrame(d,columns=['index','name','ent','position','intro','start_exprience','edu','partner'])
#       wr = pd.ExcelWriter(r'e:\t.xlsx')
#       fr.to_excel(wr,index=False)
#       wr.close()
#
#
#   def main():
#       #url = 'https://www.itjuzi.com/person?page=1'
#       url = 'https://www.itjuzi.com/person?page='
#       urls = [url + str(i) for i in range(1,1197)]
#       for url in urls:
#           que.put(url)
#
#       #开启5个线程 32个 35.264086961746216
#       for i in range(5):
#           t = ThreadUrl(que)
#           t.setDaemon(True)
#           t.start()
#
#       que.join()
#       print('end')
#       #结束进程后将结果输出成excel
#       export_excel(d)
#
#   start = time.time()
#   main()
#   print(time.time() - start)
#
#
#
#===============================================================================









#===============================================================================
#   num = 0
#   urls = [url + str(i) for i in range(1,82)]
#   p = re.compile('\n|\t','')
#   d = {'index':[],'name':[],'ent':[],'position':[],'intro':[],'start_ent':[],'work':[],
#   'edu':[],'partner':[]}
#===============================================================================





























