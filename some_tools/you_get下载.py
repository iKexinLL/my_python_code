import easygui as eg
import os
import sys

fileInfo = ''
isContinue = True
isFileInfoLenE2 = True
isFileExists = True

def inputInfo():
    fileInfo = eg.multenterbox(msg = "", title="you_get下载", fields=["网址","保存地址"])
    return fileInfo

def ShowMsg(msg):
    eg.msgbox(msg)

testUrl = 'https://www.bilibili.com/video/av10725086/'
while(True):
    fileInfo = inputInfo()

    isFileInfoNotNone = fileInfo is not None
    if (not isFileInfoNotNone):
        break

    isFileInfoLenE2 = len(fileInfo) == 2
    if (not isFileInfoLenE2):
        eg.msgbox("网址或者位置为空,请重新输入")
        continue

    isFileExists = os.path.exists(fileInfo[1])
    if (not isFileExists):
        eg.msgbox("位置不存在,请重新输入")
    else:
        fileUrl = fileInfo[0]
        filePosition = '-o ' + fileInfo[1]
        # os.system('you-get %s %s' % (filePosition, fileUrl))
        print('you-get %s %s' % (filePosition, fileUrl))
    

while(isContinue or len(fileInfo) != 2):
    fileInfo = inputInfo()

    fileUrl = fileInfo[0]
    filePosition = '-o ' + fileInfo[1]

    print(fileInfo[1])
    print(fileInfo[1] == '')

    if (fileInfo[1] == ''):
        eg.msgbox("请输入保存地址")
        inputInfo()
    elif (not os.path.exists(fileInfo[1])):
         eg.msgbox("无此路径")
         inputInfo()
    elif (os.path.exists(fileInfo[1])):
        os.system('you-get %s %s' % (filePosition, fileUrl))
        isContinue = False
    else:
        pass
        








