#!/usr/bin/python
# coding=utf-8

"""
__time__ = '2018/7/15 11:01'
__author__ = 'Kexin Xu'
__desc__ = 获取 http://www.gamersky.com/ent/xz/ 中(游民福利)的网页链接
        这个有很多,为了避免重复下载,所以对于下载过的网站进行存储
        -------------
"""
import os
import queue
import requests
from bs4 import BeautifulSoup
# 添加sleep,简单的尝试别被封锁
import time


def time_sleep(secs=0.1):
    time.sleep(secs)


DOWNLOAD_PAGES = 15
root_url = r'http://www.gamersky.com/ent/xz/'
IF_USE_PORTABLE_DISK = False
FLAG_URL_FILE_NAME = 'downloaded_url.txt'
IMG_FORMATS = ['GIF', 'JPG', 'PNG', 'BMP', 'JPEG']
KNOWN_URLS_FILE_NAME = 'known_urls.txt'


# def delete_path_files(path):
#     if os.path.exists(path):
#         for root, dirs, files in os.walk(path, topdown=False):
#             for name in files:
#                 os.remove(os.path.join(root, name))
#             for name in dirs:
#                 os.rmdir(os.path.join(root, name))
#     else:
#         os.makedirs(path)


def judge_wd():
    import wmi

    SoftName = 'WD Unlocker'
    # theSoftPath = ''
    theSoftName = 'WD Drive Unlock.exe'
    # DiskName = 'My Passport'

    wmiServer = wmi.WMI()

    LogicalDisk = wmiServer.Win32_LogicalDisk()

    for ld in LogicalDisk:
        if ld.VolumeName == SoftName:
            theSoftPath = ld.Caption + '\\' + theSoftName
            os.system('"' + theSoftPath + '"')
            return True


def folder_path_handle(if_use_portable_disk=IF_USE_PORTABLE_DISK, path=''):
    """
    用一个文件存储下载过的网址,为了避免文件被删,尝试将文件作为隐藏文件放入到文件夹内
    预计图片较多,所以把图片放入到移动硬盘中吧.

    文件夹路径判断
    1. 判断我的硬盘是否存在判断WD程序是否已经运行
        只对我自己能用...
    :return:
    """
    if if_use_portable_disk:
        folder_root_path = r'X:\杂乱文件\gamersky_xz'
        assert judge_wd(), '移动硬盘不存在,请插入硬盘'
    else:
        folder_root_path = r'e:\temp\img_save\gamersky_xz'

    file_flag_path = os.path.join(folder_root_path, FLAG_URL_FILE_NAME)

    # 如果文件夹不存在,则创建文件夹
    if not os.path.isdir(folder_root_path):
        os.makedirs(folder_root_path)

    # 如果当前文件不存在,则创建文件
    if not os.path.isfile(file_flag_path):
        # windows上,python没有os.mknod
        # os.mknod(os.path.join(file_root_path, FLAG_URL_FILE_NAME))
        with open(file_flag_path, 'w', encoding='utf-8') as f:
            f.close()

            # 设置文件属性为隐藏
            # import win32con, win32api
            # win32api.SetFileAttributes(file_root_path, win32con.FILE_ATTRIBUTE_HIDDEN)

    return path if path else folder_root_path


def get_soup(url, encoding='utf-8'):
    r = requests.get(url)
    # 解决中文乱码问题
    r.encoding = encoding
    soup = BeautifulSoup(r.text.replace('\n', ''), 'lxml')
    return soup


def get_file_for_downloaded_urls():
    """
    只下载201703之后的图片地址
    :return:
    """
    file_root_path = folder_path_handle(if_use_portable_disk=IF_USE_PORTABLE_DISK)

    file_downloaded_urls = set()

    with open(os.path.join(file_root_path, FLAG_URL_FILE_NAME), encoding='utf-8') as f:
        for line in f.readlines():
            file_downloaded_urls.add(line.replace('\n', ''))

    return file_downloaded_urls


def get_forthcoming_urls(download_page=5):
    """
    :return:
    :param download_page: 点击多少次"下一页",或者说下载几个页面的数据
    :return:
    """

    # 已下载的urls
    print('获取已下载的url')
    downloaded_urls = get_file_for_downloaded_urls()

    # 在root_url上所获取的所有下载网址
    print('获取gamersky上的url')
    mid_urls = SpiderGamersky.get_all_forthcoming_urls(download_page)

    print('开始对比...')
    forthcoming_urls = mid_urls.difference(downloaded_urls)

    print('对比结果为: ' + str(len(forthcoming_urls)) + '个网址需要获取图片')
    return forthcoming_urls


def get_url_and_file_info(soup, url_pages):
    """
    仅需要第一个<p>作为说明,剩余文字忽略,只下载图片
    :param url_pages:
    :param soup: 获取的html存储
    :return: 一个字典,存储了图片地址以及图片名称
    """
    # 用于替换windows文件名称中的违规字符
    # re_compile = '\*|\?|"|<|>|\||\u3000'

    all_p = soup.find_all('p')
    d = {}
    h = lambda x: str(x) if int(x) > 9 else '0' + str(x)

    # 获取下个网址
    # 对于只有一页的网址来说,不存在soup.find('div', 'page_css').b.text
    # 所以需要先进行判断
    if soup.find('div', 'page_css'):
        if soup.find('div', 'page_css').find_all('a')[-1].text == '下一页':
            url_pages.append(soup.find('div', 'page_css').find_all('a')[-1]['href'])

        # 确认当前图片是第几页
        pic_page = soup.find('div', 'page_css').b.text
    else:
        pic_page = '01'

    # 确认当前图片是第几页
    # 对于只有一页的网址来说,不存在soup.find('div', 'page_css').b.text
    # 所以需要先进行判断
    # if soup.find('div', 'page_css'):
    #     pic_page = soup.find('div', 'page_css').b.text
    # else:
    #     pic_page = '01'

    # 确认当前图片是第几个
    pic_num = 0

    if soup.find('div', 'Mid2L_tit'):
        pic_title = soup.find('div', 'Mid2L_tit').h1.text
    else:
        pic_title = '错误的title: ' + str(pic_num)
    # pic_txt = ''

    for p_num, temp_p in enumerate(all_p):

        if pic_page == '1' and p_num == 0:
            pic_txt = ''.join(temp_p.text.split())
            d['pic_txt'] = pic_txt
            d['pic_title'] = pic_title

        elif temp_p.img:
            pic_num += 1
            pic_format = temp_p.img['src'].rsplit('.', 1)[-1]
            if pic_format in IMG_FORMATS:
                pic_name = h(pic_page) + h(pic_num) + '.' + pic_format
            else:
                pic_name = h(pic_page) + h(pic_num) + '.' + 'jpg'

            mid_url = temp_p.img['src']

            d[mid_url] = pic_name

    return d


def main():
    # 获取要下载的url
    pic_info = {}
    pic_path_info = {}
    pic_name_info = {}
    file_root_path = folder_path_handle(if_use_portable_disk=IF_USE_PORTABLE_DISK)
    forthcoming_urls = get_forthcoming_urls(DOWNLOAD_PAGES)

    print('开始下载图片信息')
    # 20180720记录
    # 201503之前的图片好多都已经挂掉了
    # 所以直接就忽略吧~
    for forthcoming_url in forthcoming_urls:
        url_pages = [forthcoming_url]
        time_sleep()
        pic_info[forthcoming_url] = {}
        for url in url_pages:
            soup = get_soup(url)
            print('forthcoming url is ' + url)
            pic_info[forthcoming_url].update(get_url_and_file_info(soup, url_pages))

    print('图片信息下载完毕')

    que = queue.Queue()

    # 添加已获取的图片地址
    with open(os.path.join(file_root_path, KNOWN_URLS_FILE_NAME), 'w') as f:
        for base_url, pic_url_or_info in pic_info.items():
            for k, v in pic_url_or_info.items():
                if k != 'pic_txt' and k != 'pic_title':
                    que.put(k)

                    pic_path_info[k] = pic_info[base_url]['pic_title']
                    pic_name_info[k] = v

                    f.write(k + '\n')

    print('开始多线程下载图片')
    for _ in range(5):
        t = ThreadDownloadPic(que, file_root_path, pic_info, pic_path_info, pic_name_info)
        t.setDaemon(True)
        t.start()

    que.join()

    print('写入已下载的url')
    with open(os.path.join(file_root_path, FLAG_URL_FILE_NAME), 'a') as f:
        for base_url in pic_info:
            f.write(base_url + '\n')

    print('end')

    # for i in forthcoming_urls:
    #     print(i)

    #
    #
    # with open(file_root_path, 'w') as f:
    #     for url in forthcoming_urls:
    #         f.write(url)
    #         f.write('\n')


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

    def time_sleep(self, secs=0.1):
        time.sleep(secs)

    def run(self):
        while True:
            self.time_sleep()
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

                # 由于多线程的存在,导致了可能一起创建文件夹
                # 所以给这个步骤加上一个检测
                # 忽略文件创建的错误
                try:
                    if not os.path.exists(os.path.join(self.img_root_path, img_save_path)):
                        os.makedirs(os.path.join(self.img_root_path, img_save_path))
                except FileExistsError:
                    pass

                if os.path.isfile(temp_path):
                    os.remove(temp_path)

                img_contents = requests.get(url).content
                with open(temp_path, 'wb') as f:
                    f.write(img_contents)

                self.que.task_done()

            except Exception as e:
                print('这里报错?\n' + str(e)
                    + '\n' + 'img_save_path is: ' + str(img_save_path)
                    + '\n' + 'img_name is: ' + str(img_name)
                    + '\n' + 'temp_path is: ' + str(temp_path)
                    + '\n' + 'url is: ' + str(url)
                    + '\n' + '-------------' )
                break
                # 这个是由于有个图片的最后一个文字是?,导致系统报错
                # 然后这个queue就无法停下来
                # 所以我尝试用sys.exit强行终止这个问题
                # 结果也不好使~
                # 结论:下面这句话没用
                # sys.exit(1)



from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import re


class SpiderGamersky:

    def __init__(self):
        self._root_url = r'http://www.gamersky.com/ent/xz/'
        self._forthcoming_urls = set()
        # self._d_pic_info = {}

        chrome_path = r'D:\program\chromedriver\chromedriver.exe'
        self._browser = webdriver.Chrome(executable_path=chrome_path)
        self._browser.get(self._root_url)
        self.p = re.compile('ent/\d{6}/')

    def __handle_page(self, download_page=0):
        """
        经过一些尝试,发现在获取page_num的时候报错:StaleElementReferenceException
        试过一些办法,发现忽略这个问题是最简单的~
        所以直接利用循环增长页面
        :param download_page: 如果传入的数字为0,则将其设置为一个很大的数字~
        :return:
        """

        download_page = 999999 if download_page == 0 else download_page
        page_now = 1

        # 判断数据是否加载完毕
        locator_ul = (By.CLASS_NAME, 'pictxt,contentpaging')
        # 传入特定的locator格式,判断下一页是否存在
        locator_page = (By.LINK_TEXT, '下一页')
        # 传入特定的locator格式,判断要查询的元素是否加载完毕
        # 不能用这个判断,貌似这个只会检验第一个con而不是检验最后一个con
        # (毕竟程序也不知道哪个是最后的con)
        # 因为程序运行的比网页加载快,所以程序会快于网页达到下个con导致报错
        # con是一个一个展现的
        # locator_con = (By.CLASS_NAME, 'con')

        # 20180720 添加一个判断
        # 对于201503之前的图片不下载
        # 当获取到201503时,终止循环


        # 循环点击下一页,直到没有下一页为止
        # 需要等待数据完全载入后判断
        while 1:
            # 这个是判断当前页面是否加载完毕

            element_ul = WebDriverWait(self._browser, 10).until(
                EC.presence_of_element_located(locator_ul)
            )

            try:
                element_page = WebDriverWait(self._browser, 10).until(
                    EC.presence_of_element_located(locator_page)
                )
            except TimeoutException:
                print('无"下一页"元素, 停止循环, page: ' + str(page_now))
                break

            download_flag = self.__get_forthcoming_urls()

            if element_ul and element_page \
                    and page_now < download_page and download_flag == '1':
                # next_page_button = self._browser.find_element_by_partial_link_text('下一页')
                self._browser.find_element_by_link_text('下一页').click()
                page_now += 1
                # 不能用这个,理由见上面
                # element_locator_con = WebDriverWait(self._browser, 10).until(
                #     EC.presence_of_element_located(locator_con)
                # )

            else:
                break

        return self._forthcoming_urls

    def __get_forthcoming_urls(self):

        all_class_cons = self._browser.find_elements_by_class_name('con')[1:]

        for class_con in all_class_cons:
            class_title = class_con.find_elements_by_tag_name('div')[0]
            # class_txt = class_con.find_elements_by_tag_name('div')[1]

            forthcoming_pic_url = class_title.find_element_by_tag_name('a').get_attribute('href')
            # print(forthcoming_pic_url)
            # download_title = class_title.find_element_by_tag_name('a').get_attribute('title')
            # download_txt = class_txt.text

            if re.findall(self.p, forthcoming_pic_url):
                pic_date = re.findall(self.p, forthcoming_pic_url)[0][4:10]

                self._forthcoming_urls.add(forthcoming_pic_url)
            # self._d_pic_info.update()

        return '1' if pic_date >= '201503' else '0'

    @staticmethod
    def get_all_forthcoming_urls(download_page):
        return SpiderGamersky().__handle_page(download_page)
        
