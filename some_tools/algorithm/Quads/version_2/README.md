
2016年3月31日11:32:41
<p>修改程序注释 <br>
因为每个存在过的正方形都代表这个区域曾经有过点<br>
所以应该先判断这个区域是否存在过点
</p>

<pre>
<code>
 判断point是否属于rect中的一个sub_rect 
 如果属于
     判断这个sub_rect是否已经在G中
     如果存在
        则在递归调用sub_rect
     如果不存在
        判断rect中的这个sub_rect是否存在点b_point
        如果存在
           则在rect中删除rect_direction中的那个属性 
             删除rect和b_point的关系
             添加rect和sub_rect的关系 
             在sub_rect中重新计算point和b_point 
       如果不存在 
           则 在G中添加一个属性rect_direction(nw, ne, sw, se),
                表明这个方向上存在点b_point
              添加节点及其属性
              添加rect和point的关系
              向all_sub_rect中添加sub_rect(为了在form中画图)
</code>
</pre>

