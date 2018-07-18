#!/usr/bin/python
# coding=utf-8

"""
__time__ = '2018/7/17 15:53'
__author__ = 'Kexin Xu'
__desc__ = 利用queue进行多线程下载的基类
"""

import threading
import queue
import re
import requests
import os


class ThreadDownloadPic(threading.Thread):
    """
    多线程下载类
    1.下载url集合
    2.保存的地址
    3.保存的信息
    """

    def __init__(self, que, img_root_path, file_info, pic_path_info, pic_name_info):
        """
        :param que:需要下载的url集合
        :param file_info:使用字典来保存的文件信息,k为url地址,v为信息
        :param img_root_path:要保存的文件根路径
        :param pic_path_info:图片的路径信息
        :param pic_name_info:图片的名称信息
        :return:
        """
        threading.Thread.__init__(self)
        self.que = que
        self.file_info = file_info
        self.img_root_path = img_root_path
        self.pic_path_info = pic_path_info
        self.pic_name_info = pic_name_info

    def run(self):
        while True:
            try:
                url = self.que.get()
                print(url)

                re_compile = re.compile('\*|\?|"|<|>|\||\u3000')

                # 清除一些没用的和不能使用的标识
                img_save_path = '_'.join(
                                re.sub(re_compile, '_',
                                       self.pic_path_info.get(url) if self.file_info else url).split())

                img_name = '_'.join(
                                re.sub(re_compile, '_',
                                       self.pic_name_info[url]).split())

                temp_path = os.path.join(self.img_root_path, img_save_path, img_name)

                if not os.path.exists(os.path.join(self.img_root_path, img_save_path)):
                    os.makedirs(os.path.join(self.img_root_path, img_save_path))

                if os.path.isfile(temp_path):
                    os.remove(temp_path)

                img_contents = requests.get(url).content
                with open(temp_path, 'wb') as f:
                    f.write(img_contents)

                self.que.task_done()

            except Exception as e:
                print('这里报错?')  # -> 是的
                print('这里报错?\n' + str(e)
                    + 'img_save_path is: ' + str(img_save_path)
                    + '\n' + 'img_name is: ' + str(img_name)
                    + '\n' + 'temp_path is: ' + str(temp_path)
                    + '\n' + 'url is: ' + str(url)
                    + '\n' + '-------------' )
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