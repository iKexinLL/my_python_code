#!/usr/bin/python
# coding=utf-8

"""
__time__ = '2018/7/16 15:42'
__author__ = 'Kexin Xu'
__desc__ = 使用chromedriver+selenium来爬取网站
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SpiderGamersky:


    def __init__(self):
        _root_url = r'http://www.gamersky.com/ent/xz/'
        _forthcoming_urls = set()

        chrome_path = r'D:\program\chromedriver\chromedriver.exe'
        _browser = webdriver.Chrome(executable_path=chrome_path)
        _browser.get(_root_url)


    def __handle_page(self):
        # 加载首页
        __get_forthcoming_urls()

        # 传入特定的locator格式,判断下一页是否存在
        locator_next_page = (By.LINK_TEXT, '下一页')
        # 传入特定的locator格式,判断要查询的元素是否加载完毕
        locator_con = (By.CLASS_NAME, 'con')

        # 循环点击下一页,直到没有下一页为止
        # 需要等待数据完全载入后判断
        while (1):
            try:
                element_next_page = WebDriverWait(_browser, 10).until(
                    EC.presence_of_element_located(locator_next_page)
                )

                element_locator_con = WebDriverWait(_browser, 10).until(
                    EC.presence_of_element_located(locator_con)
                )

                print(_browser.find_element_by_class_name('p3').text)
                if element_next_page and element_locator_con:
                    # next_page_button = _browser.find_element_by_partial_link_text('下一页')
                    _browser.find_element_by_link_text('下一页').click()
                    __get_forthcoming_urls()

            except NoSuchElementException:
                break

    def __get_forthcoming_urls(self):

        all_class_cons = _browser.find_elements_by_class_name('con')[1:]

        for class_con in all_class_cons:
            class_title = class_con.find_elements_by_tag_name('div')[0]
            class_txt = class_con.find_elements_by_tag_name('div')[1]

            forthcoming_pic_url = class_title.find_element_by_tag_name('a').get_attribute('href')
            print(forthcoming_pic_url)
            download_title = class_title.find_element_by_tag_name('a').get_attribute('title')
            download_txt = class_txt.text

            _forthcoming_urls.add(forthcoming_pic_url)

    @staticmethod
    def get_all_forthcoming_urls():
        return SpiderGamersky().__handle_page()

if __name__ == '__main__':
    SpiderGamersky.get_all_forthcoming_urls()