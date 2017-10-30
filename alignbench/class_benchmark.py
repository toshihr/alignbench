# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime
import numpy as np
from alignbench.utility import bcolors
from alignbench.io import makedirs,pack
from alignbench.class_aligner import Aligner

DELIM_OUTFILE = '__'

class Benchmark:
	''' Benchmarking class.
	alignerオブジェクト
	inputfile-outputfile pair list
	options: {opt1: (v1,v2, ...), opt2: (v1,v2,...), ...}
	を受け取ってベンチマークを行うクラス
'''
	def __init__(self, database, aligner_with_full_option_list, scoremakers, outDir, tmpDir):
		self.database = database
		(self.aligner, self.full_option_list) = aligner_with_full_option_list
		self.scoremakers = scoremakers
		self.outDir = outDir
		self.tmpDir = tmpDir

	def make_outFile(self, a_option_str, inFile):
		(dirname,filename) = os.path.split(inFile)
		(shortname,extension) = os.path.splitext(filename)
		# make a fullpath (root + name) if inFile is not null else make a path only
		store_root = os.path.join(self.tmpDir, 'benchmark', self.database.name, self.aligner.name, a_option_str)
		name_without_ext = DELIM_OUTFILE.join( (shortname,) ) if inFile != '' else ''
		return os.path.join(store_root, name_without_ext + '.fasta')

	def run(self, x=None, y=None):
		''' run a benchmark. '''

		# --- initialize ---
		allbenchmark = {}
		self.database.refresh_list()
		num_alignments = self.database.num
		num_scores = sum(len(a_score_bin.scores) for a_score_bin in self.scoremakers)
		score_name_list = []
		for a_score_bin in self.scoremakers:
			for a_score_origin,a_score_name in a_score_bin.scores:
				score_name_list.append(a_score_name)

		# --- output the benchmark information ---
		print('[BENCHMARK][{0}] === DETAILS ==='.format(self.database.name))
		print('[BENCHMARK][{0}] database = {1} [{2}]'.format(self.database.name, self.database.name, num_alignments))
		print('[BENCHMARK][{0}] aligner = {1}'.format(self.database.name, self.aligner.name))
		print('[BENCHMARK][{0}] score = {1} [{2}]'.format(self.database.name, ','.join(score_name_list), num_scores))
		print('[BENCHMARK][{0}] ==============='.format(self.database.name))

		# --- benchmark w.r.t. each option line ---
		for a_option_set in self.full_option_list:
			# --- convert a option line to a string ---
			a_option_cmdline = Aligner.make_a_string_from_optionset(a_option_set, cmdline=True)
			a_option_str = Aligner.make_a_string_from_optionset(a_option_set, cmdline=False)

			# --- make a store dir ---
			(a_benchmark_path,dummy) = os.path.split(self.make_outFile(a_option_str, ''))
			makedirs(a_benchmark_path)

			# --- clear result space ---
			# the type of a_benchmark_allscores is numpy.array
			# row: each score, column: result for each alignment
			a_benchmark_allscores = [np.zeros(num_alignments) for i in range(0,num_scores)]

			# --- initialize input,output sets ---
			inFile_list = []
			outFile_list = []
			for inFile,refFile in self.database.gen_list():
				outFile = self.make_outFile(a_option_str, inFile)
				inFile_list.append(inFile)
				outFile_list.append(outFile)

			# --- output the benchmark information ---
			print('[BENCHMARK][{0}] running... {1}{2} {3}{4}'.format(self.database.name, bcolors.BOLD, self.aligner.name, a_option_cmdline, bcolors.ENDC))

			# BENCHMARK OF A ALIGNER WITH A OPTION START HERE #
			time_aligner_start = datetime.today()

			# --- run an aligner ---
			# results are stored in the storage
			self.aligner.run(inFile_list, outFile_list, a_option_cmdline)

			# BENCHMARK OF A ALIGNER WITH A OPTION FINISH HERE #
			time_aligner_finish = datetime.today()

			# --- output the alignment time ---
			print('[BENCHMARK][{0}] done. spent time={1}{2}{3}'.format(self.database.name, bcolors.OKGREEN, time_aligner_finish-time_aligner_start, bcolors.ENDC))

			# --- calculate scores ---
			# results are stored in the memory
			index_alignment = 0
			for inFile,refFile in self.database.gen_list():
				outFile = self.make_outFile(a_option_str, inFile)

				# --- loop w.r.t. each scoremaker ---
				index_score = 0
				for score_bin in self.scoremakers:
					outScore = outFile + '.' + score_bin.name
					# --- calculate a score ---
					value_list = score_bin.run(ref_name=refFile, target_name=outFile, outFileName=outScore)
					# --- make results ---
					for v in value_list:
						# if the value is None then the value numpy.nan is stored (i don't know why this code does not trhow the exception)
						a_benchmark_allscores[index_score][index_alignment] = v
						index_score += 1
				index_alignment += 1

			# --- collect results ---
			# allbenchmark = { option line 1: [(score 1,result_list 1), ... ], ... }
			allbenchmark[a_option_str] = list(zip(score_name_list, a_benchmark_allscores))

			# --- pack results ---
			storedArcName = pack(a_benchmark_path, erase=True)
			finalOutDir = os.path.join(self.outDir, self.database.name, self.aligner.name)
			makedirs(finalOutDir)
			if os.path.isfile(os.path.join(finalOutDir, os.path.basename(storedArcName))):
				os.remove(os.path.join(finalOutDir, os.path.basename(storedArcName)))
			shutil.move(storedArcName, finalOutDir)
		# allbenchmark = { a_benchmark_path: [(score name, values as numpy.array),] }
		return allbenchmark
