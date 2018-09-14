# To use this program simply replace the file paths on lines 6 and 9
# with the path to the folder containing the images and the path to the Metadata
# file respecitively. This will allow for the program to check the filenames
# against the metadata to ensure that there are matches

import os, csv, re

files = []
for filenames in os.walk('/Users/andrewstewart/ImageJ_testing/20180830-NZ-repeat'):
    files.append(filenames)

comma_file = open('/Users/andrewstewart/ImageJ_testing/20180830-NZ-repeat/Original_Metadata_-_20180830-NZ-repeat.csv')
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
