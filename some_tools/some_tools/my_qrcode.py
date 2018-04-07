
import sys
import os 
import qrcode
import win32api
import win32con
import tempfile
import easygui as eg

from PIL import Image

qr = qrcode.QRCode(
    version=1,  #生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）
    error_correction=qrcode.constants.ERROR_CORRECT_M, #L:7% M:15% Q:25% H:30%
    box_size=10, #每个格子的像素大小
    border=2, #边框的格子宽度大小
)

temp_path = os.environ['TEMP'] + '\\temp.png'

data = eg.enterbox(msg="请填写内容",title="简单展现二维码")

if (data):
    qr.add_data(data)
    img = qr.make_image()
    # img.get_image()

    img.save(temp_path)

    img2 = Image.open(temp_path)
    img2.show()
# win32api.MessageBox(0,'请输入一些东西用来展现...','提示',win32con.MB_OK)


