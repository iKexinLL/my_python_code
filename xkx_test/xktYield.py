
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
           