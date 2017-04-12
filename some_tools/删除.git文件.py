

'''
用shutil的时候,会有 PermissionError, 导致错误,
所以直接使用 cmd中的 rd /s /q 路径 命令
'''

import os 

path  = r'E:\code\python'

for root, dirs, files in os.walk(path):
    if root.endswith('.git'):
        os.system('rd /s /q ' + os.path.abspath(root)) # /s可以删除非空文件夹, /q 不用确认
