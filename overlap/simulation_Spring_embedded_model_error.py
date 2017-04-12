#encoding=utf-8

'''
Created on 2015年12月28日

@author: xukexin01
简单模拟一下Spring—Embedded Model
复杂度为O(n^3)
'''

import networkx as nx
import random
import numpy as np 
import matplotlib.pyplot as plt

G = nx.Graph()
for i in range(100):
    a = random.randint(0,50)
    b = random.randint(0,50)
    if a != b:
        G.add_node(a,{'size':float('%.4f'%random.random())/10})
        G.add_node(b,{'size':float('%.4f'%random.random())/10})
        G.add_edge(a,b)
    
dim = 2
shape = (len(G), dim)

#pos = np.random.random(shape)

nnodes = shape[0]

#将点和对应的下标放入字典内
nodelist = G.nodes()
nlen=len(nodelist)
index=dict(zip(nodelist,range(nlen)))  #index中存入的就是{节点a:下标a,节点b:下标b}
#初始化一个大小为图大小的矩阵,将边边之间的关系用矩阵的方式存储
M = np.zeros((nlen,nlen),dtype=np.float) + np.nan #初始化一个值为nan,大小为 nlen*nlen 的矩阵,根据networkx改写
for k,v in G.adjacency_iter():
    for m,n in v.items():
        M[index[k],index[m]] = 1  #对应上面的index

M[np.isnan(M)] = 0.0  #将其余nan置为0.0,

pos=np.asarray(np.random.random((nnodes,dim)),dtype=np.float)
#pos = nx.spring_layout(G)
it = iter(pos)
circle = {}
for k,v in G.node.items():  
    circle[k] = {'size':v['size'],'pos':next(it)}
      
pos = dict(zip(G,pos))
distance_between_nodes = {}
for k, v in circle.items():
    xa = v['pos'][0]
    ya = v['pos'][1]
    for m, n in circle.items():
        if k == m :
            continue
        xb = n['pos'][0]
        yb = n['pos'][1]
        sr = (G.node[k]['size']+G.node[m]['size'])
        if xa == xb:
            xb = xb+xb/100
        if ya == yb:
            yb = yb + yb/100
        distance_between_nodes.update({(k,m):max(min(sr/abs(xa-xb),(sr/abs(ya-yb))),1)})
        
        



fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(111)
for k,v in circle.items():
    circ = plt.Circle(v['pos'],v['size'],alpha=0.7)
    ax.add_patch(circ)
ax.autoscale()
nx.draw_networkx_edges(G,pos,alpha=0.3)
nx.draw_networkx_labels(G,pos)
plt.show()


#===============================================================================
# for i in range(15):
#     a = random.randint(1,10)
#     b = random.randint(1,10)
#     if a != b:
#         G.add_edge(a,b)
#===============================================================================
        
        

