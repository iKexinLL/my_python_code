

'''
利用win32api进行分辨率调整
    -->因为破华为云桌面不支持surface的 2736*1824
利用easygui进行一个小判断
'''

import easygui as eg
import win32api 
import sys

# 正常情况下的分辨率
normalPelsWidth = 2736
normalPelsHeight = 1824
normalMetricsWidth = 1368
normalMetricsHeight = 912

# 适配云桌面的分辨率
yunPelsWidth = 1680
yunPelsHeight = 1050
yunMetricsWidth = 1344
yunMetricsHeight = 840

# 根据当前分辨率来确认提示框的参数
# 获取当前的分辨率

nowWidth = win32api.GetSystemMetrics(0)
nowHeight = win32api.GetSystemMetrics(1)


# if (nowWidth, nowHeight) == (normalPelsWidth, normalPelsHeight)
#     (nowWidth, nowHeight) = (yunPelsWidth, yunPelsHeight)


resWidth, resHeight = (normalPelsWidth, normalPelsHeight) \
                        if (nowWidth, nowHeight) == (yunMetricsWidth, yunMetricsHeight) \
                        else (yunPelsWidth, yunPelsHeight)

moduleName = "正常" if (nowWidth, nowHeight) == (yunMetricsWidth, yunMetricsHeight) \
                else "云桌面"

msg = "是否将分辨率修改为适配%(moduleName)s模式, %(resWidth)s*%(resHeight)s ?" \
        %({'moduleName':moduleName, 'resWidth':resWidth, 'resHeight':resHeight})

title = "修改分辨率"
choices = ['ok', 'cancel']


'''
MSDN上的解释为:
DMDFO_DEFAULT: #define DMDFO_DEFAULT   0
The display's default setting.	#define DMDFO_DEFAULT
####
DMDFO_CENTER: #define DMDFO_CENTER    2
The low-resolution image is centered in the larger screen space.
####
DMDFO_STRETCH: #define DMDFO_STRETCH   1
The low-resolution image is stretched to fill the larger screen space.　	
'''

if __name__ == '__main__':
    res = eg.buttonbox(msg, title='修改分辨率', choices=choices)
    if res == 'ok':
        dm = win32api.EnumDisplaySettings(None, 0)
        dm.PelsWidth = resWidth
        dm.PelsHeight = resHeight

        # dm.BitsPerPel = 32 # 不太清楚错用
        # dm.DisplayFixedOutput = 0 # 拉伸,填充
        win32api.ChangeDisplaySettings(dm, 0)
    else:
        sys.exit(0)

