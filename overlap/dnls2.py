# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 09:59:19 2016

@author: xukexin01
"""

'''
经过这么测试,在点少于20个情况下比较好用
注意 num_of_nodes 的值
key_dis 也要注意 这个值不能太小,跟节点size,和个数有关
t的 值也是,与节点大小有关~~
总之,现在的这个方法没有一个完整的对于参数的定义
'''
#import networkx as nx
#import random
#import numpy as np 
#import matplotlib.pyplot as plt

'''
先创建几个图测试一下
我觉得还是要用plt画图,所以节点大小应该在[1,10)内
size为圆的半径
'''

import os
import json
#import pandas as pd 
import networkx as nx
#import copy
import numpy as np
import matplotlib.pyplot as plt
import random
#from string import ascii_uppercase
#import codecs as cs

G = nx.Graph()
num_of_nodes = 400
for i in range(num_of_nodes):
    G.add_node(i,{'size':random.randint(5,100),'pos':np.asarray((np.random.random(),np.random.random()))})

key_dis = 2000
t = np.asarray((200,200))

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

di = {}

def calculate_cc_distance(posA,posB): #计算两个圆心间的距离
    xa,ya = posA
    xb,yb = posB
    return np.sqrt((xa-xb)**2+(ya-yb)**2)
    
def attractive(kd,distance_a_m): #u,v的吸引力
    a_f_uv = distance_a_m/kd
    return a_f_uv


def repulsive(kd,distance_a_m):
    rep_f_uv = (kd/distance_a_m) ** 2 
    return rep_f_uv

#path  = r'

#pos = nx.spring_layout(G)
#it = iter(pos)
info_Graph = {}
for a,b in G.node.items():
    info_Graph[a] = {'size':b['size'],'pos':b['pos'],'disp':0}
    
overlap = True
iterations = 50
iteration = 0

for iteration in range(iterations):
    #iteration += 1
    for a,b in info_Graph.items():
        info_Graph[a]['disp'] = np.asarray((0,0))
        a_disp = np.asarray((0,0))
        #计算排斥力
        for m, n in info_Graph.items():
            if m != a:
                #计算两点合适距离
                #k1 = np.sqrt(2) * b['size'] + np.sqrt(2) * n['size'] + 1
                k1 = b['size'] + n['size'] + key_dis
                kd = max(20,k1)
                #计算两个节点的位置差
                position_a_m = b['pos'] - n['pos']
                #计算两个节点的距离
                distance_a_m = calculate_cc_distance(b['pos'],n['pos'])
                #计算点a的偏移量
                if distance_a_m < kd:
                    #print('斥力',(a,b))
                    b['disp'] = b['disp'] + (position_a_m/distance_a_m) * repulsive(kd,distance_a_m)
                #计算吸引力
                if distance_a_m > kd:
                    b['disp'] = b['disp'] - (position_a_m/distance_a_m) * attractive(kd,distance_a_m)
                
    for m,n in info_Graph.items():
        pos_k = n['pos'] + (n['disp']/abs(n['disp'])) * t
        info_Graph[m].update({'pos' : np.array(pos_k)})

    t = 0.7 * t   

#print(iteration)




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
#nx.draw_networkx_labels(G,pos3)
plt.show()      
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    