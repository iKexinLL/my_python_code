#encoding=utf-8
"""
Created on 2016/4/1 9:44
author: iKexinLL
"""
#encoding=utf-8
"""
Created on 2016/3/31 15:58
author: iKexinLL
"""

import networkx as nx
import matplotlib.pyplot as plt


class Quad(object):

    def __init__(self, pos, w = 1, h = 1):
        self.__graph_for_tree = nx.DiGraph()
        rect = ((0, 0), w, h)
        #添加根节点
        self.__graph_for_tree.add_node(rect, attr = 'rect', rect_direction = {})
        self.__pos = pos
        self.__all_tree_rect = []
        for k, v in pos.items():
            self.__calc_point_number_in_rect((k, v), rect)


    def get_four_rect(self, rect):
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


    def __calc_point_number_in_rect(self, point, rect):
        for rect_direction, sub_rect in self.get_four_rect(rect).items():

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
                if sub_rect in self.__graph_for_tree:
                    self.__calc_point_number_in_rect(point, sub_rect)
                else:
                    b_point = self.__graph_for_tree.node[rect]['rect_direction'].pop(rect_direction, None)
                    if b_point:
                        self.__graph_for_tree.remove_edge(rect, b_point[0])
                        self.__graph_for_tree.add_node(sub_rect, attr = 'rect', rect_direction = {})
                        self.__graph_for_tree.add_edge(rect, sub_rect)
                        self.__calc_point_number_in_rect(b_point, sub_rect)
                        self.__calc_point_number_in_rect(point, sub_rect)
                    else:
                        self.__graph_for_tree.node[rect]['rect_direction'].update({rect_direction : point})
                        self.__graph_for_tree.add_node(point[0], attr = 'point', pos = point[1])
                        self.__graph_for_tree.add_edge(rect, point[0])
                        self.__all_tree_rect.append(sub_rect)
                        break


    @property
    def tree_point(self):
        return [k for k, v in self.__graph_for_tree.node.items() if v['attr'] == 'point']

    @property
    def tree_rect(self):
        return [k for k, v in self.__graph_for_tree.node.items() if v['attr'] == 'rect']

    @property
    def pos(self):
        return self.__pos

    @property
    def graph_for_tree(self):
        return self.__graph_for_tree

    @property
    def all_tree_rect(self):
        return self.__all_tree_rect