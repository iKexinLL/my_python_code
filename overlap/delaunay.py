#encoding=utf-8
"""
Created on 2016/2/4 17:25
author: iKexinLL
direction: 尝试使用德劳内三角形进行计算
"""

import networkx as nx
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

G = nx.Graph()

#添加节点和边
nodes = {1: {'size': 1},2: {'size': 2},3: {'size': 2},4: {'size': 5},
 5: {'size': 3},6: {'size': 9},7: {'size': 0},8: {'size': 5},9: {'size': 2},
 10: {'size': 7},11: {'size': 3},12: {'size': 7}}

edges = [(1, 8),(1, 2),(1, 3),(3, 4),(3, 5),(3, 6),(3, 7),(8, 10),
 (8, 11),(8, 12),(8, 9)]

for k,v in nodes.items():
    G.add_node(k,v)
G.add_edges_from(edges)
pos = nx.pygraphviz_layout(G)
nx.draw(G,pos)
plt.show()
#输入位置
