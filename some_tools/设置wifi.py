#encoding=utf-8
"""
Created on 2016/3/24 17:04
author: iKexinLL
"""

import os

#开启
net_start = 'netsh wlan set hostednetwork mode=allow ssid={0} key={1}'
name = 'testwifi_h'
password = 'kong123456'
print(net_start.format(name, password))
os.system(net_start.format(name, password))
os.system('netsh wlan start hostednetwork')




#关闭
os.system('netsh wlan stop hostednetwork')
print('wlan off')