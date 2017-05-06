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
        这里返回的是一个新创建的FuzzyBool对象
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

    def __bool__(self):
        return self.__value > 0.5

    def __int__(self):
        '''
        round函数会进行四舍五入
        return 1 if self.__value > 0.5 else 0
        '''
        return round(self.__value)
    
    def __float__(self):
        return self.__value

    def __lt__(self, other):
        '''
        < 方法

        基本的比较有六个,">","<","==","!=",">=","<="
        至少要实现三个,剩余的Python可以进行推导

        箭头所指方向即为所要方向
        '''
        return self.__value < other.__value

    def __eq__(self, other):
        '''
        重新定义__eq__方法的话,会导致原本可以实现的hash(x)无法正常使用
        只能在类中定义__hash__方法
        '''
        return self.__value == other.__value 

    def __le__(self, other):
        return self.__value <= other.__value

    def __hash__(self):
        '''
        为了避免定义__eq__函数导致原有__hash__方法失效,
        在类中重新定义
        '''
        return hash(id(self))

    def __format__(self, format_spec):
        '''
        不太理解这个,等下再查查资料
        
        更新: 
        fb = xktFuzzyBool.FuzzyBool(.5)
        这个定义了在使用 '{0}'.format(fb) 后的返回结果
        如果 将定义 return 'a' 那么
        >>> '{0}'.format(fb)
        >>> 'a'
        但是按照如下格式定义,则直接返回 结果
        >>> '{0}'.format(fb)
        >>> 0.5
        
        format(self.__value, format_spec) == self.__value__.__format__(format_spec)
        '''
        return format(self.__value, format_spec) 
    
    def __repr__(self):
        return ("{0}({1})".format(self.__class__.__name__, self.__value))

        

class FuzzyBoolInhFloat(float):
    '''
    继承于float类,那么现在只要重写一些方法,并且屏蔽一些方法(会破坏多态性)
    '''        

    def __new__(cls, value = 0.0):
        '''
        在创建任意一个对象前,会首先调用__new__()方法(类似于声明一个对象).
        该方法不能传递self参数,因为self还未存在.
        也就是说,__new__之后才会存在,然后使用__init__初始化.
        
        为什么这下面没有定义__value呢?
        因为继承自float,那么其实这就是一个float的对象.
        '''
        return super().__new__(cls,
                                value if 0.0 <= value <= 1.0 else 0.0)

    def __and__(self, other):
        return FuzzyBoolInhFloat(min(self, other))

    def __invert__(self):
        return FuzzyBoolInhFloat(1.0 - float(self))        

    def __add__(self, other):
        '''
        取消__add__的方法.
        取消继承而来的无用方式一
        '''
        raise NotImplementedError()

    def __iadd__(self, other):
        '''
        取消继承而来的无用方式二
        这里在括号内换行不需要加 \,因为有 引号("unsupported operand type(s) for +:"
                        "'{0}' and '{1}' ")
        其他 ("adff \
                    adsf")
        '''
        raise TypeError("unsupported operand type(s) for +:"
                        "'{0}' and '{1}' ".format(
                            self.__class__.__name__, other.__class__.__name__))

    def __eq__(self, other):
        '''
        取消继承而来的无用方式三
        '''
        return NotImplemented

    def __lt__(self, other):
        '''
        这种"取消"操作无法推断
        '''
        return NotImplemented

    def __neg__(self):
        '''
        对于单值操作,使用模拟内置类型的方式
        unary:一元的
        '''
        raise TypeError("bad openrand type for unary -:'{0}'".format(
            self.__class__.__name__
        ))

    '''
    使用exec动态取消,这个是单元操作符
    '''
    for name, operator in (("__neg__", "-"), ("__index__", "index()")):
        message = ("bad openrand type for unary {0}: '{{self}}'".format(operator))
        exec("def {0}(self):raise TypeError(\"{1}\".format("
            "self = self.__class__.__name__))".format(name, message))
