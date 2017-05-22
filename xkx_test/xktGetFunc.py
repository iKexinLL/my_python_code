'''
动态导入python模块内的方法

此程序适用于与 WindowsMagicNumbers.py和StandardMagicNumbers.py在同一文件夹下时使用

一个Python Module(模块)，是一个文件，包含了Python对象定义和Python语句（definitions and statements）
详见 E:\code\py30eg\magic-numbers.py 文件
'''

import os
import sys

def load_modules():
    modules = []
    # 这里是为了读取当前文件下的文件,传递'.'是为了防止异常(返回当前环境的路径下文件内容)
    for name in os.listdir(os.path.dirname(__file__) or '.'):
        #查找以'.py'结尾且包含magic的文件
        if name.endswith('.py') and 'magic' in name.lower():
            filename = name
            # 分离文件名称和最后一个'.'后面的内容(忽略开始的'.',例如.git等等,并可能为空)
            name = os.path.splitext(name)[0] 
            # name为合理字符串且未导入到此程序中
            if name.isidentifier() and name not in sys.modules:
                with open(filename, 'r', encoding = 'utf-8') as fh:
                    code = fh.read()
                    # type(sys)(name): <module 'StandardMagicNumbers'>
                    # type(sys)(name): <module 'WindowsMagicNumbers'>
                    module = type(sys)(name)
                    # 将导入的module导入到此程序中
                    # 每个导入的包,都会在sys.modules产生一个键值
                    # 这样应该是方便管理
                    sys.modules[name] = module
                    # >>> print('StandardMagicNumbers' in sys.modules) >>> True
                    # ---------
                    # module.__dict__: {'__package__': None, '__loader__': None, '__doc__': None, '__spec__': None, '__name__': 'WindowsMagicNumbers'}
                    # module.__dict__: {'__package__': None, '__loader__': None, '__doc__': None, '__spec__': None, '__name__': 'StandardMagicNumbers'}
                    # 这步才算将代码执行
                    exec(code, module.__dict__)
                    modules.append(module)

    return modules


# get_function.cache = {}
# get_function.bad_cache = set()


def get_function(module, function_name):
    print('module: ' + str(module))
    function = get_function.cache.get((module, function_name), None)
    print('function1: ' + str(function))
    if (function is None and
        (module, function_name) not in get_function.bad_cache):
        try:
            function = getattr(module, function_name)
            print('function2: ' + str(function))
            if not hasattr(function, "__call__"):
                raise AttributeError()
            get_function.cache[module, function_name] = function
        except AttributeError:
            function = None
            get_function.bad_cache.add((module, function_name))
            raise AttributeError('No method')
    return function

get_function.cache = {}
get_function.bad_cache = set()


def main():
    modules = load_modules()
    print('get_function: ' + str(get_function.bad_cache))
    for module in modules:
        my_test = get_function(module, 'my_test_print')
        print(my_test('abc'))


#print(os.listdir(os.path.dirname(__file__)))
#print(os.getcwd())

if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
    print("usage: {0} [-1|-2] file1 [file2 [... fileN]]".format(
          os.path.basename(sys.argv[0])))
    sys.exit(2)

main()
print('get_function.cache: ' + str(get_function.cache))
print('get_function: ' + str(get_function))