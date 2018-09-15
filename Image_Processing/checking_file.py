#! python3
# Crossreferences images with the metadata 

import os
import csv
import re
from tkinter import filedialog as fd

currentdir = os.getcwd()

in_path = fd.askdirectory(initialdir=currentdir, title='Choose Folder')
# in_path = pre_in_path.name
comma_file = fd.askopenfilename(initialdir=currentdir, title='Choose Metadata File')
for i in range(0, 1):
    if len(comma_file) > 0:
        continue
    else:
        break
    if len(in_path) > 0:
        continue
    else:
        break

files = []
for filenames in os.walk(in_path):
    files.append(filenames)

# comma_file = open(meta_file)
comma_reader = csv.reader(comma_file)
comma_list = list(comma_reader)

find_series = re.compile(r'Series', re.IGNORECASE)
index = []
for i in range(len(comma_list)):
    for x in range(0, 2):
        strv = str(comma_list[i][x])
        please = find_series.findall(strv)
        if please != []:
            index.append(str(comma_list[i][x+1]))

check = []
for i in range(len(files)):
    sturv = files[i]
    if (x for x in index if sturv in x) != '':
        continue
    else:
        check.append(sturv)

print(check)
