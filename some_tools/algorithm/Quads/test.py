#encoding=utf-8
"""
Created on 2016/3/23 13:48
author: iKexinLL

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

class QuadTree(object):
    """
    传入一个点坐标集合, 输出为一个长方形集合
    然后将长方形分为四个 subr_nw,subr_ne,subr_sw,subr_se,
    如果subr中的点数大于1,则将这个subr放入到draw_rect中,
    利用循环解决, 因为我的最终目的是输入一个可以画出的正方形
    """

    def __init__(self, pos, w = 1, h = 1):
        """
        :param pos: 传入的是点坐标的集合, 根据点坐标进行分四叉树
        :param rect: pos所在的长方形 (x,y), width, height
        :return:
        """

        self.num = 0
        init_weight = w / 2
        init_height = h / 2

        self.out_put_rectangle = set()
        self.the_center_point = {}

        #生成初始的四个长方形

        subr_nw = ((0, init_height), init_weight, init_height)
        subr_ne = ((init_weight, init_height), init_weight, init_height)
        subr_sw = ((0, 0), init_weight, init_height)
        subr_se = ((init_weight, 0), init_weight, init_height)

        self.out_put_rectangle.add(subr_nw)
        self.out_put_rectangle.add(subr_ne)
        self.out_put_rectangle.add(subr_sw)
        self.out_put_rectangle.add(subr_se)


        self.insert_center_point((0, 0), w, h)
        self.insert_center_point(subr_nw)
        self.insert_center_point(subr_ne)
        self.insert_center_point(subr_sw)
        self.insert_center_point(subr_se)


        self.calc_point_number_in_rect(pos, subr_nw)
        self.calc_point_number_in_rect(pos, subr_ne)
        self.calc_point_number_in_rect(pos, subr_sw)
        self.calc_point_number_in_rect(pos, subr_se)


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



    def calc_point_number_in_rect(self,pos, rect, depth = None):

        if depth is not None:
            depth = +1
        else:
            depth = 0


        for r in self.get_four_rect(rect):
            pos_in = {}
            min_x = r[0][0]
            min_y = r[0][1]
            width = r[1]
            height = r[2]
            for k, v in pos.items():
                if min_x < v[0] < min_x + width and min_y < v[1] < min_y + height:
                    pos_in[k] = v
                    self.out_put_rectangle.add(r)
            if len(pos_in) > 1:
                self.calc_point_number_in_rect(pos_in, r, depth)
                #pos_in = {}


    def insert_center_point(self, *rect):
        """
        :param rect: 
        :return: 
        """
        return True
        point = rect[0]
        
        self.the_center_point.setdefault(point, {})


if __name__ == '__main__':
    import networkx as nx
    import matplotlib.pyplot as plt
    from matplotlib import patches


    G = nx.Graph()
    G.add_nodes_from(range(10000))
    pos = nx.random_layout(G)
    #pos = {0: (0.25, 0.25), 1: (0.6, 0.6), 2: (0.64, 0.64)}
    t = QuadTree(pos)

    # fig = plt.figure(figsize = (7,7))
    # ax = fig.add_subplot(111)
    # for k,v in pos.items():
    #     circ = plt.Circle(v, 0.005, alpha = 1)
    #     ax.add_patch(circ)
    # for i in t.out_put_rectangle:
    #     p = patches.Rectangle(i[0], i[1], i[2], fill = False)
    #     ax.add_patch(p)
    #plt.subplots_adjust(bottom = 0, left = 0, right = 1, top = 1)
    print(len(t.out_put_rectangle))
    # ax.autoscale()
    # plt.xlim(0, 1)
    # plt.ylim(0, 1)
    # plt.show()
