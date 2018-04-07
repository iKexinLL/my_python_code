
import cv2
import os 
import numpy as np

path = r'I:\my_python_code\opencv_proj\OpenCV_Test\OpenCV_Test\Image'
image_name = 'python.png'

# 修改Image目录为默认目录
os.chdir(path)

# 设置image路径
image_path = os.path.join(path,image_name)

# WINDOW_NORMAL 	the user can resize the window (no constraint) / also use to switch a fullscreen window to a normal size.
# WINDOW_AUTOSIZE 	the user cannot resize the window, the size is constrainted by the image displayed.
# WINDOW_OPENGL 	window with opengl support.
# WINDOW_FULLSCREEN 	change the window to fullscreen.
# WINDOW_FREERATIO 	the image expends as much as it can (no ratio constraint).
# WINDOW_KEEPRATIO 	the ratio of the image is respected.
# WINDOW_OPENGL 无法使用: Library was built without OpenGL support in function cvNamedWindow

# WINDOW_GUI_EXPANDED 全部显示,但有些拉伸
# WINDOW_GUI_NORMAL 全部显示,但有些拉伸
cv2.namedWindow('Test',cv2.WINDOW_GUI_EXPANDED)

# 读取image
img = cv2.imread(image_path)
# cv2.imshow('Test', img)  

height, width = img.shape[:2]
fwidth = 1
fheight = 1
size = (int(width * fwidth), int(height * fheight))  

shrink = cv2.resize(img,size)
cv2.imshow('Test', shrink)  
cv2.waitKey(0)  


