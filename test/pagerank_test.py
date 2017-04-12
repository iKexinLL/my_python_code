#encoding=utf-8
"""
Created on 2016/23/7 9:58
author: iKexinLL
direction: 确定图中的weight对于pangrank的影响
"""


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import pygraphviz_layout

G = nx.Graph()

for i in range(100):
    w = i if i > 85 else 1
    G.add_node(i, weight = w)

for i in range(200):
    a = np.random.randint(0, 100)
    b = np.random.randint(0, 100)
    w1 = G.node[a]['weight']
    w2 = G.node[b]['weight']
    if a != b:
        G.add_edge(a, b, weight = w1 + w2)



pos = pygraphviz_layout(G, 'sfdp')

pg = nx.pagerank_numpy(G)

pg_sorted = sorted(pg.items(), key = lambda x: x[1], reverse = True)

pg_top_ten_nodes = [x[0] for x in pg_sorted[:10]]

pg_ten_twenty_nodes = [x[0] for x in pg_sorted[11:21]]

fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(111)
for k,v in pos.items():
    circ = plt.Circle(v, 20, alpha = 1)
    if k > 85:
        color = 'r'
    else:
        color = 'b'
    circ.set_facecolor(color)
    ax.add_patch(circ)
#plt.subplots_adjust(bottom = 0, left = 0, right = 1, top = 1)
ax.autoscale()
nx.draw_networkx_edges(G, pos, alpha=0.4)
nx.draw_networkx_labels(G,pos)

fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(111)
for k,v in pos.items():
    circ = plt.Circle(v, 20, alpha = 1)
    if k in pg_ten_twenty_nodes:
        color = 'r'
    elif k in pg_top_ten_nodes:
        color = 'y'
    else:
        color = 'b'
    circ.set_facecolor(color)
    ax.add_patch(circ)
#plt.subplots_adjust(bottom = 0, left = 0, right = 1, top = 1)
ax.autoscale()
nx.draw_networkx_edges(G, pos, alpha=0.4)
nx.draw_networkx_labels(G,pos)

plt.show()
