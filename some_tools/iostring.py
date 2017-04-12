#encoding=utf-8
"""
Created on 2016/3/16 18:11
author: iKexinLL
"""

import io
import sys
import string
import random
import os

save_path = os.getcwd()

char_list = [random.choice(string.ascii_lowercase) for x in range(100)]
out_str = ''.join(char_list)

sys.stdout = io.StringIO()

sys.stdout.write(out_str)

#print(out_str, file = sys.stdout )
print(os.path.join(save_path, "iostring.txt"))



print('sys.stdout.getvalues()' + sys.stdout.getvalues())