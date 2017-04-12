#encoding=utf-8
"""
Created on 2016/3/17 15:53
author: iKexinLL
测试dict在方法中时候会改变
"""


class my_dict(object):

    def __init__(self):
        self.d = {'a':0, 'b':0}
        print('first self.d is ' + str(self.d))

    def test(self):
        """
        循环三次, 对self.d 进行修改
        :return:
        """
        in_d = {'b': 0, 'a':0}
        for i in range(3):
            self.change(3, in_d)

        print('after change, now in_d is {0}, and self.d is {1}'.format(str(in_d), str(self.d)))

    def change(self,a, in_d):
        self.d['a'] += 1

        in_d['b'] += 1

        print('in change, in_d is ' + str(in_d))
        print('in change, self.d is ' + str(self.d))


if __name__ == '__main__':
    my_dict().test()