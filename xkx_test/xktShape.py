'''
<Python3 程序开发指南> p205
自定义类
'''

import math

class Point: # 默认从object继承

    def __init__(self, x=0, y=0):
        print('调用__init__')
        self.x = x 
        self.y = y

    # def __new__(self): 
    #     '''
    #     __new__ 方法在__init__之前调用,
    #     未知如何设置__new__
    #     '''
    #     print('调用__new__')
    #     object.__new__(self) # 并不调用__init__
    #     #self.__init__() #wrong

    def distance_from_origin(self):
        return math.hypot(self.x, self.y) 

    def __eq__(self, other):
        '''
        p208说明了如何避免不恰当的比较
        '''
        # print('调用__eq__')
        # assert isinstance(other,Point), 'Not the same type' #第一种方法
        # if not isinstance(other,Point): raise TypeError() #第二种方法
        if not isinstance(other, Point):return NotImplemented
        return self.x == other.x and self.y == other.y 

    def __repr__(self):
        '''
        使用repr(x)调用,返回一个特定格式的字符串
        一般来说 __repr__对Python比较友好,而__str__对用户比较友好
        '''
        print('调用__repr__')
        return "Point({0.x!s}, {0.y!s})".format(self)

    def __str__(self):
        # print('调用__str__')
        return "({0.x!r}, {0.y!r})".format(self)




