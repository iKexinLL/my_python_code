
import sys

def quarters(next_quarte = 0.0, split = 0.25):
    while True:
        print('before yield')
        # 可以确认这个 receieved是用来接收send方法的参数
        # 在被next调用时, receieved均是None
        # 另外,为什么这个方法有while True但是没有终止条件呢?
        # 因为这是一个generator,只有在调用的时候才会运行.
        # 所以内部的while True只对值有影响,但不会一直运行
        # 下面的例子是官网的例子,说明了使用调用了close方法
        # 才会明确停止
        receieved = (yield next_quarte)
        print('after yield')
        if receieved is None:
            next_quarte += split
        else:
            next_quarte = receieved


result = []

generator = quarters()
while len(result) < 5:
    x = next(generator)
    if abs(x - .5) < sys.float_info.epsilon:
        x = generator.send(1.0)
    result.append(x)



def echo(value=None):
    print("Execution starts when 'next()' is called for the first time.")
    try:
        while True:
            try:
                print('yield')
                value = (yield value)
                print('value is {0}'.format(value))
            except Exception as e:
                print('Exception')
                value = e
    finally:
        print("Don't forget to clean up when 'close()' is called.")

'''
>>> ge = echo(1)
>>> Don't forget to clean up when 'close()' is called.
>>> next(ge)
>>> Execution starts when 'next()' is called for the first time.
>>> yield
>>> 1
>>> next(ge)
>>> value is None
>>> yield
>>> next(ge)
>>> value is None
>>> yield
>>> ge.send(2)
>>> value is 2
>>> yield
>>> 2
>>> ge.close()
>>> Don't forget to clean up when 'close()' is called.        
'''
           
### 例子2 对于文件通配符的处理

if sys.platform.startswith("win"):
    def get_files(names):
        for name in names:
            if os.path.isfile(name): # 1.如果name为文件则输出文件名称
                yield name 
            else: # 2.如果name不是文件,则使用glob进行分析
                for file in glob.iglob(name):
                    if not os.path.isfile(file): # 3.如果使用glob解析仍不是文件
                        continue                 # (一般为文件夹),则略过
                    yield file # 4.返回了按照Unix解析路径的文件结果
else:
    def get_files(names):
        '''
        这里使用圆括号创建了一个生成器表达式.
        '''
        return (file for file in names if os.path.isfile(file))

'''
>>> for file in get_files([r'D:\python35\*.exe']):
        print(file)
>>> D:\python35\python.exe
D:\python35\pythonw.exe
D:\python35\Removepywin32.exe
'''