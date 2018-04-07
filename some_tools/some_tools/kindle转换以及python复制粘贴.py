import win32clipboard as w
import win32con
# 在Unicode 字符集下， 用CF_UNICODETEXT标记
# http://blog.csdn.net/ycc892009/article/details/6521565
# 而不是使用 win32con.CF_TEXT,否则会产生乱码
d = {}


d[' '] = ''
d['， '] = ','
d['。'] = '.'
d['，'] = ','
d['“'] = '"'
d['”'] = '"'

def trans(a):
    s = ''
    for i in range(len(a)):
        if a[i] != '\n':
            s += d.get(a[i],a[i])
        else:
            break
    w = settext(s)
    t = gettext(w)
    print(t)
    # print(t.decode(encoding='utf-8'))
    # return t

def gettext(w):
    w.OpenClipboard()
    t = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return t


def settext(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()

    return w
