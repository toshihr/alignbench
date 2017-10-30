# -*- coding: utf-8 -*-
import os
import re
import shlex
import subprocess
from alignbench.io import makedirs

class ScoreMaker:
	''' Q Score and so on. '''
	def __init__(self, name, exec_name, option, refStyle, targetStyle, outStyle, refFormat, testFormat, scores, quiteErr=False):
		try:
			self.name = name
			self.exec_name = exec_name
			self.option = option
			self.refStyle = refStyle
			self.targetStyle = targetStyle
			self.outStyle = outStyle
			self.refFormat = refFormat
			self.testFormat = testFormat
			self.scores = scores
			self.quiteErr = quiteErr

			# check
			assert self.refFormat in ('fasta','xml'), 'refFormat should be one of fasta, xml.'
			assert self.testFormat in ('fasta','msf'), 'refFormat should be one of fasta, msf.'
			#assert os.access(self.exec_name, os.X_OK), '{0} is not executable.'.format(self.exec_name)

			self.regex = re.compile('([^=,;]+)=([^=,;]+)')

		except AssertionError() as e:
			print(e.args)

	def make_msf(fasta_name, msf_name):
		# TODO: bali score用にいつか作る
		pass

	def run(self, ref_name, target_name, outFileName):
		''' return the scores
		ref_name: reference sequence file name (ext. should be .ref_fasta)
		target_name: test sequence file name (ext. should be .fasta)
'''
		# --- make output dirs ---
		makedirs(os.path.dirname(outFileName))

		# --- treat input file name if necessary ---
		if self.refFormat == '.xml':
			ref_name = ref_name[:-len('.ref_fasta')] + '.xml'
		if self.testFormat == '.msf':
			msf_name = target_name[:-len('.fasta')] + '.msf'
			self.make_msf(target_name, msf_name)
			target_name = msf_name

		# --- make args ---
		cmdline = self.exec_name + ' ' + self.option
		# reference style
		if self.refStyle is not None:
			cmdline += ' ' + self.refStyle + ref_name
		# target style
		if self.targetStyle is not None:
			cmdline += ' ' + self.targetStyle + target_name
		# output style
		if self.outStyle is not None:
			cmdline += ' ' + self.outStyle + outFileName
		# split cmdline
		args = shlex.split(cmdline)

		# --- execute ---
		try:
			p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		except OSError:
			print('Failed to execute command: ' + args[0])
		# read outputs
		(stdoutdata,stderrdata) = p.communicate()
		# treat stdout as an output if inStyle is None
		if self.outStyle is None and stdoutdata is not None:
			f = open(outFileName, 'w')
			f.write(stdoutdata.decode('utf-8'))
			f.close()
		# treat errors
		if stderrdata:
			pass
#			print(stderrdata.decode('utf-8'))

		# --- treat scores ---
		# algorithm: search [, or ;][score name]=[score value][, or ;] line then grab them.
		allLines = ''
		with open(outFileName, 'r') as f:
			allLines = f.read()
		keys = [score_original for score_original,score_name in self.scores]
		results = {}
		for score,value in self.regex.findall(allLines):
			if score.strip() in keys:
				results[score.strip()] = float(value.strip())
		# result should be returned with the correct order and with the correct dimension
		return_value_list = [results[name] if name in results.keys() else None for name in keys]
		return return_value_list
