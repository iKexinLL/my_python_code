#encoding=utf-8
"""
Created on 2016/7/20 13:06
author: iKexinLL
"""

import functools


def positive_result(function):

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        assert result > 0, function.__name__ + "() result isn't >= 0"
        return result

    return wrapper


