#!/usr/bin/python
# coding=utf-8

"""
__time__ = '2018/5/12 15:23'
__author__ = 'Kexin Xu'
"""
import math


class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.__value = "self.__value"
        self.t = x

        print(__file__)

    def distance_from_origin(self):
        return math.hypot(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "Point({0.x}, {0.y})".format(self)

    def __str__(self):
        return "{0.x!r}, {0.y!r}".format(self)

    @property
    def print_self_value(self):
        return self.__value