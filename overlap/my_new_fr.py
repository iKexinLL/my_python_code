#encoding=utf-8
"""
Created on 2016/3/24 10:45
author: iKexinLL
先只利用质点进行计算
pos = nx.random_layout 的范围为 (1,1)
"""

import networkx as nx
from random import random
import math
import matplotlib.pyplot as plt
import sys
import numpy as np


li = [(1, 2), (1, 3), (3, 4), (3, 5), (3, 6), (3, 7), (1, 8), (8, 9), (8, 10), (8, 11), (8, 12)]
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
    G.add_node(i[0])
    G.add_node(i[1])
    G.add_edge(i[0], i[1])


def calculate_cc_distance(posA, posB): #计算两个圆心间的距离
    return math.hypot((posA[0] - posB[0]), (posA[1] - posB[1]))


def gravitation(k, duv): #u,v的吸引力
    return (duv * duv) / k


def repulsive(k, duv):
    return (k * k) / duv


def my_fr_layout(G, iterations = 50, if_draw = False):

    W = 1
    L = 1
    area = W * L
    k = math.sqrt(area / nx.number_of_nodes(G))

    for v in nx.nodes_iter(G):
        G.node[v]['x'] = random()
        G.node[v]['y'] = random()

    iterations = iterations

    t = 1 / 10
    dt = t / (iterations + 1)

    for i in range(iterations):

        print("iter {0}".format(i))

        if if_draw:
            pos = {}
            for v in G.nodes_iter():
                pos[v] = [G.node[v]['x'], G.node[v]['y']]

            plt.close()
            plt.ylim([-0.1, 1.1])
            plt.xlim([-0.1, 1.1])
            plt.axis('off')
            nx.draw_networkx(G, pos = pos, node_size = 10, width = 0.1, with_labels = False)
            plt.savefig("pic/{0}.png".format(i))

        #计算排斥力
        for v in G.nodes_iter():

            G.node[v]['dx'] = 0
            G.node[v]['dy'] = 0

            for u in G.nodes_iter():
                if u != v:

                    #计算两个节点的位置差
                    dx = G.node[v]['x'] - G.node[u]['x']
                    dy = G.node[v]['y'] - G.node[u]['y']

                    #计算两个节点的距离
                    distance_u_v = math.hypot(dx, dy)

                    #计算点a的偏移量
                    if distance_u_v != 0:
                        d = repulsive(k, distance_u_v) / distance_u_v
                        G.node[v]['dx'] += dx * d
                        G.node[v]['dy'] += dy * d

        #计算吸引力
        for u, v in G.edges_iter():

            #计算两个节点的位置差
            dx = G.node[v]['x'] - G.node[u]['x']
            dy = G.node[v]['y'] - G.node[u]['y']
            #计算两个节点的距离
            distance_u_v = math.hypot(dx, dy)

            if distance_u_v != 0:
                d = gravitation(k, distance_u_v) / distance_u_v
                _dx = dx * d
                _dy = dy * d
                G.node[v]['dx'] += -_dx
                G.node[v]['dy'] += -_dy
                G.node[u]['dx'] += +_dx
                G.node[u]['dy'] += +_dy

        #print(graph_info)
        for v in G.nodes_iter():

            dx = G.node[v]['dx']
            dy = G.node[v]['dy']

            disp = math.hypot(dx, dy)

            if disp != 0:

                d = min(disp, t) / disp
                x = G.node[v]['x'] + dx * d
                y = G.node[v]['y'] + dy * d

                x = min(W, max(0, x)) - W / 2
                y = min(L, max(0, y)) - L / 2
                G.node[v]['x'] = min(math.sqrt(W * W / 4 - y * y), max(-math.sqrt(W * W / 4 - y * y), x)) + W / 2
                G.node[v]['y'] = min(math.sqrt(L * L / 4 - x * x), max(-math.sqrt(L * L / 4 - x * x), y)) + L / 2

        t -= dt


        pos = {}
        for v in G.nodes_iter():
            pos[v] = [G.node[v]['x'], G.node[v]['y']]

    if if_draw:
        plt.close()
        plt.ylim([-0.1, 1.1])
        plt.xlim([-0.1, 1.1])
        plt.axis('off')
        nx.draw_networkx(G, pos = pos, node_size = 10, width = 0.1, with_labels = False)
        plt.savefig("pic/{0}.png".format(i + 1))

    return pos



G = nx.random_partition_graph(range(10), 0.3, 0.3)
pos = my_fr_layout(G)
plt.close()
plt.ylim([-0.1, 1.1])
plt.xlim([-0.1, 1.1])
plt.axis('off')
nx.draw_networkx(G, pos = pos, node_size = 10, width = 0.1, with_labels = False)
plt.savefig("pic/orig.png")
plt.show()
