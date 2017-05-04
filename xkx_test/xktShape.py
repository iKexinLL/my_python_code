'''
<Python3 程序开发指南> p205
自定义类
ipython 自动重载包
%load_ext autoreload
%autoreload 2
'''

import math

class Point: # 默认从object继承

    def __init__(self, x=0, y=0):
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
        # assert isinstance(other, Point), 'Not the same type' #第一种方法
        # if not isinstance(other, Point): raise TypeError() #第二种方法
        if not isinstance(other, Point):return NotImplemented
        return self.x == other.x and self.y == other.y 

    def __repr__(self):
        '''
        使用repr(x)调用,返回一个特定格式的字符串
        一般来说 __repr__对Python比较友好,而__str__对用户比较友好
        返回x的字符串表示,在可能的地方eval(repr(x)) == x
        '''
        return "Point({0.x!s},{0.y!s})".format(self)

    def __str__(self):
        # print('调用__str__')
        # 关于!r的解释,查阅文档,找 format string syntax
        return "({0.x!r},{0.y!r})".format(self)


class Circle(Point):

    def __init__(self, radius, x=0, y=0):
        super().__init__(x, y)
        self.radius = radius

    def edge_distance_from_origin(self):
        return abs(self.distance_from_origin() - self.radius)

    def area(self):
        return math.pi * (self.radius ** 2)

    def circumference(self):
        return 2 * math.pi * self.radius

    def __eq__(self, other):
        # 子类是否需要 isinstance 判断?
        # 不需要,至少在这里,基类的判断可以消除歧义,毕竟要符合Point才能是Circle
        return self.radius == other.radius and super().__eq__(other)

    def __repr__(self):
        return "Circle({0.radius!r},{0.x!r},{0.y!r})".format(self)

    def __str__(self):
        return repr(self)


class ProCircle(Point):
    '''添加了修饰器'''

    def __init__(self, radius, x=0, y=0):
        '''
        1.如果在set,get方法中使用了不加下划线的变量,则会无限递归
            set的无限递归可以理解.set方法中的self.radius = radius这一步会无限调用set方法.
            那么get方法的无限递归呢?啊,对,return self.radius这个方法同样会无限调用get方法.
            所以这个property中还是要使用其他变量(@property会创建一个对象.详见ProCircleTestOne)
        2.问题见 ProCircleTestOne
        3.问题见 ProCircleTestTwo
        '''
        super().__init__(x, y)
        print('调用父类__init__完毕')
        self.radius = radius # 这会调用 set方法,而ProCircleTestTwo中使用__radius则不会调用set
    
    @property
    def radius(self): # getter
        '''This is a ProCircle with "property"''' # help一下就会显示
        print('调用get')
        return self.__radius
    
    @radius.setter
    def radius(self, radius):
        print('调用set')
        assert radius > 0, "radius must be nonzero and non-negative"
        self.__radius = radius

    def edge_distance_from_origin(self):
        return abs(self.distance_from_origin() - self.radius)

    def area(self):
        return math.pi * (self.radius ** 2)
    
    def circumference(self):
        return 2 * math.pi * self.radius

    def __eq__(self, other):
        '''
        子类是否需要 isinstance 判断?
        不需要,至少在这里,基类的判断可以消除歧义,毕竟要符合Point才能是Circle
        '''
        return self.radius == other.radius and super().__eq__(other)

    def __repr__(self):
        return "Circle({0.radius!r},{0.x!r},{0.y!r})".format(self)

    def __str__(self):
        return repr(self) 


class ProCircleTestOne(Point):
    '''替换@property中的内容,虽然这并不符合规范'''

    def __init__(self, radius, x=0, y=0):
        '''
        这里使用了self.test_value进行了测试.
        发现@propery会默认生成一个radius的值,按照如下内容写法,将会test_value == radius

        >>> pcto = ProCircleTestOne('5',6,7)
        >>> pcto.test_value
        >>> 5
        >>> pcto.radius
        >>> 5
        '''
        super().__init__(x, y)
        print('调用父类__init__完毕')
        self.test_value = radius # 这里改为了 __radius
    
    @property
    def radius(self): # getter
        '''This is a ProCircle with "property"''' # help一下就会显示
        print('调用get')
        return self.test_value
    
    @radius.setter
    def radius(self, radius):
        print('调用set')
        assert radius > 0, "radius must be nonzero and non-negative"
        self.test_value = radius 

    def __repr__(self):
        return "Circle({0.radius!r},{0.x!r},{0.y!r})".format(self)

    def __str__(self):
        return repr(self)         

class ProCircleTestTwo(Point):
    '''
    如何像C#那样创建一个私有变量,只能通过get访问?
    而且现在问题是使用self.__radius并不能触发set方法
    结论见ProCircleTestThree
    '''

    def __init__(self, radius, x=0, y=0):
        '''
        使用self.__radius初始化,并不能触发set中的检测
        >>> pctt = xktShape.ProCircleTestTwo('5',6,7)
        >>> pctt
        >>> Circle('5',6,7)
        >>> pctt.radius
        >>> '5'
        >>> pctt.radius = -3
        >>> .. 报错
        >>> pctt.radius = 5
        >>> pctt.radius
        >>> 5
        '''
        super().__init__(x, y)
        print('调用父类__init__完毕')
        self.__radius = radius
    
    @property
    def radius(self): # getter
        '''This is a ProCircle with "property"''' # help一下就会显示
        print('调用get')
        return self.__radius
    
    @radius.setter
    def radius(self, radius):
        print('调用set')
        assert radius > 0, "radius must be nonzero and non-negative"
        self.__radius = radius    

    def __repr__(self):
        return "Circle({0.radius!r},{0.x!r},{0.y!r})".format(self)

    def __str__(self):
        return repr(self)         

    def p(self):
        print(self.__radius)


class ProCircleTestThree(Point):
    '''
    在__init__中,不必一定要写成双下划线.
    可以像如下方式,只要使用@property,将get方法处理掉,那么就无法获取radius的内容了
    利用其它方法返回radius的值就可以了...
    '''

    def __init__(self, radius, x=0, y=0):
        '''
        最终结论
        '''
        super().__init__(x, y)
        print('调用父类__init__完毕')
        self.radius = radius
    
    @property
    def radius(self): # getter
        '''This is a ProCircle with "property"''' # help一下就会显示
        print('调用get')
        #return self.__radius
        pass
    
    @radius.setter
    def radius(self, radius):
        print('调用set')
        assert radius > 0, "radius must be nonzero and non-negative"
        self.__radius = radius    

    def __repr__(self):
        return "Circle({0.radius!r},{0.x!r},{0.y!r})".format(self)

    def __str__(self):
        return repr(self)         

    def return_radius(self):
        return(self.__radius)        