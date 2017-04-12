#encoding=utf-8
"""
Created on 2016/3/31 9:44
author: iKexinLL
利用类和列表储存这个树,
根据目前的数据格式(匿名):id, name
创建格式如下: id, name, pos, children, is_leaf
"""

class Quad(object):

    def __init__(self, node):

        self.id = node['id']
        self.name = node['name']
        self.pos = node['pos']
        self.children = []
        self.is_leaf = False


class Node(object):
    """
    读取json文件, 并将里面的内容进行计算
    """

    def __init__(self, path = 'F:\\networkx_json\\ceshi.json'):
        import json
        import random

        #这里gkb才好用, 是数据问题
        with open(path, encoding = 'gbk') as f:
            json_data = json.loads(f.read())

        entityList = json_data['entityList']

        for i in entityList:
            i.update({'pos':[random.random(), random.random()]})

        self.nodes = entityList

class CalcQuadTree(object):

    def __init__(self, node, w = 1, h = 1):

        self.node = node
        self.quad_tree = []

        init_rect = ((0, 0), w, h)

        self.quad_tree.append(init_rect)

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

        return (rect_nw, rect_ne, rect_sw, rect_se)


    def calc_point_number_in_rect(self, point, rect):
        for r in self.get_four_rect(rect):

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

                if r in self.__graph_for_tree:
                    b_point = [(k,self.__pos[k]) for k,v in self.__graph_for_tree.edge.get(r,None).items() if self.__graph_for_tree.node[k]['attr'] == 'point']
                    if b_point:
                        self.__graph_for_tree.edge.get(r).pop(b_point[0][0])
                        self.calc_point_number_in_rect(b_point[0], r)
                        self.calc_point_number_in_rect(point, r)
                    else:
                        self.calc_point_number_in_rect(point, r)
                else:
                    self.__graph_for_tree.add_node(point[0], attr = 'point')
                    self.__graph_for_tree.add_node(r, attr = 'rect')
                    self.__graph_for_tree.add_edge(r, point[0])
                    self.__graph_for_tree.add_edge(rect, r)