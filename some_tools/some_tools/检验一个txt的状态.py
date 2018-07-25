

import os
import time
import datetime
import re

p = re.compile('; |；|;')
file_path = r'I:\单词\单词整理.txt'


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

old_modify_time = TimeStampToTime(os.path.getatime(file_path))
new_time = ''


while 1:
    # 添加一个sleep,防止cpu过高
    time.sleep(0.1)
    new_time = TimeStampToTime(os.path.getatime(file_path))
    if new_time == old_modify_time:
        print(1)
    else:
        with open(file_path, encoding='utf-8') as fr:
            lt = []
            tp = fr.readlines()
            for line in tp:
                lt.append(re.sub(p, ',', line))
        
        with open(file_path, 'w', encoding='utf-8') as fw:
            fw.write(''.join(lt))

        old_modify_time = TimeStampToTime(os.path.getatime(file_path))
        # break
                
