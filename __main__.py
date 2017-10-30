#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
from alignbench import Resource,ScoreMaker,Aligner,Database,IO_LISTMODE,FLAG,SILENT,RANGES,run,init_mode
from collections import defaultdict

def setDefaultOptionValue(RESOURCE, tmpDir):
	# if sys.platform == 'darwin':
	# 	databaseDir = '/Users/keru/Dropbox/database'
	# elif 'linux' in sys.platform:
	# 	databaseDir = '/home/keru/research/database'

	RESOURCE['general'].update({
		'pluginDir': os.path.join('.','plugin'),
		'databaseDir': os.path.join('.','database'),
		'outDir': '',
	# output filename
		'outFile_stats': 'stats.csv',
		'outFile_summary': 'summary.txt',

	# after the benchmark this dir will be removed
		'tmpDir': tmpDir,
	# the number of parallel processes
		'num_of_process': 1,
		'statMethod': 'coin', # one of coin, R, python
	})


### MAIN PROGRAM ###
if __name__ == '__main__':
	# target benchmark
	if len(sys.argv) > 1:
		a_benchmark_name = sys.argv[1]
	else:
		a_benchmark_name = 'bench_templete.py'

	# global variable
	today = datetime.datetime.today()
	tmpDir = os.path.join(os.environ['HOME'],'tmp', '{0:04}{1:02}{2:02}'.format(today.year,today.month,today.day))

	RESOURCE = {}
	RESOURCE['general'] = {}
	RESOURCE['score_generaters'] = {}
	RESOURCE['aligners'] = {}
	RESOURCE['databases'] = {}

	setDefaultOptionValue(RESOURCE, tmpDir=tmpDir)

	RESOURCE['general']['outDir'] = os.path.join('.', '{0}_{1:04}{2:02}{3:02}'.format(os.path.splitext(a_benchmark_name)[0], today.year,today.month,today.day))

	# search resources
	if os.path.exists(RESOURCE['general']['pluginDir']):
		for root,dirs,files in os.walk(RESOURCE['general']['pluginDir']):
			for a_file in files:
				if os.path.splitext(a_file)[1] != '.py':
					continue
				fullName = os.path.join(root,a_file)
				with open(fullName) as script: exec(script.read())

	RES = Resource()
	for k,v in RESOURCE['general'].items(): RES.add_with_key('general',k,v)
	for a_name,a_param in RESOURCE['score_generaters'].items(): RES.addObj(ScoreMaker(name=a_name,**a_param))
	for a_name,a_param in RESOURCE['aligners'].items(): RES.addObj(Aligner(name=a_name,**a_param))
	for a_name,a_param in RESOURCE['databases'].items():
		a_param = a_param.copy()
		arcName = a_param.pop('arcName')
		if os.path.dirname(arcName) == '':
			arcName = os.path.join(RESOURCE['general']['databaseDir'], arcName)
		RES.addObj(Database(name=a_name,tmpDir=tmpDir,arcName=arcName,**a_param))

	# load benchmark setting
	print('load a benchmark setting...: {0}'.format(a_benchmark_name))
	with open(a_benchmark_name) as script: exec(script.read())

	# initialize statistical method
	init_mode(RESOURCE['general']['statMethod'])

	# execute the benchmark
	run(RES, BENCH)



