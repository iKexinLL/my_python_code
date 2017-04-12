#encoding=utf-8
"""
Created on 2016/3/18 15:15
author: iKexinLL
或许应该确认第一层大小, 第二层大小, 这样可以方便的找出每个文件下的文件大小了
get_size 统计目前的C盘74.5/145, 用时33min
"""

import os

def get_size_error(dir):
    """
    这样子写的话, 无法获取root下面的子文件夹的大小(只能获取当前目录下的文件大小)
    一个root_size的大小,应该是当前root下的文件大小加上root下的子文件夹的总和
    :param dir:
    :return:
    """
    result = {'file_size' : {}, 'root_size' : {}}
    for root, dirs, files in os.walk(dir):
        result['root_size'][root] = 0
        for file in files:
            try:
                path = os.path.join(root, file)
                size = round(os.path.getsize(path) /1024/1024, 2)
                result['file_size'][path] = size
                result['root_size'][root] += size
            except PermissionError:
                continue
            except FileNotFoundError:
                continue

    return result



def get_size(dir):
    """
    这样子写的话, 可以获取root下面的子文件夹的大小
    一个root_size的大小,应该是当前root下的文件大小加上root下的子文件夹的总和
    :param dir:
    :return:
    """
    searched_root = [dir]
    result = {'file_size' : {}, 'root_size' : {}}
    for root, dirs, files in os.walk(dir):
        result['root_size'].setdefault(root, 0)
        searched_root.append(root)
        for file in files:
            try:
                path = os.path.join(root, file)
                size = round(os.path.getsize(path) /1024/1024, 2)
                result['file_size'][path] = size
                result['root_size'][root] += size
                last_root = root.rpartition('\\')[0]
                for _ in range(root.count('\\') - 1):
                    if last_root in searched_root:
                        result['root_size'][last_root] += size
                    last_root = last_root.rpartition('\\')[0]
            except PermissionError:
                continue
            except FileNotFoundError:
                continue

    return result


def get_root_size(result, level = 1, rank = 0, reverse = True):

    root_size = [(x, result['root_size'][x]) for x in result['root_size'] if x.count('\\') == level]

    if rank > 0:
        root_size = sorted(root_size, key = lambda x: x[1], reverse = reverse)[:rank]

    return root_size

def fun_print(text):
    print(text)


#size = get_size(r'D:\Program Files\Microsoft Office')
#print ('There are %.3f' % (size/1024/1024), 'Mbytes in c:\\windows')
#sorted_size = sorted(file_size.items(), key = lambda x: x[1], reverse = True)