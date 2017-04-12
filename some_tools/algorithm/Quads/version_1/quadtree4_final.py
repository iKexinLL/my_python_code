#encoding=utf-8
"""
Created on 2016/3/30 17:27
author: iKexinLL
修正了test3的问题

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

    return (rect_nw, rect_ne, rect_sw, rect_se)





H = nx.Graph()
H.add_nodes_from(range(100))
pos = nx.random_layout(H)
rect = ((0, 0), init_weight, init_height)


G = nx.DiGraph()

def calc_point_number_in_rect(point, rect):

    for r in get_four_rect(rect):

        min_x = r[0][0]
        min_y = r[0][1]
        width = r[1]
        height = r[2]

        #判断point是否属于这个rect
        #如果属于,则判断这个rect中是否存在一个b_point
        #   如果存在则将这个rect分解为四个sub_rect,将这个b_point放入到sub_rect中
        #   将point也放入到sub_rect中
        #
        #如果不属于 pass
        #递归, 直到发现了一个从未发现过的rect
        if min_x <= point[1][0] < min_x + width and min_y <= point[1][1] < min_y + height:

            if r in G:
                b_point = [(k,pos[k]) for k,v in G.edge.get(r,None).items() if G.node[k]['attr'] == 'point']
                if b_point:
                    G.edge.get(r).pop(b_point[0][0])
                    calc_point_number_in_rect(b_point[0], r)
                    calc_point_number_in_rect(point, r)
                else:
                    calc_point_number_in_rect(point, r)
            else:
                G.add_node(point[0], attr = 'point')
                G.add_node(r, attr = 'rect')
                G.add_edge(r, point[0])
                G.add_edge(rect, r)



G.add_node(rect, attr = 'rect')

for k,v in pos.items():
    calc_point_number_in_rect((k, v), rect)

G.remove_nodes_from(nx.isolates(G))

npoint = [k for k, v  in G.node.items() if v['attr'] == 'point']
nrect = [k for k, v  in G.node.items() if v['attr'] == 'rect']

fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(111)
for rec in nrect:
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