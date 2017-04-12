'''
删除
https://onedrive.live.com/view.aspx/Documents/%e5%8f%af%e5%bf%83^4s%20Notebook?cid=fc5ec797c2f13fdf&id=documents&wd=target%28%E5%BE%AE%E4%BF%A1%E4%BF%9D%E5%AD%98.one%7CCB6F6694-2DDA-4A72-AD6E-7A59DE852096%2F%E7%9F%A5%E4%B9%8E%E4%B8%8A%E7%9A%8448%E6%9D%A1%E7%A5%9E%E5%9B%9E%E5%A4%8D%EF%BC%8C%E9%92%88%E9%92%88%E8%A7%81%E8%A1%80%EF%BC%8C%E7%9C%8B%E5%AE%8C%E6%95%B4%E4%B8%AA%E4%BA%BA%E9%80%9A%E9%80%8F%E5%A4%9A%E4%BA%86%7CF983C580-203E-40E7-913F-6F0C654D8585%2F%29
有些从微信传过来的文章有些乱
'''

from bs4 import BeautifulSoup as bsp

path_xml = r'E:\code\python\未完成\Untitled-1.xml'

# 读取xml文件
with open(path_xml, encoding ='utf-8') as f:
    content_xml = f.read()
soup = bsp(content_xml, 'lxml-xml')

child_oe = soup.find_all('OE') 

'''
查找内容
找到一个new_line,
如果 new_line.pos-1且new_line.pos-2为内容 或者 new_line.pos+1且new_line.pos+2为内容
    则continue
    否则pos放入删除列表
'''


pos_contents = []
pos_new_line = []
# pos_others = [] # 图像看做内容处理

for pos in range(len(child_oe)):
    temp_cont = child_oe[pos].T
    if temp_cont:
        if temp_cont.text != '\n': #内容
            pos_contents.append(pos)
        else:
            pos_new_line.append(pos)
    else:
        pos_contents.append(pos)

del_postition = []
del_num = 0 #已经删除的数字
'''
仔细研究了一下
pos_new_line[:20]
Out[12]: [4, 6, 8, 11, 14, 17, 20, 23, 26, 28, 30, 32, 34, 35, 37, 39, 40, 42, 44, 45]

pos_contents[:20]
Out[7]: [0, 1, 2, 3, 5, 7, 9, 10, 12, 13, 15, 16, 18, 19, 21, 22, 24, 25, 27, 29]

只要判断 new_line的位置就可以了,情况如下:
如果 new_line.pos-1且new_line.pos-2为内容 或者 new_line.pos+1且new_line.pos+2为内容
    则continue
    否则pos放入删除列表
desc: 比如 new_line位置 4,前两位2,3均在pos_contents中,那么这个4就不用删除
desc: 然后 new_line位置 6,前两位4,5中的4不在pos_content中,那么这个6需要删除,
      但是在删除后,原pos_contents中的7就变为了6,那么, new_line中的8变为了7,
      那么这个7是不用删除的.
concl: 那么这种情况,每次删除后,两个pos列表中的数字均需要减1.
       如果不考虑性能,使用in来判断,并循环两次来处理pos的减少.
       --- 2017年4月12日00:59:30 先考虑到这,睡觉
       ---- 或者干脆我把new_line全删了,这样所有的内容都能保持同一格式

'''

