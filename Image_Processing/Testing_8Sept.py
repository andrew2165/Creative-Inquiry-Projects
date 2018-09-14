# Testing_8Sept.py

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
	IJ.run("Bio-Formats Importer", str("open=" + os.path.join(srcDir, filename) + " autoscale color_mode=Colorized open_files open_all_series display_metadata rois_import=[ROI manager] split_channels view=Hyperstack stack_order=XYCZT"))
	
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


	# PRIMARY PROCESSING LOOP

	
	# Using Series Information, the images can now be processes properly
	channels = ['C=0', 'C=1', 'C=2', 'C=3']
	it_chan = iter(channels)
	for i in range(len(index)):
		IJ.selectWindow(str(filename + ' - ' + index[i] + ' - '+channels[0]))
		IJ.run("Z Project...", "projection=[Max Intensity]")
		IJ.selectWindow(str(filename + ' - ' + index[i] + ' - '+channels[1]))
		IJ.run("Z Project...", "projection=[Max Intensity]")
		IJ.selectWindow(str(filename + ' - ' + index[i] + ' - '+channels[2]))
		IJ.run("Z Project...", "projection=[Max Intensity]")
		#od = GenericDialog("Gray Field Slice")
		#od.addStringField("Which Layer is most in focus for C4?","")
		#od.showDialog()
		#if gd.wasCanceled():
		#	break
		#gf = od.getNextString()
		
		IJ.run("Merge Channels...", str("c2=[MAX_"+filename+" - "+index[i]+" - C=0] c3=[MAX_"+filename+" - "+index[i]+" - C=2] c6=[MAX_"+filename+" - "+index[i]+" - C=1] create keep"))
		IJ.selectWindow(str(filename + ' - ' + index[i] + ' - '+channels[0]))
		imp=IJ.getImage()
		imp.close()
		IJ.selectWindow(str(filename + ' - ' + index[i] + ' - '+channels[1]))
		imp=IJ.getImage()
		imp.close()
		IJ.selectWindow(str(filename + ' - ' + index[i] + ' - '+channels[2]))
		imp=IJ.getImage()
		imp.close()
		
# TODO:
# Figure out how to deal with Channel 3 (4) grayscale
# Figure out how to get the composite to work correctly
# Figure out how to make this program as generic as possible to deal with Vera's naming
# Just make the program as agnostic as possible
# And don't forget about adding an error bar


   
  # Saving the image
	# saveDir = currentDir.replace(srcDir, dstDir) if keepDirectories else dstDir
	# if not os.path.exists(saveDir):
		# os.makedirs(saveDir)
	# print "Saving to", saveDir
	# IJ.saveAs(imp, "Tiff", os.path.join(saveDir, fileName));
	# imp.close()


get_info()
