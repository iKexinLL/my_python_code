#!/usr/bin/python
# coding=utf-8

"""
__time__ = '2018/7/16 15:42'
__author__ = 'Kexin Xu'
__desc__ = 使用chromedriver+selenium来爬取网站
        此过程只是为了获取网站上的网址
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SpiderGamersky:

    def __init__(self):
        self._root_url = r'http://www.gamersky.com/ent/xz/'
        self._forthcoming_urls = set()
        # self._d_pic_info = {}

        chrome_path = r'D:\program\chromedriver\chromedriver.exe'
        self._browser = webdriver.Chrome(executable_path=chrome_path)
        self._browser.get(self._root_url)

    def __handle_page(self, download_page=0):
        """
        :param download_page: 如果传入的数字为0,则将其设置为一个很大的数字~
        :return:
        """
        # 加载首页
        self.__get_forthcoming_urls()
        download_page = 999999 if download_page == 0 else download_page

        # 传入特定的locator格式,判断下一页是否存在
        locator_next_page = (By.LINK_TEXT, '下一页')
        # 传入特定的locator格式,判断要查询的元素是否加载完毕
        # 不能用这个判断,貌似这个只会检验第一个con而不是检验最后一个con
        # (毕竟程序也不知道哪个是最后的con)
        # 因为程序运行的比网页加载快,所以程序会快于网页达到下个con导致报错
        # con是一个一个展现的
        # locator_con = (By.CLASS_NAME, 'con')

        # 循环点击下一页,直到没有下一页为止
        # 需要等待数据完全载入后判断
        while 1:
            try:
                # 这个是判断当前页面是否加载完毕
                element_next_page = WebDriverWait(self._browser, 10).until(
                    EC.presence_of_element_located(locator_next_page)
                )

                page_now = int(self._browser.find_element_by_class_name('p3').text)

                if element_next_page and page_now < download_page:
                    # next_page_button = self._browser.find_element_by_partial_link_text('下一页')
                    self._browser.find_element_by_link_text('下一页').click()

                    # 不能用这个,理由见上面
                    # element_locator_con = WebDriverWait(self._browser, 10).until(
                    #     EC.presence_of_element_located(locator_con)
                    # )

                    # 这个是判断点击'下一页'后,页面是否加载完毕
                    try:
                        element_next_page = WebDriverWait(self._browser, 10).until(
                            EC.presence_of_element_located(locator_next_page)
                        )

                        if element_next_page:
                            print('点击完下一页后的页数:' + self._browser.find_element_by_class_name('p3').text)
                            self.__get_forthcoming_urls()

                    except:
                        pass

                    if element_next_page:
                        print('点击完下一页后的页数:' + self._browser.find_element_by_class_name('p3').text)
                        self.__get_forthcoming_urls()
                else:
                    break

            except NoSuchElementException:
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

            self._forthcoming_urls.add(forthcoming_pic_url)
            # self._d_pic_info.update()

    @staticmethod
    def get_all_forthcoming_urls(download_page):
        return SpiderGamersky().__handle_page(download_page)


if __name__ == '__main__':
    SpiderGamersky.get_all_forthcoming_urls(2)