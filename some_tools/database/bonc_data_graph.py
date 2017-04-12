#encoding=utf-8
"""
Created on 2016/8/19 9:34
author: iKexinLL
"""

import networkx as nx

info_file_path = r'E:\github\some_tools\database\graph_info.txt'

G = nx.DiGraph()

with open(info_file_path) as f:
    for lines in f.readlines():
        target,source = lines.split(' ')
        G.add_edge(target, source)



