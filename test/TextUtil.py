#encoding=utf-8
"""
Created on 2016/3/14 21:40
author: iKexinLL
This module provides a few string mainpulation functions
'\n' 竟然不能在 simplify('''this \n  and that \t to''') 中用


>>> is_balanced("(python (is (not (lisp))))")
True
>>> shorten("The Crossing", 10)
'The Cro...'
>>> simplify(" some    text with  spurious whitespace ") #spurious 伪造的
'some text with spurious whitespace'
"""

import string

from blaze.compute.tests.test_bcolz_compute import to

def is_balanced(text , brackets = "()[]{}<>") :

    counts = {}
    left_for_right = {}

    for left, right in zip(brackets[::2], brackets[1::2]):

        assert left != right, "the bracket characters must differ"

        counts[left] = 0
        left_for_right[right] = left

    for c in text:
        if c in counts:
            counts[c] += 1
        elif c in left_for_right:
            left = left_for_right[c]
            if counts[left] == 0:
                return False
            counts[left] -= 1

    return not any(counts.values())

def shorten(text, length = 25, indicator = '...'):

    if length <= len(indicator):
        final_length = length
    else:
        final_length = length - len(indicator)

    if len(text) > length:
        text = text[:final_length] + indicator

    return text


def simplify_error(text, whitespace = string.whitespace, delete = ""):
    """
    :param text:
    :param whitespace:
    :param delete:
    :return: return the text with multiple spaces reduced to single spaces

>>> simplify('''this   and that \t to''')
'this and that to'
>>> simplify('''   Washington  D.C.  ''')
'Washington D.C.'
>>> simplify(" abcdefghi ", delete = "abhi ")
'cdefg'
    """

    result = []
    words = []
    for char in text:
        if char in delete:
            continue
        elif char in whitespace:
            if words:
                result.append(words)
            words = ""

        else:
            words += char

        if words:
            result.append(words)

    return " ".join(result)
#>>> simplify_error("this   and\n that\t to")
#t th thi this this a an and and t th tha that that t to

def simplify(text, whitespace = string.whitespace, delete = ""):
    """
    :param text:
    :param whitespace:
    :param delete:
    :return: return the text with multiple spaces reduced to single spaces

>>> simplify('''this   and that\t to''')
'this and that to'
>>> simplify('''   Washington  D.C.''')
'Washington D.C.'
>>> simplify(" abcdefghi ", delete = "abhi ")
'cdefg'
    """

    result = []
    words = ""
    for char in text:
        if char in delete:
            continue
        elif char in whitespace:
            if words:
                result.append(words)
                words = ""
        else:
            words += char

    if words:
        result.append(words)

    return " ".join(result)

if __name__ == '__main__':

    import doctest
    doctest.testmod()