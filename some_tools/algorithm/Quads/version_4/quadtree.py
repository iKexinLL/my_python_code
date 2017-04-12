#encoding=utf-8
"""
Created on 2016/4/7 16:33
author: iKexinLL
尝试使用结构进行计算
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
#     circ = plt.Circle(pos[p], 10, alpha = 0.6)
#     circ.set_facecolor('b')
#     ax.add_patch(circ)
# plt.xlim(0, 1000)
# plt.ylim(0, 1000)
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

#li = []

def update_net_force(rect):
    for sub in G[rect]:
        if G.node[sub].get('attr') == 'point':

            #计算当前节点与center_point的力
            #假设为吸引力,距离越近,吸引力越大
            distance = calc_distance(G.node[sub]['pos'], root_rect[0])
            roo_weight = G.node[root_rect]['weight']

            force = roo_weight / (distance * distance)

            G.node[sub]['disp'][0] = (1000 / 2 - G.node[sub]['pos'][0]) * force * 10
            G.node[sub]['disp'][1] = (1000 / 2 - G.node[sub]['pos'][1]) * force * 10
            #print(G.node[sub]['disp'])
            #print('%s is a point'%sub)
            #li.append(sub)
            #开始计算这个c与其他每个节点的力
            calc_the_force(sub, root_rect)

        else:
            update_net_force(sub)


def calc_the_force(point, rect):

    #计算当前节点与每个rect的力关系
    for sub in G[rect]:
        if G.node[sub].get('attr') == 'rect':
            d = sub[1]
            r = math.hypot(G.node[point]['pos'][0] - sub[0][0],
                           G.node[point]['pos'][1] - sub[0][1])

            if d / r > 0.5:
                #将rect看做整体计算
                rect_weight = G.node[rect]['weight']
                force = rect_weight / (r * r)
                G.node[point]['disp'][0] += (G.node[point]['pos'][0] - sub[0][0]) * force * 10
                G.node[point]['disp'][1] += (G.node[point]['pos'][1] - sub[0][1]) * force * 10
            else:
                #计算rect中每个点的力
                calc_the_force(point, sub)

        elif sub == point:
            continue

        else:
            sub_weight = G.node[sub]['weight']
            r = math.hypot(G.node[point]['pos'][0] - G.node[sub]['pos'][0],
                           G.node[point]['pos'][1] - G.node[sub]['pos'][1])

            force = sub_weight / (r * r)

            G.node[point]['disp'][0] += (G.node[point]['pos'][0] - G.node[sub]['pos'][0]) * force * 10
            G.node[point]['disp'][1] += (G.node[point]['pos'][1] - G.node[sub]['pos'][1]) * force * 10



def update_position():
    for i in the_points:
        G.node[i]['pos'] += G.node[i]['disp']
        G.node[i]['disp'] = [0, 0]




def init_the_method():

    init_weight = init_height = 1000

    H = nx.Graph()
    scale = init_height
#为节点添加 质量weight, 位移displacement, 速度speed, 层级depth
    for i in range(100):
        H.add_node(i,
                   pos = np.random.random(2) * scale,
                   weight = np.random.randint(1, 10),
                   disp = [0, 0],
                   speed = 0,
                   depth = 0,
                   attr = 'point')


    root_rect = ((0, 0), init_weight, init_height)

    return H, root_rect


H, root_rect = init_the_method()




for i in range(50):
    print(i)
    the_points = []
    the_rects = []
    all_sub_rect = [] #用于画出format图

    G = nx.DiGraph()
    G.add_node(root_rect, attr = 'rect', rect_direction = {}, weight = 0, depth = 0)

    for k,v in H.node.items():
        calc_point_number_in_rect((k, v['pos']), root_rect)

    for k,v in G.node.items():
        if v['attr'] == 'point':
            the_points.append(k)
        else:
            the_rects.append(k)

    plt.close()
    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(111)
    for rec in all_sub_rect:
        r = plt.Rectangle(rec[0], rec[1], rec[2], fill = False)
        ax.add_patch(r)
    for p in the_points:
        circ = plt.Circle(H.node[p]['pos'], 10, alpha = 0.6)
        circ.set_facecolor('b')
        ax.add_patch(circ)
    plt.ylim([-500, 1500])
    plt.xlim([-500, 1500])
    plt.axis('off')
    plt.savefig("pic/{0}.png".format(i))

    update_net_force(root_rect)
    update_position()