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


if __name__ == '__main__':
    main()

# d['root_url'] = {'down_url_1':'name_1'
#                  'down_url_2':'name_2'}
