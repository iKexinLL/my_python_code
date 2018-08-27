#!/usr/bin/python
# coding=utf-8

"""
__time__ = '2018/7/17 15:53'
__author__ = 'Kexin Xu'
__desc__ = 利用queue进行多线程下载的基类
"""

import threading
import re
import requests
import os
import time

class ThreadDownloadPic(threading.Thread):
    """
    多线程下载类
    1.下载url集合
    2.保存的地址
    3.保存的信息
    """

    def __init__(self, que, f_write):
        """
        :param que:需要下载的url集合
        :param que.url:url地址
        :param que.img_path:图片的路径信息
        :param que.img_name:图片的名称信息
        :return:
        """
        threading.Thread.__init__(self)
        self.que = que
        self.f_write = f_write

    def time_sleep(self, secs=0.1):
        time.sleep(secs)

    def f_write_urls(self, url):
        self.f_write.write(url + '\n')

    def run(self):
        while True:
            self.time_sleep()
            try:
                res_d = self.que.get()
                print(res_d['url'])

                # 由于多线程的存在,导致了可能一起创建文件夹
                # 所以给这个步骤加上一个检测
                # 忽略文件创建的错误
                try:
                    if not os.path.exists(res_d['img_path']):
                        os.makedirs(res_d['img_path'])
                except FileExistsError:
                    pass

                if os.path.isfile(res_d['img_name']):
                    os.remove(res_d['img_name'])

                img_contents = requests.get(res_d['url']).content
                with open(res_d['img_name'], 'wb') as f:
                    f.write(img_contents)

                self.f_write_urls(res_d['url'])

            except Exception as e:
                print('这里报错?\n' + str(e)
                    + '\n' + 'img_save_path is: ' + str(res_d['img_path'])
                    + '\n' + 'img_name is: ' + str(res_d['img_name'])
                    + '\n' + 'url is: ' + str(res_d['url'])
                    + '\n' + '-------------')
                    
            finally:
                self.que.task_done()

                # 这个是由于有个图片的最后一个文字是?,导致系统报错
                # 然后这个queue就无法停下来
                # 所以我尝试用sys.exit强行终止这个问题
                # 结果也不好使~
                # 结论:下面这句话没用
                # sys.exit(1)

'''
    for k,v in d_pic.items():
        # 这里要研究一下
        # 将item放入队列中。
        #
        # 如果可选的参数block为True且timeout为空对象（默认的情况，阻塞调用，无超时）。
        # 如果timeout是个正整数，阻塞调用进程最多timeout秒，如果一直无空空间可用，抛出Full异常（带超时的阻塞调用）。
        # 如果block为False，如果有空闲空间可用将数据放入队列，否则立即抛出Full异常
        # que.put(k, block=False, timeout=3)
        que.put(k)

    for i in range(5):
        t = ThreadDownloadPic(que, d_pic, img_save_path)
        t.setDaemon(True)
        t.start()

    que.join()

    print('end')
'''