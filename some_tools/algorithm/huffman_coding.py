#encoding=utf-8
"""
Created on 2016/3/10 16:20
author: iKexinLL
尝试编辑 哈夫曼编码
"""

#import struct #结构化成C语言结构 https://docs.python.org/3.4/library/struct.html#struct.pack
#import heapq  #heapq 是一个最小堆，堆顶元素 a[0] 永远是最小的. 和 Java 中的优先队列类似. https://docs.python.org/3.4/library/heapq.html
from heapq import heappush, heappop, heapify
from collections import defaultdict



# 实现霍夫曼树的方式有很多种，可以使用优先队列（Priority Queue）简单达成这个过程，
# 给与权重较低的符号较高的优先级（Priority），算法如下：
#
# ⒈把n个终端节点加入优先队列，则n个节点都有一个优先权Pi，1 ≤ i ≤ n
#
# ⒉如果队列内的节点数>1，则：
#
#   ⑴从队列中移除两个最大的Pi节点，即连续做两次remove（max(Pi）, Priority_Queue)
#   ⑵产生一个新节点，此节点为（1）之移除节点之父节点，而此节点的权重值为（1）两节点之权重和
#   ⑶把（2）产生之节点加入优先队列中
# ⒊最后在优先队列里的点为树的根节点（root）

import collections

word = 'this is an example of a huffman tree'
#将这个句子中的每个字母都放入到 heap中
freq = collections.Counter(word)

def encode_huff(freq):
    #wt为出现频率, sym为符号, ""内为计算的huffman_code

    heap = [[wt, [sym, ""]] for sym, wt in freq.items()]
    heapify(heap)
    while(len(heap)) > 1:
        ll = heappop(heap) # --> 这个应该是最左面的那个, 所以先将huffmancode加一个'0'
        lr = heappop(heap) # --> 这个应该是右边的那个, 所以先将huffmancode加一个'1'
        for pair in ll[1:]:
            pair[1] += '0'
        for pair in lr[1:]:
            pair[1] += '1'

        #然后将计算的结果在放回到heap中
        heappush(heap, [ll[0]+lr[0]] + ll[1:] + lr[1:])

    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

encode_huff(freq)















