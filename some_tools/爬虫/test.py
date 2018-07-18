#!/usr/bin/python
# coding=utf-8

import threading
import queue
import re

class ThreadUrl(threading.Thread):
    """
    多线程下载类
    1.下载url集合
    2.保存的地址
    3.保存的信息
    """

    def __init__(self, que, img_save_path, file_info):
        """
        :param que:需要下载的url集合
        :param file_info:使用字典来保存的文件信息,k为url地址,v为信息
        :param img_save_path:要保存的文件路径
        :return:
        """
        threading.Thread.__init__(self)
        self.que = que
        self.file_info = file_info
        self.img_save_path = img_save_path

        def run(self):
            while (True):
                try:
                    url = self.que.get()
                    print(url)

                    re_compile = '\*|\?|"|<|>|\||\u3000'
                    
                    file_name = re.sub(re_compile, '', 
                            file_info[url] if file_info else url)

                    temp_path = os.path.join(self.img_save_path, file_name)
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