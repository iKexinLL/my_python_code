#encoding=utf-8
"""
Created on 2016年3月31日11:37:11
author: iKexinLL
改进加边的逻辑

point_nw     |       point_ne
             |
    nw       |     ne
             |
-------------|----------------
             |
    sw       |     se
             |
             |
point_sw     |       point_se
"""

import networkx as nx
import matplotlib.pyplot as plt

w = h = 1

init_weight = w
init_height = h


def get_four_rect(rect):

    min_x = rect[0][0]
    min_y = rect[0][1]
    width = rect[1]
    height = rect[2]
    center_x = (min_x + min_x + width) * 0.5
    center_y = (min_y + min_y + height) * 0.5

    rect_nw = ((min_x, center_y), width * 0.5, height * 0.5)
    rect_ne = ((center_x, center_y), width * 0.5, height * 0.5)
    rect_sw = ((min_x, min_y), width * 0.5, height * 0.5)
    rect_se = ((center_x, min_y), width * 0.5, height * 0.5)

    return {'nw' : rect_nw, 'ne' : rect_ne, 'sw' : rect_sw, 'se' : rect_se}





H = nx.Graph()
H.add_nodes_from(range(100))
pos = nx.random_layout(H)



G = nx.DiGraph()
all_sub_rect = [] #用于画出format图

def calc_point_number_in_rect(point, rect):

    for rect_direction, sub_rect in get_four_rect(rect).items():

        min_x = sub_rect[0][0]
        min_y = sub_rect[0][1]
        width = sub_rect[1]
        height = sub_rect[2]

        # 判断point是否属于rect中的一个sub_rect
        # 如果属于
        #     判断rect中的这个sub_rect是否存在点b_point
        #       如果存在
        #           则在rect中删除rect_direction中的那个属性
        #             删除rect和point的关系
        #             添加rect和sub_rect的关系
        #             在sub_rect中重新计算point和b_point
        #       如果不存在
        #           则在G中添加一个属性rect_direction(nw, ne, sw, se),表明这个方向上存在点b_point
        #             添加rect和point的关系

        if min_x <= point[1][0] < min_x + width and min_y <= point[1][1] < min_y + height:
            if sub_rect in G:
                calc_point_number_in_rect(point, sub_rect)
            else:
                b_point = G.node[rect]['rect_direction'].pop(rect_direction, None)
                if b_point:
                    G.remove_edge(rect, b_point[0])
                    G.add_node(sub_rect, attr = 'rect', rect_direction = {})
                    G.add_edge(rect, sub_rect)
                    calc_point_number_in_rect(b_point, sub_rect)
                    calc_point_number_in_rect(point, sub_rect)
                else:
                    G.node[rect]['rect_direction'].update({rect_direction : point})
                    G.add_node(point[0], attr = 'point', pos = point[1])
                    G.add_edge(rect, point[0])
                    all_sub_rect.append(sub_rect)
                    break

rect = ((0, 0), init_weight, init_height)

G.add_node(rect, attr = 'rect', rect_direction = {})

for k,v in pos.items():
    calc_point_number_in_rect((k, v), rect)

G.remove_nodes_from(nx.isolates(G))

npoint = [k for k, v  in G.node.items() if v['attr'] == 'point']
nrect = [k for k, v  in G.node.items() if v['attr'] == 'rect']


fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(111)
for rec in all_sub_rect:
    r = plt.Rectangle(rec[0], rec[1], rec[2], fill = False)
    ax.add_patch(r)
for p in npoint:
    circ = plt.Circle(pos[p], 0.015, alpha = 0.6)
    circ.set_facecolor('b')
    ax.add_patch(circ)
plt.show()


posg = nx.drawing.nx_agraph.pygraphviz_layout(G, 'dot')
nx.draw_networkx_nodes(G, posg, nodelist=npoint,node_color='y', node_size = 95)
nx.draw_networkx_nodes(G, posg, nodelist=nrect,node_color='b',node_size=65)
nx.draw_networkx_edges(G, posg)
#nx.draw_networkx_labels(G, posg)
plt.show()