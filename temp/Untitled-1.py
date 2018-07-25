import functools


def positive_result(function):
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        assert result >= 0, function.__name__ + "() result isn't >= 0 "
        return result
    wrapper.__name__ = function.__name__
    wrapper.__doc__ = function.__doc__
    return wrapper

@positive_result
def test(a = -1):
    return a 

def positive_result_2(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        assert result >= 0, function.__name__ + "() result isn't >= 0 "
        return result
    return wrapper

@positive_result_2
def test_2(a = -1):
    return a 

test()
test_2()


assigned = functools.WRAPPER_ASSIGNMENTS

for attr in assigned:
    print(attr + ':' + str(getattr(test, attr)))
    
>>> __module__:__main__
>>> __name__:test
>>> __qualname__:positive_result.<locals>.wrapper
>>> __doc__:None
>>> __annotations__:{}


import unicodedata

unicodedata.category(',')

