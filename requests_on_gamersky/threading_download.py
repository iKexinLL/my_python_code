#!/usr/bin/python
# coding=utf-8

"""
__time__ = '2018/7/13 15:07'
__author__ = 'Kexin Xu'
__desc__ = 利用threading以及queue进行多线程下载

"""

import threading
import queue
import time
import requests
import os
import re
from bs4 import BeautifulSoup

import gui_for_download


class ThreadUrl(threading.Thread):

    def __init__(self, que, d_pic, img_save_path):
        threading.Thread.__init__(self)
        self.que = que
        self.d_pic = d_pic
        self.img_save_path = img_save_path

    def run(self):
        while (True):
            try:
                url = self.que.get()
                print(url)

                temp_path = os.path.join(self.img_save_path, self.d_pic[url])
                img_contents = requests.get(url).content
                with open(temp_path, 'wb') as f:
                    f.write(img_contents)

                self.que.task_done()

            except Exception as e:
                print('这里报错?') # -> 是的
                print(e)
                # 这个是由于有个图片的最后一个文字是?,导致系统报错
                # 然后这个queue就无法停下来
                # 所以我尝试用sys.exit强行终止这个问题
                # 结果也不好使~
                # 结论:下面这句话没用
                # sys.exit(1)


def get_soup(url, encoding='utf-8'):
    r = requests.get(url)
    # 解决中文乱码问题
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text.replace('\n', ''), 'lxml')
    return soup


def get_url_and_file_name(soup, url_pages):
    '''
    获取当前网页的所有<p>元素
    对以下情况进行判断

    现在有四种情况,一个网页内:
    1.图片下面有说明
    2.所有图片最上方有说明,下方无说明
    3.有些图片有说明,有些图面没有说明
    4.所有图片无说明
    这就需要判断p.text是否存在了
    思路就是这样判断,我觉得还是要加上四位序号,这样以后翻起来会方便点

    对于第一页,需要特殊处理,因为第一页中往往存在一个顶置的整体说明

    :param soup: 获取的html存储
    :return: 一个字典,存储了图片地址以及图片名称
    '''
    # 用于替换windows文件名称中的违规字符
    re_compile = '\*|\?|"|<|>|\||\u3000'

    all_p = soup.find_all('p')
    d = {}
    h = lambda x: str(x) if int(x) > 9 else '0' + str(x)

    # 这么判断对于 http://www.gamersky.com/ent/201807/1072244.shtml 无效
    # 所以修改为用soup判断
    if soup.find('div', 'page_css'):
        if soup.find('div', 'page_css').find_all('a')[-1].text == '下一页':
            url_pages.append(soup.find('div', 'page_css').find_all('a')[-1]['href'])

    # 情况2,当有图片没有说明时,且第一个p仅为文字时使用
    upper_title = ''
    if all_p[0].text != '' and not all_p[0].img:
        upper_title = all_p[0].text

    # 确认当前图片是第几页
    pic_page = soup.find('div', 'page_css').b.text

    # 确认当前图片是第几个
    pic_num = 0

    for temp_p in all_p:

        pic_num += 1

        pre_name = h(pic_page) + h(pic_num)

        if upper_title != '' and pic_page != '1':
            pre_name += '_' + upper_title
        # 情况1 图片下面有说明
        # p.text存在且p.img存在
        if temp_p.img:
            if temp_p.text != '':
                # 删除 \n,\xa0等一些其它标识
                mid_name = pre_name + '_' + ''.join(temp_p.text.split())
            # 情况3,4
            # p.text不存在且p.img存在
            elif temp_p.text == '':
                mid_name = pre_name

            mid_url = temp_p.img['src']
            mid_suffix = temp_p.img['src'].rsplit('.', 1)[-1]
            d[mid_url] = re.sub(re_compile, '', mid_name) + '.' + mid_suffix

    return d


def delete_path_files(path):
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    else:
        os.makedirs(path)


def main():
    WEB_ENCODING = 'utf-8'
    que = queue.Queue()

    d_pic = {}

    # first_url = r'http://www.gamersky.com/ent/201805/1046795.shtml'
    first_url = r'http://www.gamersky.com/ent/201807/1072380.shtml'

    first_url = gui_for_download.judge_url()

    root_save_path = r'e:\temp\img_save'
    img_save_path = os.path.join(root_save_path,
                                 '_'.join(first_url.rsplit('.', 1)[0].split('/')[3:6]))

    url_pages = [first_url]

    delete_path_files(img_save_path)

    for url in url_pages:
        soup = get_soup(url)
        d_pic.update(get_url_and_file_name(soup, url_pages))

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
        t = ThreadUrl(que, d_pic, img_save_path)
        t.setDaemon(True)
        t.start()

    que.join()

    print('end')


if __name__ == '__main__':
    print('start')
    start = time.time()
    main()
    print(time.time() - start)

# for k, v in d_pic.items():
#     temp_path = os.path.join(img_save_path,v)
#     img_contents = requests.get(k).content
#     with open(temp_path, 'wb') as f:
#         f.write(img_contents)
