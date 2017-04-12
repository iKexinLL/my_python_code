#encoding=utf-8
"""
Created on 2016/4/12 16:28
author: iKexinLL
"""


class Heap(object) :
    def __init__(self,a) :
        self.a = a
        self.heapsize = len(a)


    def parent(self,i) :
        return (i - 1) // 2


    def left(self,i) :
        return 2 * i + 1


    def right(self,i) :
        return 2 * i + 2


    def max_heapify(self,i, heap_size):
        l = self.left(i)
        r = self.right(i)

        if heap_size:
            heap_size = len(self.a)
        else:
            heap_size = heap_size

        if l <= heap_size  - 1 and self.a[l] > self.a[i] :
            largest = l
        else :
            largest = i

        if r <= heap_size and self.a[r] > self.a[largest] :
            largest = r
        if not largest == i :
            self.a[i],self.a[largest] = self.a[largest],self.a[i]
            self.max_heapify(largest, heap_size)


    def build_max_heap(self) :
        heapsize = len(self.a)
        for i in reversed(range(len(self.a) // 2)) :
            self.max_heapify(i,heapsize)


    def heapsort(self) :
        self.build_max_heap()
        heap_size = len(self.a)
        for i in reversed(range(1,len(self.a))) :
            self.a[0],self.a[i] = self.a[i],self.a[0]
            self.max_heapify(0,heap_size)
            heap_size = heap_size - 1