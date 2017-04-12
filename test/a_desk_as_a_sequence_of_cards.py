#encoding=utf-8
"""
Created on 2016/7/18 16:05
author: iKexinLL
"""

import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]


    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]
