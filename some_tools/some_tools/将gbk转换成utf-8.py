
'''
因为有很多文档都是gbk的,使用上有些不方便,所以直接转换成utf-8的
'''

path = r'E:\my_work\工作\多维订报\SR_asian\db'

import os

for root, dirs, files in os.walk(path):
    for file in files:
        try:
            with open(os.path.join(root, file), encoding = 'gbk') as fr:
               contents = fr.read()
            with open(os.path.join(root, file), 'w', encoding = 'utf-8') as fw:
                fw.write(contents)
        except Exception as e:
          print(file, e)
          
        
        