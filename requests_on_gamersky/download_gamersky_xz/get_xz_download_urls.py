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
import sys
import datetime

import requests
from bs4 import BeautifulSoup

try:
    from download_gamersky_xz.ThreadDownloadPic import ThreadDownloadPic
    from download_gamersky_xz.get_html_by_chromedriver import SpiderGamersky
except:
    import ThreadDownloadPic
    from get_html_by_chromedriver import SpiderGamersky

# 添加sleep,简单的尝试别被封锁
import time

def time_sleep(secs=0.1):
    time.sleep(secs)



DOWNLOAD_PAGES = 1
root_urls = [r'http://www.gamersky.com/ent/qw',
        r'http://www.gamersky.com/ent/xz']
IF_USE_PORTABLE_DISK = False
FLAG_URL_FILE_NAME = 'downloaded_url.txt'
IMG_FORMATS = ['GIF', 'JPG', 'PNG', 'BMP', 'JPEG']
NOW_DATE = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')


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

def get_image_folder_path(root_url, if_use_portable_disk=IF_USE_PORTABLE_DISK):
    """
    确认要存储图片的文件夹位置
    """

    folder_name = root_url.split('/')[-1]

    if if_use_portable_disk:
        folder_root_path = r'X:\杂乱文件' + '\\gamersky_' + folder_name + '\\' + NOW_DATE
        assert judge_wd(), '移动硬盘不存在,请插入硬盘'
    else:
        folder_root_path = r'e:\temp\img_save' + '\\gamersky_' + folder_name + '\\' + NOW_DATE

    # 如果文件夹不存在,则创建文件夹
    if not os.path.isdir(folder_root_path):
        os.makedirs(folder_root_path)

    return folder_root_path

def get_file_for_downloaded_urls(file_root_path):
    """
    读取已经下载过(downloaded_url.txt)的的网址
    """

    file_flag_path = os.path.join('\\'.join(file_root_path.split('\\')[:-1]), FLAG_URL_FILE_NAME)
    # 如果当前文件不存在,则创建文件
    if not os.path.isfile(file_flag_path):
        # windows上,python没有os.mknod
        # os.mknod(os.path.join(file_root_path, FLAG_URL_FILE_NAME))
        with open(file_flag_path, 'w', encoding='utf-8') as f:
            f.close()
    
    file_downloaded_urls = set()

    with open(file_flag_path, encoding='utf-8') as f:
        for line in f.readlines():
            file_downloaded_urls.add(line.replace('\n', ''))

    return file_downloaded_urls


def get_soup(url, encoding='utf-8'):
    r = requests.get(url)
    # 解决中文乱码问题
    r.encoding = encoding
    soup = BeautifulSoup(r.text.replace('\n', ''), 'lxml')
    return soup

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
    for root_url in root_urls:
        pic_info = {}
        pic_path_info = {}
        pic_name_info = {}

        part_name = root_url.split('/')[-1]

        # 图片要存储的根目录
        file_root_path = get_image_folder_path(root_url, if_use_portable_disk=IF_USE_PORTABLE_DISK)

        # downloaded_url.txt位置
        print('获取%s已下载的url'%part_name)
        downloaded_urls = get_file_for_downloaded_urls(file_root_path)

        print('获取gamersky上的url')
        spider_gamersky = SpiderGamersky(root_url)
        forthcoming_urls = spider_gamersky.get_all_forthcoming_urls(DOWNLOAD_PAGES)
        spider_gamersky.close_chromedriver()

        print('开始下载%s图片信息'%part_name)
        cnt = 0
        for forthcoming_url in forthcoming_urls:
            url_pages = [forthcoming_url]
            # time_sleep()
            pic_info[forthcoming_url] = {}
            for url in url_pages:
                if url not in downloaded_urls:
                    soup = get_soup(url)
                    print('forthcoming url is ' + url)
                    pic_info[forthcoming_url].update(get_url_and_file_info(soup, url_pages))
                    cnt += 1
                else:
                    continue
            print('------------已统计%d个图片需要下载-----------' % cnt)

        # 添加已获取的图片地址

        que = queue.Queue()

        for base_url, pic_url_or_info in pic_info.items():
            for k, v in pic_url_or_info.items():
                if k != 'pic_txt' and k != 'pic_title':
                    que.put(k)

                    pic_path_info[k] = pic_info[base_url].get('pic_title','None_' + time.strftime('%Y%m%d_%H%M%S'))
                    pic_name_info[k] = v


        print('开始多线程下载图片')
        with open(os.path.join(file_root_path, FLAG_URL_FILE_NAME), 'a') as f:
            for _ in range(5):
                t = ThreadDownloadPic.ThreadDownloadPic(que, file_root_path, pic_info, pic_path_info, pic_name_info, f)
                t.setDaemon(True)
                t.start()

            que.join()

        print('写入已下载的url')
        print('end_' + part_name)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print(time.time() - start_time)
