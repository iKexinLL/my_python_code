#!/usr/bin/python
# coding=utf-8

"""
__time__ = '2018/7/16 15:42'
__author__ = 'Kexin Xu'
__desc__ = 使用chromedriver+selenium来爬取网站
        此过程只是为了获取网站上的网址
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import re


class SpiderGamersky:

    def __init__(self, root_url):
        self._root_url = root_url
        self._forthcoming_urls = set()
        # self._d_pic_info = {}

        chrome_path = r'D:\program\chromedriver\chromedriver.exe'
        try:
            self._browser = webdriver.Chrome(executable_path=chrome_path)

            self._browser.set_page_load_timeout(20)
            self._browser.set_script_timeout(20)
        except TimeoutException as e:
            print('链接超时')
            print(e)
            self.close_chromedriver()

        self._browser.get(self._root_url)
        self.p = re.compile(r'ent/\d{6}/')

    def __wait_element(self, locator, browser, timeout=10):
        return WebDriverWait(self._browser, 10).until(
                EC.presence_of_element_located(locator)
            )

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

            element_ul = self.__wait_element(locator=locator_ul, browser=self._browser)

            try: 
                element_page = self.__wait_element(locator=locator_page, browser=self._browser)
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

    def get_all_forthcoming_urls(self, download_page):
        return self.__handle_page(download_page)

    def close_chromedriver(self):
        self._browser.close()


if __name__ == '__main__':
    # SpiderGamersky().get_all_forthcoming_urls(0)
    pass
    
