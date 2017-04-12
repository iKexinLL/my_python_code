'''
删除 onenote中内容的之间的空行
需要删除OE内容
利用decompose删除
'''

from bs4 import BeautifulSoup as bsp

path_xml = r'E:\code\python\未完成\Untitled-1.xml'

# 读取xml文件
with open(path_xml, encoding ='utf-8') as f:
    content_xml = f.read()
soup = bsp(content_xml, 'lxml-xml')


oe_children = soup.OEChildren

the_contents = []
the_new_line = []

for conts in oe_children.find_all('OE'):
    temp_cont = conts.T
    if temp_cont:
        if temp_cont.text != '\n':
            the_contents.append(conts)
        else:
            the_new_line.append(conts)


for i in the_new_line:
    i.decompose()

with open(r'e:\temp\res_one.xml', 'w', encoding = 'utf-8') as f:
    f.write(res)    






