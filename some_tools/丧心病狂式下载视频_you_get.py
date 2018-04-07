
import os
# 那么我就创建80个python文件来下载整部合集

'''
以数字对python文件进行命名
里面的内容可以直接使用python命令执行
'''

file_path = r'I:\temp_code'

url = 'https://www.bilibili.com/video/av7997007/?p=%s'
h = lambda x : str(x) if x > 9 else '0' + str(x)

start_point = 1
end_point = 81
old_name = 'UWP 开发入门教程合集.mp4'
new_name = 'UWP开发入门教程合集_%s'

filePosition = "-o i:/video"

# 文件模板
template = '''
import os

filePosition = "-o i:/video" 
xml_file_path = r'i:/video/UWP 开发入门教程合集.cmt.xml'
old_name = 'UWP 开发入门教程合集.mp4'
new_name = 'UWP开发入门教程合集_%(num)s.mp4'

old_video_path = r'i:/video/' + old_name
new_video_path = r'i:/video/' + new_name

os.system('you-get %(filePosition)s %(true_url)s')

if os.path.exists(xml_file_path):
    os.remove(xml_file_path)

if os.path.exists(old_video_path):
    os.rename(old_video_path,new_video_path)
    
'''
#
d = {}
d['filePosition'] = filePosition

# 根据网址写入文件
for i in range(start_point, end_point):
    
    d['true_url'] = url % i
    d['num'] = h(i) 
    
    python_file_path = r'i:/temp_code/' + h(i) + '.py'

    with open(python_file_path, 'w', encoding = 'utf-8') as f:
        f.write(template % d)

# 运行所有文件里的内容
path = r'I:\temp_code'
for root, dirs, files in os.walk(path):
    for file in files:
        os.system(r'python ' + os.path.join(root,file))