#encoding=utf-8
"""
Created on 2016/3/18 18:44
author: iKexinLL
"""


import networkx as nx
import random

G = nx.Graph()

for i in range(300000):
    G.add_node(i, weight = random.choice([1,2,3,4]))
