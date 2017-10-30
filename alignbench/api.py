# -*- coding: utf-8 -*-

'''
Requirements:
  python >=2.7.3 or >= 3.0
  numpy, scipy, rpy2 package
  R and coin library

'''

__all__ = ['run','_test']

import itertools
import os
import time
import csv
import tarfile # for unpack an archive
import shutil # for delete tmp files
import glob # for search dir
import subprocess # for execute an external process
import shlex # for parsing a cmdline
import sys # for exit
import numpy as np # for vector calculations
import warnings
from functools import partial
from multiprocessing import Pool
from datetime import datetime
import logging
import logging.handlers
import collections
from math import floor
import matplotlib.pyplot as plt

from alignbench.io import makedirs
from alignbench.class_aligner import Aligner
from alignbench.class_benchmark import Benchmark
from alignbench.class_statisticalanalyzer import StatisticalAnalyzer
from alignbench.utility import bcolors

# === MAIN ===
class RunOption:
	def RunOption(aligner_with_full_option = collections.defaultdict(list),
					aligner_x_with_full_option = collections.defaultdict(list),
					id_range_list = [],
					id_global = True,
					scoremakers = [],
					databaseDir = '',
					outDir = '',
					tmpDir = '',
					outFile_stats = '',
					outFile_summary = ''):

		self.aligner_with_full_option = aligner_with_full_option
		self.aligner_x_with_full_option = aligner_x_with_full_option
		self.id_range_list = id_range_list
		self.id_global = id_global
		self.scoremakers = scoremakers
		self.databaseDir = databaseDir
		self.outDir = outDir
		self.tmpDir = tmpDir
		self.outFile_stats = outFile_stats
		self.outFile_summary = outFile_summary

def run_benchmark_for_a_database(a_database, runOption):
	# init variables
	a_benchmark_summary = []

	# BENCHMARK OF A DATABASE STARTED HERE #
	time_database_start = datetime.today()
	a_benchmark_summary.append('[{0}] start time: {1}'.format(a_database.name, time_database_start.strftime("%Y-%m-%d %H:%M:%S")))

	try:
		# --- init database ---
		# unpack the database
		a_database.unpack()
		a_database.refresh_list(runOption.id_global)
		# output the identity file
		makedirs(os.path.join(runOption.outDir,a_database.name))
		with open(os.path.join(runOption.outDir,a_database.name,'identity.csv'), 'w') as f:
			for inFile,refFile,identity in a_database.inFile_refFile_list:
				f.write('{0},{1}\n'.format(os.path.basename(refFile),identity))

		# --- run benchmarks ---
		benchmarks = []
		for a_aligner, a_full_option_list in runOption.aligner_with_full_option.items():
			a_bench_set = Benchmark(a_database, (a_aligner,a_full_option_list), runOption.scoremakers, runOption.outDir, runOption.tmpDir)
			a_benchmark_result = a_bench_set.run()
			benchmarks.append( (a_aligner.name, a_benchmark_result) )

		# --- analyze & output the results ---
		analyze = StatisticalAnalyzer(benchmarks, a_database, runOption.outDir, runOption.outFile_stats, runOption.tmpDir)
		analyze.run(runOption.id_range_list, runOption.aligner_x_with_full_option)

		# --- output the option details to the summary file ---
		option_fullcmdline = {}
		for a_aligner, a_full_option_list in runOption.aligner_with_full_option.items():
			for a_option_set in a_full_option_list:
				# make a full of option
				opt_short = Aligner.make_a_string_from_optionset(a_option_set, cmdline=False, full=False)
				opt_full = Aligner.make_a_string_from_optionset(a_option_set, cmdline=True, full=True)
				option_fullcmdline[opt_short] = opt_full
		a_benchmark_summary.append('# option details:')
		for short,full in option_fullcmdline.items():
			a_benchmark_summary.append('{0},{1}'.format(short,full))

		# --- clean up the database ---
		a_database.clean()

		# BENCHMARK OF A DATABASE FINISHED HERE #
		time_database_finish = datetime.today()
		a_benchmark_summary.append('[{0}] finish time: {1}'.format(a_database.name, time_database_finish.strftime("%Y-%m-%d %H:%M:%S")))
		a_benchmark_summary.append('[{0}] elapsed time: {1}'.format(a_database.name, time_database_finish-time_database_start))

		# --- output the summary ---
	#		print('[{0}]SUMMARY OF THE BENCHMARK'.format(a_database.name))
		with open(os.path.join(runOption.outDir,a_database.name,runOption.outFile_summary), 'w') as f:
			for line in a_benchmark_summary:
	#				print(line)
				f.write(line+'\n')
	except Exception as e:
		print('[ERROR]{0}'.format(e))


def run(RES, BENCH):
	# check
	RES.check_minor_keys('Database', BENCH['databases'])
	RES.check_minor_keys('ScoreMaker', BENCH['scoremakers'])
	RES.check_minor_keys('Aligner', [a_name for a_name,a_option in BENCH['alignerset'] ])
	RES.check_minor_keys('Aligner', [a_name for a_name,a_option in BENCH['alignerset_compared'] ])

	# correct objects for the benchmark
	databases = [RES['Database'][a_name] for a_name in BENCH['databases'] ]
	aligner_with_compressed_option = [(RES['Aligner'][a_name],a_option) for a_name,a_option in BENCH['alignerset'] ]
	aligner_x_with_compressed_option = [(RES['Aligner'][a_name],a_option) for a_name,a_option in BENCH['alignerset_compared'] ]

	# --- init ---
	runOption = RunOption()
	runOption.id_range_list = BENCH['id_range_list']
	runOption.id_global = BENCH['id_global']
	runOption.scoremakers = [RES['ScoreMaker'][a_name] for a_name in BENCH['scoremakers'] ]
	runOption.databaseDir = RES['general']['databaseDir']
	runOption.outDir = RES['general']['outDir']
	runOption.tmpDir = tmpDir = RES['general']['tmpDir']
	runOption.outFile_stats = RES['general']['outFile_stats']
	runOption.outFile_summary = RES['general']['outFile_summary']

	num_of_process = RES['general']['num_of_process']
	outFile_summary = RES['general']['outFile_summary']

	# --- init pool ---
	p = Pool(num_of_process)
	print('[ROOT PROCESS] the number of process = {0}'.format(num_of_process))

	# --- necessary treatment ---
	# make a full path
	runOption.outDir = os.path.abspath(runOption.outDir)
	runOption.tmpDir = os.path.abspath(runOption.tmpDir)
	makedirs(runOption.outDir)
	makedirs(runOption.tmpDir)

	# --- generate aligner with option list ---
	# expand the options and merge the options if the aligner is same
	runOption.aligner_with_full_option = collections.defaultdict(list)
	for a_aligner,a_option_set in aligner_with_compressed_option:
		runOption.aligner_with_full_option[a_aligner].extend( Aligner.expand_options(a_option_set) )
	runOption.aligner_x_with_full_option = collections.defaultdict(list)
	for a_aligner,a_option_set in aligner_x_with_compressed_option if aligner_x_with_compressed_option is not None else {}:
		runOption.aligner_x_with_full_option[a_aligner].extend( Aligner.expand_options(a_option_set) )

	# merge aligner x to aligner list
	for a_aligner,a_full_option_list in runOption.aligner_x_with_full_option.items():
		runOption.aligner_with_full_option[a_aligner].extend(a_full_option_list)

	# if the aligner_x_with_full_option is empty, then add the first node of aligner_with_full_option
	if len(runOption.aligner_x_with_full_option) == 0:
		a_aligner,a_full_option_list = list(runOption.aligner_with_full_option.items())[0]
		runOption.aligner_x_with_full_option[a_aligner].extend(a_full_option_list)

	# omit duplicates
	for a_aligner, a_full_option_list in runOption.aligner_with_full_option.items():
		new_list = []
		for a_full_option_dict in a_full_option_list:
			if a_full_option_dict not in new_list:
				new_list.append(a_full_option_dict)
		runOption.aligner_with_full_option[a_aligner] = new_list
	for a_aligner, a_full_option_list in runOption.aligner_x_with_full_option.items():
		new_list = []
		for a_full_option_dict in a_full_option_list:
			if a_full_option_dict not in new_list:
				new_list.append(a_full_option_dict)
		runOption.aligner_x_with_full_option[a_aligner] = new_list

	# here we have the followings:
	# runOption.aligner_with_full_option = {Aligner -> [dict(options),...]}
	# runOption.aligner_x_with_full_option = {Aligner -> [dict(options),...]}

	# --- make a unique identity range list ---
	sorted(set(runOption.id_range_list), key=runOption.id_range_list.index)

	# BENCHMARK STARTED HERE #
	time_all_start = datetime.today()

	# --- main loop ---
	pool_return = p.map_async(partial(run_benchmark_for_a_database, runOption=runOption), databases)
	p.close()

	# wait finish
	while not pool_return.ready():
		time.sleep(1)
	
	p.join()

	# BENCHMARK FINISHED HERE #
	time_all_finish = datetime.today()

	# --- output the total summary ---
	print('')
	print(bcolors.BOLD + 'Total elapsed time: {0}.'.format(time_all_finish - time_all_start) + bcolors.ENDC)
	for a_database in databases:
		print(bcolors.BOLD + 'The benchmark results of {0} are stored in {1} and ...{2}{3}'.format(a_database.name, os.path.join(runOption.outDir,a_database.name,runOption.outFile_stats), os.path.sep, outFile_summary) + bcolors.ENDC)

	# --- clean up ---
	for a_aligner, a_full_option_list in runOption.aligner_with_full_option.items():
		a_aligner.clean()
	shutil.rmtree(tmpDir)

def _test():
	import doctest
	doctest.testmod(verbose=False)	

if __name__ == '__main__':
	_test()
