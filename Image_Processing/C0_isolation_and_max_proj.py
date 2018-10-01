# File Processing 13Sept2018
# Just grabbing C0, doing a max projection, and saving.

import os, csv, re
from ij import IJ
from ij.gui import GenericDialog

def get_info():
	srcDir = IJ.getDirectory("Input_Directory")
	if not srcDir:
		print("No input directory selected")
		return
	dstDir = IJ.getDirectory("Output_Directory")
	if not dstDir:
		print("No output directory selected")
		return
	gd = GenericDialog("Process Folder")
	gd.addStringField("File_extension",".lif")
	gd.addStringField("File_name_contains","")
	gd.addCheckbox("Keep directory structure when saving", True)
	gd.showDialog()
	if gd.wasCanceled():
		return
	ext = gd.getNextString()
	containString = gd.getNextString()
	keepDirectories = gd.getNextBoolean()
	for root, directories, filenames in os.walk(srcDir):
		for filename in filenames:
      # Check for file extension
			if not filename.endswith(ext):
				continue
      # Check for file name pattern
			if containString not in filename:
				continue
			print(srcDir)
			print(filename)
			process(srcDir, dstDir, root, filename, keepDirectories)

def process(srcDir, dstDir, currentDir, filename, keepDirectories):
	print "Processing:"
   
  # Opening the image
	print "Open image file", filename
	IJ.run("Bio-Formats Importer", str("open=" + os.path.join(srcDir, filename) + " color_mode=Colorized open_files open_all_series display_metadata rois_import=[ROI manager] split_channels view=Hyperstack stack_order=XYCZT use_virtual_stack"))
	
	# Exporting the Metadata to .csv
	IJ.selectWindow(str("Original Metadata - " + filename))
	IJ.saveAs("Text", str(os.path.join(dstDir, str("Original Metadata - " + filename[0:-4] + ".csv"))))

	# Determines Number of Series and their names from Metadata
	md_file = open(str(os.path.join(dstDir, str("Original Metadata - " + filename[0:-4] + ".csv"))))
	md_reader = csv.reader(md_file)
	md_array = list(md_reader)
	find_series = re.compile(r'Series', re.IGNORECASE)
	index = []
	for i in range(len(md_array)):
		for x in range(0,2):
			strv = str(md_array[i][x])
			please = find_series.findall(strv)
			if please != []:
				index.append(str(md_array[i][x+1]))

	# Primary Processing Loop

	channels = ['C=0', 'C=1', 'C=2', 'C=3']
	for i in range(len(index)):
		print('loopedy loop')
		# Dealing with Channel 0
		IJ.selectWindow(str(filename + ' - ' + index[i] + ' - '+channels[0]))
		IJ.run("Z Project...", "projection=[Max Intensity]")
		IJ.saveAs("Tiff", str(os.path.join(dstDir, str("Max_" + filename[0:-4] + ' - ' + index[i] + ".tif"))))
		imp=IJ.getImage()
		imp.close()
		IJ.selectWindow(str(filename + ' - ' + index[i] + ' - '+channels[0]))
		imp=IJ.getImage()
		imp.close()
		# Dealing with excess channels
		IJ.selectWindow(str(filename + ' - ' + index[i] + ' - '+channels[1]))
		imp=IJ.getImage()
		imp.close()
		IJ.selectWindow(str(filename + ' - ' + index[i] + ' - '+channels[2]))
		imp=IJ.getImage()
		imp.close()
		IJ.selectWindow(str(filename + ' - ' + index[i] + ' - '+channels[3]))
		imp=IJ.getImage()
		imp.close()

	
get_info()
print('finished')
	
