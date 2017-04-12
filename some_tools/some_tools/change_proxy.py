# encoding=utf-8
"""
Created on 2016/9/12 19:43
author: iKexinLL
尝试根据IP判断目前是在家里还是在公司,然后进行代理切换
来自:http://www.au92.com/archives/shi-yong-P-y-t-h-o-n-gei-I-E-she-zhi-dai-li.html
备用:http://mt.sohu.com/20160117/n434810017.shtml
这么写仍然需要重新打开浏览器,或者打开"代理设置",仍不够自动化,所以要修改一下(按照备用里面说明:
"如果不手动打开IE设置里的局域网设置窗口的话，所有代理设置是不生效的。这是为什么呢？"
After the script runs the browsers will still have the old proxy stored in-memory, so you need to restart them so they can re-read the new proxy settings from the registry
"""

import socket
import win32api
import win32con

myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname_ex(
    myname)  # 公司返回 ('IKexinLL', [], ['169.254.162.68', '192.168.81.111', '10.161.252.160'])
pathInReg = 'Software\Microsoft\Windows\CurrentVersion\Internet Settings'


def change_proxy(addr):
    d = {}

    if '10.161.252.173' in myaddr[2] or '10.161.252.132' in myaddr[2] or '127.0.0.1' in myaddr[2]:  # 公司ip
        d['ProxyServer'] = '10.161.32.26:8080'
        d['ProxyOverride'] = '*.local;10.161.*.*;10.163.*.*;192.168.8.*;127.0.0.1;<local>'
        d['ProxyEnable'] = 1
    else:
        d['ProxyEnable'] = 0

    return d


# 新增代码
def refresh():
    import ctypes

    internet_option_refresh = 37
    internet_option_settings_changed = 39

    internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

    internet_set_option(0, internet_option_refresh, 0, 0)
    internet_set_option(0, internet_option_settings_changed, 0, 0)


if __name__ == '__main__':
    d = change_proxy(myaddr)
    for k, v in d.items():
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, pathInReg, 0, win32con.KEY_ALL_ACCESS)
        # print(key,k,0,v)
        win32api.RegSetValueEx(key, k, 0, win32con.REG_DWORD if k == 'ProxyEnable' else  win32con.REG_SZ, v)
        win32api.RegCloseKey(key)

    refresh()
    
    print('\a')
    #弹出一个提示框,表示代理已经修改
    win32api.MessageBox(0,'代理已经修改','提示',win32con.MB_OK)
    

'''

i = 0
d3 = {}
while True:
    name = win32api.RegEnumValue(key,i) #获取此项里面的每项名称和值
    d3[name[0]] = name[1:]
    i += 1

# win32api.RegEnumKeyExW(key) # 获取当前项中的分项名称
'''