import os

path = '/Users/andrewstewart/CI_Images/Oct_4_18_Spawning/Timelapse/20181004'
files = os.listdir(path)
files_sorted = sorted(files)
del files_sorted[0]
serials = ["{0:03}".format(i) for i in range(len(files_sorted))]

for i in range(len(files_sorted)):
    os.rename(str(path+'/'+files_sorted[i]), str(path+'/timelapse'+serials[i]+'.tif'))

print('finished')
