#encoding=utf-8
"""
Created on 2016/3/29 14:54
author: iKexinLL
每个节点开始的时候都将根正方形rect传入到calc_point_number_in_rect中,
分解rect为四个sub_rect
在calc_point_number_in_rect中, 计算rect属于哪个sub_rect
然后判断sub_rect中是否存在节点,
1.如果存在,获取这个sub_rect中的节点,将这个sub_rect分解为sub_sub_rect,
重新放入节点,然后在计算传入节点的所属的sub_sub_rect
2.如果不存在,则将这个节点放入到sub_rect中
"""

import networkx as nx

class Quad(object):

    def __init__(self, pos, w = 1, h = 1):

        init_weight = w
        init_height = h

        self.G = nx.DiGraph()
        self.G.add_node('root')

        for k,v in pos.items():
            self.calc_point_number_in_rect((k,v), ((0, 0), init_weight, init_height), 0)



    def calc_point_number_in_rect(self, pos, rect, depth = None):

        for r in self.get_four_rect(rect):

            min_x = r[0][0]
            min_y = r[0][1]
            width = r[1]
            height = r[2]

            #判断point是否属于这个rect
            if min_x < pos[1][0] < min_x + width and min_y < pos[1][1] < min_y + height:
                #如果属于,则判断这个rect中是否存在一个b_point
                #如果存在则将这个rect分解为四个sub_rect,将这个b_point放入到sub_rect中
                #将point也放入到sub_rect中
                b_point = [v for k,v in G.edge.get(r).items() if v['attr'] == 'point']
                if b_point:
                    self.G.edge.get(r).pop(b_point[0])
                    self.calc_point_number_in_rect(b_point, r)
                    self.calc_point_number_in_rect(pos, r)


                self.G.add_edge(rect, pos)


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

if __name__ == '__main__':
    import networkx as nx
    import matplotlib.pyplot as plt
    from matplotlib import patches


    G = nx.Graph()
    G.add_nodes_from(range(100))
    pos = nx.random_layout(G)
    #pos = {0: (0.25, 0.25), 1: (0.6, 0.6), 2: (0.64, 0.64)}
    t = Quad(pos)
