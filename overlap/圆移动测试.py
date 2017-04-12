#encoding=utf-8

'''
Created on 2015年12月9日

@author: xukexin01
'''
'''
设定两个圆重叠,使圆各自平移应该移动的距离的一半
只移动两个重叠的圆
'''
import numpy as np
import matplotlib.pyplot as plt

def calculate_cc_distance(posA,posB): #计算两个圆心间的距离
    xa,ya = posA
    xb,yb = posB
    return np.hypot((xa-xb),(ya-yb))

def final_point(circle,c_A,c_B,pos_A,pos_B,r_A,r_B,d=2): #计算移动后的圆心
    #print('final_point')
    df = r_A + r_B + d
    dab = calculate_cc_distance(pos_A,pos_B)
    ntm = (df - dab)/2   #先两个圆各移动一半 need_to_move
    pxa,pya = pos_A
    pxb,pyb = pos_B
    
    if pxa > pxb:
        dn = (ntm/df * (pxa - pxb))
        fpxa = pxa + dn
        fpxb = pxb - dn 
    else:
        dn = (ntm/df * (pxb - pxa))
        fpxa = pxa - dn
        fpxb = pxb + dn
    
    if pya > pyb:
        dn = (ntm/df) * (pya - pyb)
        fpya = pya + dn
        fpyb = pyb - dn
    else:
        dn = (ntm/df) * (pyb - pya)
        fpya = pya - dn
        fpyb = pyb + dn
    
    circle[c_A].update({'pos':(fpxa,fpya)})
    circle[c_B].update({'pos':(fpxb,fpyb)})
    
    
def final_point_out(circle,c_A,c_B,pos_A,pos_B,r_A,r_B,d=2): #计算移动后的圆心
    #print('final_point')
    df = r_A + r_B + d
    dab = calculate_cc_distance(pos_A,pos_B)
    ntm = (df - dab)   #外圆移动need_to_move的距离
    pxa,pya = pos_A
    pxb,pyb = pos_B
    fpxa = fpxb = fpya = fpyb = 0
    if pxa > pxb:
        dn = (ntm/df * (pxa - pxb))
        fpxa = pxa + dn
    else:
        dn = (ntm/df * (pxb - pxa))
        fpxb = pxb + dn
    
    if pya > pyb:
        dn = (ntm/df) * (pya - pyb)
        fpya = pya + dn
    else:
        dn = (ntm/df) * (pyb - pya)
        fpyb = pyb + dn
    
    circle[c_A].update({'pos':(fpxa,fpya)})
    circle[c_B].update({'pos':(fpxb,fpyb)})        

def judge_overlap(pos_A,pos_B,r_A,r_B):
    return calculate_cc_distance(pos_A,pos_B) < r_A + r_B
    
    




fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(111)
ax.set_xlim((-20,20))
ax.set_ylim((-20,20))

#===============================================================================
# circleA = {'r':5,'pos':(6,7)}
# circleB = {'r':6,'pos':(5,9)}
#===============================================================================
import json
#with open(r'E:\xkx\networkx_json\联想.json') as f: #打开json文件
    #d1 = json.loads(f.read())                 #将内容放入到d1中

#读取json中的文件内容
#attributeList = d1['attributeList']
#relationList = d1['relationList']
#entityList = d1['entityList']


circle = {'a':{'r':5,'pos':(6,7)},
          'b':{'r':6,'pos':(5,9)},
          'c':{'r':4,'pos':(4,4)},
          'd':{'r':2,'pos':(3,-2)}} 

for k,v in circle.items():
    circ = plt.Circle(v['pos'],v['r'],color='y',alpha=0.4)
    ax.add_patch(circ)
    plt.plot(v['pos'][0],v['pos'][1],'bo')

df = {}
for i in range(5):
    for k,v in circle.items():
        for m, n in circle.items():
            if m == k:
                pass
            elif judge_overlap(v['pos'],n['pos'],v['r'],n['r']):
                final_point(circle,k,m,v['pos'],n['pos'],v['r'],n['r'],d=5)
    print(circle)
    print('------------')
            
for k,v in circle.items():
    circ = plt.Circle(v['pos'],v['r'],color='k',alpha=0.4)
    ax.add_patch(circ)
    plt.plot(v['pos'][0],v['pos'][1],'ro')

plt.show()
    







#===============================================================================
# 
# 
# #设定希望的间距 m = 2
# m = 2
# df = circleA['r'] + circleB['r'] + m
# res = final_ponit(circleA['pos'],circleB['pos'],df)
# 
# circleA.update({'pos':res[0]})
# circleB.update({'pos':res[1]})
# 
# 
# circ = plt.Circle(circleA['pos'],circleA['r'],color='k',alpha=0.5)
# ax.add_patch(circ)
# circ = plt.Circle(circleB['pos'],circleB['r'],color='k',alpha=0.5)
# ax.add_patch(circ)
# plt.plot(circleA['pos'][0],circleA['pos'][1],'ro')
# plt.plot(circleB['pos'][0],circleB['pos'][1],'ro')
# #plt.subplots_adjust(bottom=0.01,left=0.01,right=0.99,top=0.99)
# plt.show()
# 
# 
# #===============================================================================
# # def final_ponit(posA,posB,df):
# #     
# #     #计算点a点b到原点的距离
# #     pa = calculate_distance((0,0),posA)
# #     pb = calculate_distance((0,0),posB)
# #     
# #     #如果点a的横坐标大于b点的横坐标,则a向左移,b向右移
# #     if posA[0] > posB[0]:
# #         fpax = (pa - df) * posA[0] / pa
# #         fpbx = (pa + df) * posA[0] / pa
# #     elif posA[0] < posB[0]:
# #         fpax = (pa + df) * posA[0] / pa
# #         fpbx = (pa - need_to_move) * posA[0] / pa
# #     else:
# #         pass
# #         #如果点a的横坐标大于b点的横坐标,则a向左移,b向右移
# #     if posA[1] > posB[1]:
# #         fpay = (pa + need_to_move) * posA[1] / pa
# #         fpby = (pa - need_to_move) * posA[1] / pa
# #     elif posA[1] < posB[1]:
# #         fpay = (pa - need_to_move) * posA[1] / pa
# #         fpby = (pa + need_to_move) * posA[1] / pa
# #     else:
# #         pass
# #     print((fpax,fpay),(fpbx,fpby))
# #     return ((fpax,fpay),(fpbx,fpby))
# #===============================================================================
# 
# def final_ponit1(posA,posB,df):
#     dab = calculate_distance(circleA['pos'],circleB['pos'])
#     need_to_move = (df - dab)/2
#     #计算点a点b到原点的距离
#     da = calculate_distance((0,0),posA)
#     db = calculate_distance((0,0),posB)
#     #如果点a的横坐标大于b点的横坐标,则a向左移,b向右移
#     if posA[0] > posB[0]:
#         fpax = ((da + need_to_move) * circleA['pos'][0]) / da
#         fpbx = ((db - need_to_move) * circleB['pos'][0]) / db
#     elif posA[0] < posB[0]:
#         fpax = ((da - need_to_move) * circleA['pos'][0]) / da
#         fpbx = ((db + need_to_move) * circleB['pos'][0]) / db
#     else:
#         pass
#         #如果点a的横坐标大于b点的横坐标,则a向左移,b向右移
#     if posA[1] > posB[1]:
#         fpay = ((da + need_to_move) * circleA['pos'][1]) / da
#         fpby = ((db - need_to_move) * circleB['pos'][1]) / db
#     elif posA[1] < posB[1]:
#         fpay = ((da - need_to_move) * circleA['pos'][1]) / da
#         fpby = ((db + need_to_move) * circleB['pos'][1]) / db
#     else:
#         pass
#     print(str((fpax,fpay))+','+str((fpbx,fpby)))
#     return ((fpax,fpay),(fpbx,fpby))
#===============================================================================

