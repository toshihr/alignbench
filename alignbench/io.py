# -*- coding: utf-8 -*-
import tarfile
import shutil
import os

def makedirs(dirName):
	try:
		os.makedirs(dirName)
	except OSError:
		pass

def pack(dirName, erase=False, addDirName=True):
	'''
		pack dir.
		ex.) ./dirName/data1
                           data2
                             ...
               are stored in dirName.tar.bz2 with relative path dirName/data1,...

	'''
	# .tar.gz -> mode=gz
	arcName = dirName + '.tar.bz2'
	th = tarfile.open(arcName, 'w:bz2')
	for root, dirs, files in os.walk(dirName):
		for f in files:
			fullpath = os.path.join(root, f)
			#above_dir = os.path.basename(root)
			#relativepath = os.path.join(above_dir, f)
			if addDirName:
				relativepath = fullpath[len(os.path.dirname(dirName) + os.path.sep):]
			else:
				relativepath = fullpath[len(dirName + os.path.sep):]
				
			# archive relative path
			th.add(fullpath, arcname=relativepath)
	th.close()

	if erase:
		shutil.rmtree(dirName, ignore_errors=True)

	return arcName
