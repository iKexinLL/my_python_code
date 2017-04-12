# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 09:59:19 2016

@author: xukexin01
@attention
"""

import networkx as nx
#import random
import numpy as np 
import matplotlib.pyplot as plt

'''
先创建几个图测试一下
我觉得还是要用plt画图,所以节点大小应该在[1,10)内
size为圆的半径
E:\学习文档\网络-布局算法\APVIS05-UsingSpringToRemoveNodeOverlapping.pdf
'''

G = nx.Graph()
nodes = {1: {'size': 1},2: {'size': 2},3: {'size': 2},4: {'size': 5},
 5: {'size': 3},6: {'size': 9},7: {'size': 0},8: {'size': 5},9: {'size': 2},
 10: {'size': 7},11: {'size': 3},12: {'size': 7}}
 
edges = [(1, 8),(1, 2),(1, 3),(3, 4),(3, 5),(3, 6),(3, 7),(8, 10),
 (8, 11),(8, 12),(8, 9)]

G = nx.Graph()
for k,v in nodes.items():
    G.add_node(k,v)
G.add_edges_from(edges)

dim = 2
#pos=np.asarray(np.random.random((len(G),dim)) * 30,dtype=np.float)
pos = np.array([[  2.44884149,  15.57364831],
       [ 27.96154684,  28.81867837],
       [ 16.06149927,  11.84425066],
       [ 14.34535351,   6.85417308],
       [ 28.95343848,  14.76803812],
       [  3.71652313,  26.9861553 ],
       [  9.15293294,  20.59768012],
       [ 16.04026516,   0.64657496],
       [ 10.88754725,  26.72494111],
       [ 14.06244131,   3.73882726],
       [ 16.76772381,   0.87093988],
       [ 20.61774731,  27.81145559]])
#pos = nx.spring_layout(G)
it = iter(pos)
info_Graph = {}
for a,b in G.node.items():  
    info_Graph[a] = {'size':b['size'],'pos':next(it),'disp':0}

#从现在开始,用info_Graph计算就可以了
'''
Suppose a node v∈V has
the positions (x0v,yv0 ) and (xv,yv) in the drawings of
Γ0 and Γ respectively. Then Γ0 preserves the mental
map of Γ if for ∀u ∈V,
• x0v < x0u ⇔ xv < xu, and
• yv0 < yu0 ⇔ yv < yu, and
• x0v = x0u ⇔ xv = xu, and
• yv0 = yu0 ⇔ yv = yu
They then propose three requirements for a layout
adjustment:
1. The adjusted(调整过的) drawing should be compact(紧凑,简洁).
2. Node images should be disjoint.
3. The mental(精神) map should be preserved(被保护) during interaction(相互作用).
(应该是mental map的结构)
'''
'''
首先给定一个两点间的合适距离 k = 3
然后计算两点间应有的距离 k' = l1 + l2 + m
l1 为点a的外切矩形的对角线的一半 sqrt(2) * ra
l2 为点b的外切矩形的对角线的一半 sqrt(2) * rb
kd = max(k,k')
那么
 吸引力 attractive fa = d/kd
 排斥力 repulsive  fr = (kd/d)**2

'''


def calculate_cc_distance(posA,posB): #计算两个圆心间的距离
    xa,ya = posA
    xb,yb = posB
    return np.sqrt((xa-xb)**2+(ya-yb)**2)
    
iterations = 30
t = np.asarray((0.5,0.5))
for iteration in range(iterations):
    for a,b in info_Graph.items():
        info_Graph[a]['disp'] = np.asarray((0,0))
        for m, n in info_Graph.items():
            if m != a:
                #计算两点合适距离
                k1 = np.sqrt(2) * v['size'] + np.sqrt(2) * n['size'] + 1
                kd = max(2,k1)
                #计算两个节点的位置差
                position_a_m = b['pos'] - n['pos']
                #计算两个节点的距离
                distance_a_m = calculate_cc_distance(b['pos'],n['pos'])
                #引力 
                fa = distance_a_m/kd
                #斥力
                fr = (kd/distance_a_m) ** 2
                #计算点a,m的偏移量
                #计算排斥力
                disp_a = b['disp'] + (position_a_m/distance_a_m) * fr
                #disp_m = n['disp'] + (position_a_m/distance_a_m) * fa
                #计算吸引力
                info_Graph[a]['disp'] = info_Graph[a]['disp'] - (position_a_m/distance_a_m) * fa
                #info_Graph[m]['disp'] = info_Graph[m]['disp'] + (position_a_m/distance_a_m) * fa
        
            

                #disp_a = np.where(disp_a < 0.01,0.01,disp_a)        
                pos_k = b['pos'] + b['disp'] * t
                
                info_Graph[a].update({'pos':np.array(pos_k)})
                    
                t = 0.9 * t    
                #if m == 2:
                    
                    #print(info_Graph)







pos3 = {}
for a,b in info_Graph.items():
    pos3[a] = b['pos']      
    
    
    



fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(111)
for k,v in info_Graph.items():
    circ = plt.Circle(v['pos'],v['size'],alpha=0.7)
    #circ = plt.Circle(v['pos'],0.01,alpha=0.7)
    ax.add_patch(circ)
ax.autoscale()
#nx.draw_networkx_edges(G,pos3,alpha=0.3)
nx.draw_networkx_labels(G,pos3)
plt.show()      
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    