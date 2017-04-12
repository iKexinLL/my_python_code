'''
获取metro下的注册表相关信息
'''

import win32api
import win32con

pathInReg = r'SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppContainer\Mappings' 
path_output = r'E:\code\python\some_tools\some_tools\metro.txt'

key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, pathInReg, 0, win32con.KEY_ALL_ACCESS)

t_metro = win32api.RegEnumKeyExW(key)

d = {}

for i in t_metro:
    temp_path = pathInReg + '\\' + i[0]
    temp_key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, temp_path, 0, win32con.KEY_ALL_ACCESS)
    temp_k = win32api.RegQueryValueEx(temp_key,'DisplayName')
    d[temp_k[0]] = i[0]
    win32api.RegCloseKey(temp_key)

win32api.RegCloseKey(key)

# 写出文件
with open(path_output, 'w', encoding = 'utf-8') as f:
    for k, v in d.items():
        f.write(k + '    ' + v + '\n')


'''
管理员运行:
CheckNetIsolation.exe loopbackexempt -a -p=S-1-15-2-2608634532-1453884237-1118350049-1925931850-670756941-1603938316-3764965493
'''