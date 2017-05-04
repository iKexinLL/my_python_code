'''
模糊型布尔值

a = FuzzyBool.FuzzyBool(.875)
b = FuzzyBool.FuzzyBool(.25)

a >= b                              # return True
bool(a), bool(b)                    # return (True, False)
....

支持 <, <=, ==, !=, >=, >, not(~), and(&), or(|) 
conjuction()
disjunction()

!!!注意 __del__() 只是引用计数减一,并不能保证其被回收
'''

class FuzzyBool:

    def __init__(self, value = 0.0):
        '''
        创建私有__value值,未使用@property方式创建.
        '''
        self.__value = value if 0.0 <= value <= 1.0 else 0.0

    def __and__(self, other):
        '''
        AND操作符
        由于AND操作符,只有当全部为真时才返回True,否则返回False,所以直接返回最小值.
        未加类型判断
        '''
        return FuzzyBool(min(self.__value, other.__value))

    def __iand__(self, other):
        '''
        这里未定义__rand__, 因为这个方法对于FuzzyBool是没有必要的.

        大多数二元操作符的特殊方法都具有"i"(in-palce)与"r"(反射,即互换操作数)这两个版本
        '''
        self.__value = min(self.__value, other.__value)
        return self

    def __or__(self, other):
        return FuzzyBool(max(self.__value, other.__value))

    def __ior__(self, other):
        self.__value = max(self.__value, other.__value)
        return self    
    
    def __repr__(self):
        return ("{0}({1})".format(self.__class__.__name__, self.__value))