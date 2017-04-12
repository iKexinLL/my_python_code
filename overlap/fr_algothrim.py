#encoding=utf-8

'''
Created on 2015年12月28日

@author: xukexin01
没有边界,随着迭代次数的增加,可能整体像某个位置进行偏移
'''

import networkx as nx
import random
#import numpy as np
import math
import matplotlib.pyplot as plt
import sys

li = [(1,2),(1,3),(3,4),(3,5),(3,6),(3,7),(1,8),(8,9),(8,10),(8,11),(8,12)]
G = nx.Graph()
 
#===============================================================================
# for i in range(100):
#     a = random.randint(0,50)
#     b = random.randint(0,50)
#     if a != b:
#         G.add_node(a,{'size':float('%.4f'%(random.random()/10))})
#         G.add_node(b,{'size':float('%.4f'%(random.random()/10))})
#         G.add_edge(a,b)
#===============================================================================
     
for i in li:
    G.add_node(i[0],{'size':float('%.4f'%(random.random()/10))})
    G.add_node(i[1],{'size':float('%.4f'%(random.random()/10))})
    G.add_edge(i[0],i[1])
        
        
W = 1
H = 1


area = W * H

k = math.sqrt(area/len(G))

def calculate_cc_distance(posA,posB): #计算两个圆心间的距离
    xa,ya = posA
    xb,yb = posB
    return math.hypot((xa-xb), (ya-yb))

def calculate_distance(info_Graph,a,b):
    xa,ya = info_Graph[a]['pos']
    xb,yb = info_Graph[b]['pos']
    ra = info_Graph[a]['size']
    rb = info_Graph[b]['size']
    
    return  math.sqrt((xa-xb)**2+(ya-yb)**2) + ra + rb


def gravitation(k,duv): #u,v的吸引力
    gra_f_uv = (duv ** 2)/k
    return gra_f_uv


def repulsive(k,duv):
    rep_f_uv = (k ** 2)/duv
    return rep_f_uv

dim = 2

pos=np.asarray(np.random.random((len(G),dim)),dtype=np.float)

#pos = nx.spring_layout(G)
it = iter(pos)
info_Graph = {}
for a,b in G.node.items():  
    info_Graph[a] = {'size':b['size'],'pos':next(it),'disp':0}
    
def return_min_array(arr1,arr2):
    res = np.array([0,0],dtype=np.float)
    if arr1[0] > arr2[0]:
        res[0] = arr2[0]
    else:
        res[0] = arr1[0]
    
    if arr1[1] > arr2[1]:
        res[1] = arr2[1]
    else:
        res[1] = arr1[1]
    return res

iterations = 300
t = np.asarray((0.5,0.5))
for iteration in range(iterations):
    for a,b in info_Graph.items():
        info_Graph[a]['disp'] = np.asarray((0,0))
        #计算排斥力
        for m, n in info_Graph.items():
            if m != a:
                #计算两个节点的位置差
                position_a_m = b['pos'] - n['pos']
                #计算两个节点的距离
                distance_a_m = calculate_cc_distance(b['pos'],n['pos'])
                #计算点a的偏移量
                disp_a = b['disp'] + (position_a_m/distance_a_m) * repulsive(k,distance_a_m)
                
                info_Graph[a]['disp'] = disp_a
        
        #计算吸引力
    for u,v in G.edges():
        #计算两个节点的位置差
        position_u_v = info_Graph[u]['pos'] - info_Graph[v]['pos']
        #计算两个节点的距离
        distance_u_v = calculate_cc_distance(info_Graph[u]['pos'], info_Graph[v]['pos'])
        info_Graph[u]['disp'] = info_Graph[u]['disp'] - (position_u_v/distance_u_v) * gravitation(k,distance_u_v)
        info_Graph[v]['disp'] = info_Graph[v]['disp'] + (position_u_v/distance_u_v) * gravitation(k,distance_u_v)

    #print(info_Graph)
    for a,b  in info_Graph.items():
                #设置最小的移动路径
        disp_a = np.where(disp_a < 0.01,0.01,disp_a)
        pos_k = b['pos'] + (b['disp']/abs(b['disp'])) * t

        info_Graph[a].update({'pos':np.array(pos_k)})
        
            
    t = 0.8 * t        
            
            
pos3 = {}
for a,b in info_Graph.items():
    pos3[a] = b['pos']                
            
            
fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(111)
for k,v in info_Graph.items():
    #circ = plt.Circle(v['pos'],v['size'],alpha=0.7)
    circ = plt.Circle(v['pos'],0.01,alpha=0.7)
    ax.add_patch(circ)
ax.autoscale()
nx.draw_networkx_edges(G,pos3,alpha=0.3)
nx.draw_networkx_labels(G,pos3)
plt.show()            
            
            
    
    
    
    
        