
import os
import easygui as eg
import psutil
import tempfile

temp_path = os.environ['TEMP'] + '\process.txt'

with open(temp_path) as f:
    for pid in psutil.process_iter():
        a = psutil.Process(pid)

