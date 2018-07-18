

'''
修改计算逻辑为读取注册表是否开启了代理
由于Github for windows需要切换代理,
所以修改程序,添加了对文件的修改
'''

import socket
import win32api
import win32con
import re 

# 新增代码
def refresh():
    import ctypes

    internet_option_refresh = 37
    internet_option_settings_changed = 39

    internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

    internet_set_option(0, internet_option_refresh, 0, 0)
    internet_set_option(0, internet_option_settings_changed, 0, 0)


d = {}
d['ProxyServer'] = '10.161.72.126:808'
d['ProxyOverride'] = '*.local;127.0.0.1;account.jetbrains.com;resharper-plugins.jetbrains.com'
d['ProxyEnable'] = 1

if __name__ == '__main__':
    pathInReg = 'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, pathInReg, 0, win32con.KEY_ALL_ACCESS)
    
    flag_http_in_file = '0'
    p = re.compile('\[https*\]')
    
    # 获取当前代理是否开启
    # isProxyEnable[1] 为开启
    # isProxyEnable[0] 为关闭
    isProxyEnable = win32api.RegQueryValueEx(key, 'ProxyEnable')

    if isProxyEnable[0] == 0:
        d['ProxyServer'] = '10.161.72.126:808'
        d['ProxyOverride'] = '*.local;127.0.0.1;account.jetbrains.com;resharper-plugins.jetbrains.com'
        d['ProxyEnable'] = 1
        
        # 修改 C:\Users\kongp\.gitconfig 
        # 删除Github代理
        with open(r'C:\Users\kongp\.gitconfig', 'r') as f:
            tp = f.readlines()
        
        for line_num, i in enumerate(tp):
            if re.match(p, i):
                flag_http_in_file = '1'
        
        if flag_http_in_file == '1':
            pass
        else:
            with open(r'C:\Users\kongp\.gitconfig', 'a') as f:
                f.write('\n[http]\n')
                f.write('    proxy = 10.161.72.126:808\n')
                f.write('[https]\n')
                f.write('    proxy = 10.161.72.126:808\n')


        proxy_info = '代理已经打开'

    else:
        d['ProxyEnable'] = 0
        proxy_info = '代理已经关闭'

        del_line_nums = []
        res_tp = []
        # 修改 C:\Users\kongp\.gitconfig 
        # 删除Github代理
        with open(r'C:\Users\kongp\.gitconfig', 'r') as f:
            tp = f.readlines()
        
        for line_num, i in enumerate(tp):
            if re.match(p, i):
                del_line_nums.append(line_num)
                del_line_nums.append(line_num+1)

        for line_num, line in enumerate(tp):
            if line_num in del_line_nums:
                pass
            else:
                res_tp.append(line)
        
        with open(r'C:\Users\kongp\.gitconfig', 'w') as f:
            for i in res_tp:
                f.write(i)

    for k, v in d.items():
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, pathInReg, 0, win32con.KEY_ALL_ACCESS)
        # print(key,k,0,v)
        win32api.RegSetValueEx(key, k, 0, win32con.REG_DWORD if k == 'ProxyEnable' else  win32con.REG_SZ, v)
        win32api.RegCloseKey(key)

    refresh()
    
    print('\a')
    # 弹出一个提示框,表示代理已经修改
    win32api.MessageBox(0,proxy_info,'提示',win32con.MB_OK)

'''

    # 监视代理
# 确保这些 *.local;127.0.0.1;account.jetbrains.com;resharper-plugins.jetbrains.com
# 网址处于无法联网状态
# 如果代理处于打开状态,则设置例外
# 监控间隔 先设置1秒吧
# 如果在设置中,删除了"对于下列字符开头....."中的内容
# 则 ProxyOverride 就不会存在,导致程序错误

import os
import sys
import time
import win32api
import win32con

oldProxyInfo = ''
newProxyInfo = ''

# 获取进程信息

def GetInfo():
    d = {}
    d['ProxyOverride'] = '*.local;127.0.0.1;account.jetbrains.com;resharper-plugins.jetbrains.com'
    d['pathInReg'] = 'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
    d['key'] = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, d['pathInReg'], 0, win32con.KEY_ALL_ACCESS)
    return d

def Monitor(d):
    try:
        while (True):
            time.sleep(1)
            tempInfo = win32api.RegEnumKeyExW(d['key'])
            isProxyEnable = win32api.RegQueryValueEx(d['key'], 'ProxyEnable')
            proxyOverrideInfo = win32api.RegQueryValueEx(d['key'], 'ProxyOverride')[0]
            isSettProxyOverride = (proxyOverrideInfo == d['ProxyOverride'])
            if (isProxyEnable[0] == 1 and not isSettProxyOverride):
                print('yes')
                win32api.RegSetValueEx(d['key'], 'ProxyOverride', 0, win32con.REG_SZ, d['ProxyOverride'])
                refresh()
            else:
                print('no')
                continue
    finally:
        win32api.RegCloseKey(d['key'])

def refresh():
    import ctypes

    internet_option_refresh = 37
    internet_option_settings_changed = 39

    internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

    internet_set_option(0, internet_option_refresh, 0, 0)
    internet_set_option(0, internet_option_settings_changed, 0, 0)



if __name__ == '__main__':
    d = GetInfo()
    Monitor(d)
    
'''






   



