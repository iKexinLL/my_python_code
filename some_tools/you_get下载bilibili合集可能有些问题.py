
import os 

url = 'https://www.bilibili.com/video/av7997007/?p=%s'

start_point = 1
end_point = 81
old_name = 'UWP 开发入门教程合集.mp4'
new_name = 'UWP开发入门教程合集_%s.mp4'

filePosition = "-o i:/video"

old_video_path = r'i:/video/' + old_name
xml_file_path = r'i:/video/UWP 开发入门教程合集.cmt.xml'

for i in range(start_point, end_point):

    new_video_path = r'i:/video/' + new_name % i

    if os.path.exists(old_video_path):
        os.rename(old_video_path,new_video_path)
    if os.path.exists(xml_file_path):
        os.remove(xml_file_path)
    true_url = url % i
    print('you-get %s %s' % (filePosition, true_url))
    os.system('you-get %s %s' % (filePosition, true_url))


# os.system('shutdown -s')