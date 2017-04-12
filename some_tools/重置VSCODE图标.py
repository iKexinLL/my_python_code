
import shutil
import os

path_source = r'D:\Program Files (x86)\Microsoft VS Code\code_file.ico'

path_target = r'D:\Program Files (x86)\Microsoft VS Code\resources\app\resources\win32\code_file.ico'

# 删除 target文件
if os.path.exists(path_target):
    os.remove(path_target)

shutil.copy(path_source, path_target)


# 重启"资源管理器"

os.system(r'taskkill /f /im explorer.exe')

os.system(r'explorer.exe')

