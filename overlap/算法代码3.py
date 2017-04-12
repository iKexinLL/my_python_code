#encoding=utf-8
'''
Created on 2015年12月10日
先放一下,效率太低了,对于几百万的企业,我都不知道能不能算出来

@author: xukexin01
不能只用左下角,所以必须用随机出一个角
可以用二维数组计算.
 [(m,n) for m in range(lb[0]+1,rb[0]) for n in range(lb[1]+1,lt[1])]
 可以对c_set的长度做一个限制
 需要给点加一个计数器,因为点对多连四个正方形,所以一旦其计数器为4的话,它则可以被pop
 感觉给中间开始比较好
'''


import os
import json
import pandas as pd 
import networkx as nx
import copy
import numpy as np
import matplotlib.pyplot as plt
import random
from string import ascii_uppercase
import codecs as cs
 
attributeList = []
relationList = []
entityList = []
ent_sum_power_radius = 0
type_A = {}
type_B = {}
type_C = {}
type_D = {}
type_E = {}
  
for dirpath,dirnames,filename in os.walk(r'e:\xkx\json'):
    for i in filename:
        path = dirpath+ '\\' + i
        print(path)
        f = cs.open(path)
        try:
            d_json = json.loads(f.read())                #将内容放入到d_json中
        except Exception as e:
            print(e)
            f.close()
            f = cs.open(path,encoding='utf-8')
            d_json = json.loads(f.read()) 
        f.close()
  
        #读取json中的文件内容
        attributeList.extend(d_json['attributeList'])
        relationList.extend(d_json['relationList'])
        entityList.extend(d_json['entityList']) 
          
G = nx.Graph()  
peo = []      
ent = []
#仅对于随机产生的企业类型和大小,否则无法去重
#因为entityList中存储的是dict,无法iter,所以只能用这个方法({}.fromkeys(a).keys())
#这个有点慢~~
ao = []
#ao = [m for m in entityList if m not in m]
for m in entityList:
    if m not in ao:
        ao.append(m)
entityList = ao[:]
ao = []
for m in relationList:
    if m not in ao:
        ao.append(m)
relationList = ao[:]
ao = []
for m in attributeList:
    if m not in ao:
        ao.append(m)
attributeList = ao[:]
  
#添加大小以及企业或者人的类型
for m in entityList:
    #m.update({'classId':str(int(m['classId']))})
    #m.update({'id':str(int(m['id']))})
    m.update({'size':random.randint(1,100)})
    m.update({'category':random.choice(ascii_uppercase[:5])})
    G.add_node(m['id'],{'classId':m['classId'],'name':m['name'],'size':m['size'],'category':m['category']})
    if m['classId'] == 1.0:
        ent.append(m['id'])
        ent_sum_power_radius = ent_sum_power_radius + m['size'] ** 2
        if m['category'] == 'A':
            type_A.update({m['id']:{'size':m['size']}})
        elif m['category'] == 'B':
            type_B.update({m['id']:{'size':m['size']}})
        elif m['category'] == 'C':
            type_C.update({m['id']:{'size':m['size']}})
        elif m['category'] == 'D':
            type_D.update({m['id']:{'size':m['size']}})
        elif m['category'] == 'E':
            type_E.update({m['id']:{'size':m['size']}})
    if m['classId'] == 2.0:
        peo.append(m['id'])         


ent = {'2': {'size': 3}}
np_shape = []
#100038472585.0: {'size': 50}
def init_rectangle(ent_id,size,px,py,quadrant): #根据角落选择正方形位置,根据圆的半径推算出正方形以及圆心,均按照顺时针移动
    '''
    for k,v in ent.items():
        rec = init_rectangle(k,v['size'],0,0,2,1
    '''
    m = 20
    height =  int(2 * (size + m))
    lb_corner = ()
    lt_corner = ()
    rt_corner = ()
    rb_corner = ()
    if quadrant == 1:
        lb_corner = (px,py)
        lt_corner = (px,py+height)
        rt_corner = (px+height,py+height)
        rb_corner = (px+height,py)
    elif quadrant == 2:
        lb_corner = (px-height ,py)
        lt_corner = (px-height,py+height)
        rt_corner = (px,py+height)
        rb_corner = (px,py)
    elif quadrant == 3:
        lb_corner = (px-height,py-height)
        lt_corner = (px-height,py)
        rt_corner = (px,py)
        rb_corner = (px,py-height)
    elif quadrant == 4:
        lb_corner = (px,py-height)
        lt_corner = (px,py)
        rt_corner = (px+height,py)
        rb_corner = (px+height,py-height)
    else:
        raise TypeError('not a quadrant')
    center = (lb_corner[0] + (rb_corner[0] - lb_corner[0]) / 2, rb_corner[1] + (rt_corner[1] - rb_corner[1]) / 2)
    return {'id':ent_id,'height':height,'r':size,
            'lb_corner':lb_corner, 'lt_corner':lt_corner, 'rt_corner':rt_corner, 
            'rb_corner':rb_corner,'center':center}   

def confirm_nonuse_point(rec,can_set_point,cannot_set_point, np_shape = np_shape):
    #将数组改成坐标系,这个只将正方形内部的点变成1
    #layout_height = len(np_shape)
    ''' #数组和坐标系第一象限的关系 (a,b)  --->  (-b,a)
    rect_translate_matrix
    '''
    lb = rect_translate_matrix(rec['lb_corner'])
    rb = rect_translate_matrix(rec['rb_corner'])
    lt = rect_translate_matrix(rec['lt_corner'])
    #np_shape[lt[0]+1:lb[0],lb[1]+1:rb[1]] = 1
    for m in range(lt[0]+1,lb[0]):
        for n in range(lb[1]+1,rb[1]):
            np_shape[m,n] = 1
            cannot_set_point.add(martix_translate_rect((m,n)))
    #can_set_point.update([(-lt[1]-1,x) for x in range(lb[0],rb[0]+1)]) #top
    #can_set_point.update([(-lb[1]-1,x) for x in range(lb[0],rb[0]+1)]) #bottom
    #can_set_point.update([(y,lb[0]) for y in range(-lt[1]-1,-lb[1])])  #lelt
    #can_set_point.update([(y,rb[0]) for y in range(-lt[1]-1,-lb[1])])  #lelt
    can_set_point.update([martix_translate_rect((lt[0],x)) for x in range(lb[1],rb[1]+1)]) #top             
    can_set_point.update([martix_translate_rect((lb[0],x)) for x in range(lb[1],rb[1]+1)])  #bottom
    can_set_point.update([martix_translate_rect((y,lb[1])) for y in range(lt[0],lb[0]+1)])  #lelt
    can_set_point.update([martix_translate_rect((y,rb[1])) for y in range(lt[0],lb[0]+1)])  #right
    #与不能选的点做差集
    can_set_point.difference_update(cannot_set_point)
    
    
def rect_translate_matrix(point):
    return (-point[1]-1,point[0])
    

def martix_translate_rect(point):
    return (point[1],-point[0]-1)

def cannot_set_point(canot_set_point,can_set_point,rectangle,np_shape):
    pass
    
    
    
    
#corner_set = [1,2,3,4]

can_set_point = set()
cannot_set_point = set() #用于判断顶点
#使用二维数组进行查找排序 
#lc = round(np.sqrt(4 * ent_sum_power_radius)) + 5   
lc = 4000
np_shape = np.zeros((lc,lc),np.int32)
#在中间获取一个圆
px = int(lc/2 - 2)
py = int(lc/2 - 2) 
#得到初始的矩阵
#计算初始正方形的点 ent_id,size,px,py,quadrant
irec = init_rectangle(1,2,px,py,1)
#初始化可选择的点confirm_nonuse_point
confirm_nonuse_point(irec,can_set_point,cannot_set_point,np_shape)
#到此,初始化完毕

#选择一个id测试 100000326827.0 50 
#choice_point = random.choice(list(can_set_point)) #获取一个可以放置正方形的节点
#corner = random.choice(corner_set)

def right_rectangle(end_id,size,can_set_point,choice_point,quadrand,np_shape = np_shape):
    layout_length = len(np_shape)
    rectangle = init_rectangle(end_id,size,choice_point[0],choice_point[1],quadrand)
    lb = rect_translate_matrix(rectangle['lb_corner'])
    rb = rect_translate_matrix(rectangle['rb_corner'])
    lt = rect_translate_matrix(rectangle['lt_corner'])
    if abs(lb[0]) > layout_length or abs(lt[0]) > layout_length or abs(rb[1]) > layout_length:
        return 1
    else:
        return sum(sum(np_shape[-lt[1]-1:-lb[1],lb[0]:rb[0]+1])) #在ipython 中不需sum(sum(

p = 0

#判断四个方向上是否能放下这个正方形
def judge_direction(ent_id,size,can_set_point,np_shape = np_shape,p=p):
    '''
            |
        li8 | li1
      |-----|-----|
   li7|   li|9    | li2
    --|li12-|-li10|--->
      |     |     |
   li6|    lit11  | li3
      |-----|-----|
        li5 | li4
array([[  0.,   1.,   2.,   3.,   4.],
       [  5.,   6.,   7.,   8.,   9.],
       [ 10.,  11.,  12.,  13.,  14.],
       [ 15.,  16.,  17.,  18.,  19.],
       [ 20.,  21.,  22.,  23.,  24.]])
       数组的方向跟坐标还不一样..... 
        mar[1:4,2]
        Out[292]: array([  7.,  12.,  17.])      
        mar[2,1:4]
        Out[293]: array([ 11.,  12.,  13.])
      那么让数组也从左下角开始就好了
    
    '''
    choice_point = random.choice(list(can_set_point))
    corner_set = [1,2,3,4]
    if right_rectangle(ent_id,size,can_set_point,choice_point,1,np_shape) != 0 :
        corner_set.remove(1)
    if right_rectangle(ent_id,size,can_set_point,choice_point,2,np_shape) != 0 :
        corner_set.remove(2)
    if right_rectangle(ent_id,size,can_set_point,choice_point,3,np_shape) != 0 :
        corner_set.remove(3)
    if right_rectangle(ent_id,size,can_set_point,choice_point,4,np_shape) != 0 :
        corner_set.remove(4)
    if len(corner_set) != 0 :
        dire = random.choice(corner_set)
        #return ent.update(init_rectangle(ent_id,size,choice_point,dire,np_shape))
        irec = init_rectangle(ent_id,size,choice_point[0],choice_point[1],dire)
        confirm_nonuse_point(irec,can_set_point,np_shape)
        return irec
    
    else:
        p = p + 1
        print(p)
        return judge_direction(ent_id,size,can_set_point,np_shape)
        
#ui = judge_direction(100000326827,choice_point,50,np_shape)
   
#
d = {}
for k,v in type_A.items():
    e = {k:judge_direction(k,v['size'],can_set_point,np_shape)}
    print(type(e))
    print(e)
    d.update(e)
fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(111)
ax.set_xlim((0,400))
ax.set_ylim((0,400))
for k,v in d.items():
    cir2c = plt.Rectangle(v['lb_corner'],v['height'],v['height'],color='k',alpha=0.5)
    ax.add_patch(cir2c)
    circ = plt.Circle(v['center'],v['r'],color='r',alpha=0.5)
    ax.add_patch(circ)

#plt.subplots_adjust(bottom=0.01,left=0.01,right=0.99,top=0.99)
plt.show()        
        
        
        
        
        
        
        

        
     
    #left bottom top right
        
#===============================================================================
# d = init_rectangle(0,0,50)
# can_set_point = set()
# can_set_point.add(d['lt'])
# can_set_point.add(d['rb'])
# can_set_point.add(d['rt'])
# 
# def point_rectangle(ent,n_point):
#     cx = n_point[0]
#     cy = n_point[1]
#     rec = init_rectangle(cx,cy,ent['size'])
# 
# for k,v in type_A.items():
#     n_point = random.choice(list(can_set_point))
#     rec = init_rectangle(k,n_point[0],n_point[1],v['size'])
#     #移除c_set中的点
#     
#     
#     
#         
# def circle_rec():
#     pass
# #现在得到三个类型的企业type_A,B,C
# #找到一个企业,初始化为初始正方形
# m = 2
# c_point = set()
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
#         
#         
#         
#         
#         
#         
#         
#         
#===============================================================================