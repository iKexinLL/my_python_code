#encoding=utf-8
"""
Created on 2016/4/1 15:25
author: iKexinLL
为节点添加 质量weight, 位移displacement, 速度speed, 层级depth
是否要用list存储?
根据 http://xueshu.baidu.com/s?wd=paperuri%3A%28a378548e4c41886142f33a1941edc155%29&filter=sc_long_sign&tn=SE_xueshusource_2kduw22v&sc_vurl=http%3A%2F%2Fwenku.baidu.com%2Fview%2F3e49ec6f1eb91a37f1115c0a.html&ie=utf-8
上的论文, 其需要从上至下和从下至上进行遍历
也不用, G 完全可以实现这个
先不算 size
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math


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


def calc_point_number_in_rect(point, rect):

    for rect_direction, sub_rect in get_four_rect(rect).items():

        min_x = sub_rect[0][0]
        min_y = sub_rect[0][1]
        width = sub_rect[1]
        height = sub_rect[2]

        # 判断point是否属于rect中的一个sub_rect
        # 如果属于
        #     判断sub_rect是否已经在G中,在G中(则表示曾经有点在这个sub_rect中,但现在已经被分割)
        #       如果存在
        #           重新计算point在sub_rect
        #
        #       如果不存在
        #           判断rect中的这个sub_rect是否存在点b_point
        #               如果存在
        #                   则在rect中删除rect_direction中的那个属性(把b_point从那个rect中删除)
        #                   删除rect和point的关系 edge
        #                   减少rect中的weight
        #                   在G中添加一个rect节点
        #                   添加rect和sub_rect的关系
        #                   b_point的depth - 1
        #                   在sub_rect中重新计算point和b_point
        #
        #              如果不存在
        #                   则在G中添加一rect的点
        #                   属性rect_direction(nw, ne, sw, se),表明这个方向上存在点b_point
        #                   属性weight为其所包含的所有点的weight的总和
        #                   在G中添加一个point, 属性为对应H的点的属性, depth += 1
        #                   添加rect和point的关系 edge
        #   添加节点的depth
        #

        if min_x <= point[1][0] < min_x + width and min_y <= point[1][1] < min_y + height:

            if sub_rect in G:
                #
                calc_point_number_in_rect(point, sub_rect)
                #G.node[point[0]]['depth'] += 1
                G.node[rect]['weight'] += H.node[point[0]]['weight']
            else:
                b_point = G.node[rect]['rect_direction'].pop(rect_direction, None)
                if b_point:
                    G.remove_edge(rect, b_point[0])
                    G.node[rect]['weight'] += H.node[point[0]]['weight']
                    sub_depth = G.node[rect]['depth']
                    G.add_node(sub_rect, attr = 'rect', rect_direction = {}, weight = 0, depth = sub_depth + 1)
                    G.add_edge(rect, sub_rect)

                    #G.node[point[0]]['depth'] += 1
                    #H.node[point[0]]['depth'] += 1
                    calc_point_number_in_rect(b_point, sub_rect)
                    calc_point_number_in_rect(point, sub_rect)
                    #G.node[b_point[0]]['depth'] += 1
                    #G.node[point[0]]['depth'] += 1
                else:
                    point_info = H.node[point[0]]
                    #point_info['depth'] += 1
                    G.add_node(point[0], point_info)
                    G.node[rect]['rect_direction'][rect_direction] = point
                    G.node[rect]['weight'] +=  point_info['weight']
                    G.add_edge(rect, point[0])
                    all_sub_rect.append(sub_rect)
                    #break
            G.node[point[0]]['depth'] += 1
            break

init_weight = init_height = 1000

H = nx.Graph()
scale = init_height
#为节点添加 质量weight, 位移displacement, 速度speed, 层级depth
for i in range(100):
    H.add_node(i,
               pos = np.random.random(2) * scale,
               weight = np.random.randint(1, 10),
               disp = (0, 0),
               speed = 0,
               depth = 0,
               attr = 'point')

root_rect = ((0, 0), init_weight, init_height)


G = nx.DiGraph()
all_sub_rect = [] #用于画出format图


G.add_node(root_rect, attr = 'rect', rect_direction = {}, weight = 0, depth = 0)

pos = {}
for k,v in H.node.items():
    pos[k] = v['pos']

for k,v in pos.items():
    calc_point_number_in_rect((k, v), root_rect)

the_points = [k for k, v  in G.node.items() if v['attr'] == 'point']
the_rects = [k for k, v  in G.node.items() if v['attr'] == 'rect']

# posg = nx.drawing.nx_agraph.pygraphviz_layout(G, 'dot')
# nx.draw_networkx_nodes(G, posg, nodelist=the_points,node_color='y', node_size = 165)
# nx.draw_networkx_nodes(G, posg, nodelist=the_rects,node_color='b',node_size=65)
# nx.draw_networkx_edges(G, posg)
# nx.draw_networkx_labels(H, posg)
# plt.show()

# fig = plt.figure(figsize = (10,10))
# ax = fig.add_subplot(111)
# for rec in all_sub_rect:
#     r = plt.Rectangle(rec[0], rec[1], rec[2], fill = False)
#     ax.add_patch(r)
# for p in the_points:
#     circ = plt.Circle(pos[p], G.node[p]['weight']/5, alpha = 0.6)
#     circ.set_facecolor('b')
#     ax.add_patch(circ)
# plt.xlim(0, 100)
# plt.ylim(0, 100)
# plt.show()


#现在 G 就为生成好的树了
#也就是现在在G中, 利用力算法, 计算disp(这个应该是偏移量, 然后移动的距离为 disp * speed)
#需要一个获取rect内总weight的方法

#theta = 1
#d为点所在的rect的长度, r为到rect中心的距离
#根据 http://arborjs.org/docs/barnes-hut 这里的说明,计算每个点的偏移量


def calc_distance(point_one, point_two):
    #计算两个点之间的距离
    return math.hypot(point_one[0] - point_two[0],
                      point_one[1] - point_two[1])
def get_children(G, rect):
    return G[rect]



def update_net_force(rect):
    for sub in G[rect]:
        if G.node[sub].get('attr') == 'point':
            print(sub)
            #计算当前节点与center_point的力
            #假设为吸引力,距离越近,吸引力越大
            distance = calc_distance(G.node[sub]['pos'], root_rect[0])
            r = root_rect[1]

            G.node[sub]['disp'][0] = root_rect[0][0] - G.node[sub]['pos'][0]
            G.node[sub]['disp'][1] = root_rect[0][1] - G.node[sub]['pos'][1]

            print('%s is a point'%sub)
            #开始计算这个c与其他每个节点的力
            calc_the_force(sub, root_rect, center_dx, center_dy)
            break
        else:
            update_net_force(sub)


def calc_the_force(point, rect, center_dx, center_dy):

    #计算当前节点与每个rect的力关系
    for sub in G[rect]:
        if G.node[sub].get('attr') == 'rect':
            d = sub[1]
            r = math.hypot(G.node[point]['pos'][0] - sub[0][0],
                           G.node[point]['pos'][1] - sub[0][1])


            if d / r > 0.5:
                #将rect看做整体计算
                G.node[sub]['disp'][0] += G.node[point]['pos'][0] - sub[0][0]
                G.node[sub]['disp'][1] += G.node[point]['pos'][1] - sub[0][1]
            else:
                #计算rect中每个点的力
                calc_the_force(point, sub, center_dx, center_dy)

