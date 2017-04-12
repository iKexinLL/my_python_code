#encoding=utf-8
"""
Created on 2016/3/24 16:52
author: iKexinLL
练习一下 heapq, 弄一弄堆
对于一个堆(完全二叉树)来说,如果父节点的编号为k, 那么它的左儿子编号为k * 2 + 1, 右儿子的编号为k * 2 + 2
反之, 如果已知一个子节点的编号为k, 那么其父节点的编号为 (k - 1) // 2

        0
   1         2
3    4    5    6
"""

import heapq


data = [1, 2, 12, 19, 36, 5, 99, 22, 3, 17, 28, 46, 25, 92]

'''
堆的左儿子一定比右儿子小
'''


def heapify(x):
    """Transform list into a heap, in-place, in O(len(x)) time."""
    n = len(x)
    # Transform bottom-up.  The largest index there's any point to looking at
    # is the largest with a child index in-range, so must have 2*i + 1 < n,
    # or i < (n-1)/2.  If n is even = 2*j, this is (2*j-1)/2 = j-1/2 so
    # j-1 is the largest, which is n//2 - 1.  If n is odd = 2*j+1, this is
    # (2*j+1-1)/2 = j so j-1 is the largest, and that's again n//2-1.
    for i in reversed(range(n//2)):
        siftup(x,i)


def siftup(x,i):
    '''
    :param i: 传入一个向上调整的编号
    :return:
    '''

    length_x = len(x) #也是最大编码号
    new_item = x[i] #当前x中,编码为i的值
    childpos = 2*i + 1 #最大的儿子节点

    pass



n = len(data)

def siftdown(i):
    '''
    :param i: 传入一个向下调整的编号,注意是编号
    :return:
    '''
    #flag 标记是否需要继续向下调整
    #t为等待交换的编号
    t = flag = 0

    #当i节点有儿子(一般来说, 肯定要首先左儿子),并且需要继续调整的时候,循环就执行.
    #需要调整的条件:当i节点大于其子节点的时候

    while(i * 2 < n and flag == 0):

        #先与左儿子比较,如果大于左儿子,则将左儿子的编号赋给t, 否则将自身的编号给t
        if data[i] > data[i * 2]:
            t = i * 2
        else:
            t = i

        #先判断是否存在右儿子
        #在比较右儿子的值和左儿子的值,如果右儿子的值较大,则将右儿子的编号赋给t
        if 2 * i + 1 <= n:
            if data[t] > data[t + 1]:
                t = i * 2 + 1

        #如果t != i, 则表示最小的节点编号不是自己, 那么就交换,
        #且将新的位置t赋给i
        if t != i:
            data[i], data[i] = data[t], data[i]
            i = t
        #当 t == i时,表示最小的节点编号已经是自己了
        else:
            flag = 1






heapify(data)



