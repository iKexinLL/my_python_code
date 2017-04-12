'''
    网易云下载的一些音乐有同一首歌但是不同版本的歌曲,
    比如
        If I Let You Go (Acoustic) - unplug - Westlife
        If I Let You Go (Live) - Westlife
        If I Let You Go (Radio Edit) - Westlife
    所以还是删一删比较好,
    不够智能化, delete方法只能传一个歌曲名,忘了怎么弄了
'''

import re
import os 
import collections

path = r'F:\westlife'

songsName = [x for x in os.walk(path)][0][2]

p1 = re.compile('-|\(')

allSongsName = [re.split(p1, x)[0].strip() for x in songsName]

songsCounter = collections.Counter(allSongsName)

multiSongsName = [(m, n)[0] for m, n in songsCounter.items() if n > 1]

res = []

for m in range(len(allSongsName)):
    if allSongsName[m] in multiSongsName:
        res.append(songsName[m])

res.sort()

def delete_songs(songName, path = path):
    songPath = os.path.join(path, songName)
    os.remove(songPath)

    res.remove(songName)

    print('deleted ' + songPath)
    print([x + '\n' for x in res])
    return None