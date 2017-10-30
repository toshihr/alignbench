# -*- coding: utf-8 -*-
import itertools
import os
import shlex
import subprocess
from alignbench.io import makedirs
from alignbench.fasta import msf2fasta, Fasta

DELIM_OPTION_BETWEEN = '_'
DELIM_OPTION_KEY_AND_VALUE = '='

class Aligner:
	''' This is a class of aligner.'''

	def __repr__(self):
		return 'Aligner[{0}]'.format(self.name)

	def __init__(self, name, exec_name, inStyle, outStyle, outFormat, necessaryOption='', quiteErr=False, removeFiles=None):
		'''
		inStyle:  (1)None: use stdin as an input, (2)IO_LISTMODE: use 'inStyle' option as inputs/outputs and (3)otherwise: use 'inStyle' option as an input
		outStyle: (1)None: use stdout as an output, (2)IO_LISTMODE: use 'inStyle' option as inputs/outputs and (3)otherwise: use 'outStyle' option as an out
		'''
		self.name = name
		self.exec_name = exec_name
		self.inStyle = inStyle
		self.outStyle = outStyle
		self.outFormat = outFormat
		self.quiteErr = quiteErr
		self.removeFiles = removeFiles

		if len(necessaryOption) > 0:
			self.necessaryOption = ' ' + necessaryOption
		else:
			self.necessaryOption = ''

	def clean(self):
		if self.removeFiles:
			for f in self.removeFiles:
				if os.path.isfile(f):
					os.remove(f)

	@staticmethod
	def expand_options(compressed_view):
		''' make a set of options list from compressed view.

		>>> cv = { '-opt1': (1,2,3), '-opt2': ['a'], '-opt3=':'b'}
		>>> Aligner.expand_options(cv)
		[{'-opt1': 1, '-opt2': 'a', '-opt3=': 'b'}, {'-opt1': 2, '-opt2': 'a', '-opt3=': 'b'}, {'-opt1': 3, '-opt2': 'a', '-opt3=': 'b'}]

		>>> Aligner.expand_options(OPTION_DEFAULT)
		[{}]

		>>> cv = { '-opt1': FLAG, }
		>>> Aligner.expand_options(cv)
		[{'-opt1': ''}]

		>>> cv = { '-opt1': 'GONNET', }
		>>> Aligner.expand_options(cv)
		[{'-opt1': 'GONNET'}]

		'''
		# if the values is not tuple or list, change it to tuple
		for k,v in compressed_view.items():
			if v.__class__.__name__ != 'tuple' and v.__class__.__name__ != 'list':
				compressed_view[k] = (v,)

		# make a generator of options
		gen_options = ( dict(zip(compressed_view.keys(), x)) for x in itertools.product(*compressed_view.values() ) )
		# make a list of options. each option set is called a option set.
		options_list = [x for x in gen_options]
		return options_list

	@staticmethod
	def make_a_string_from_optionset(a_option_set, cmdline=False, full=False):
		''' make a string from the set of options.

		>>> a_option_set1 = {'-opt1': 1, '-opt2': 'a'}
		>>> Aligner.make_a_string_from_optionset(a_option_set1, cmdline=False, full=False)
		'1_a'
		>>> Aligner.make_a_string_from_optionset(a_option_set1, cmdline=False, full=True)
		'opt1=1_opt2=a'
		>>> Aligner.make_a_string_from_optionset(a_option_set1, cmdline=True, full=False)
		'-opt1 1 -opt2 a'
		>>> Aligner.make_a_string_from_optionset(a_option_set1, cmdline=True, full=True)
		'-opt1 1 -opt2 a'

		>>> a_option_set2 = {}
		>>> Aligner.make_a_string_from_optionset(a_option_set2, cmdline=False, full=False)
		'DEFAULT'
		>>> Aligner.make_a_string_from_optionset(a_option_set2, cmdline=False, full=True)
		'DEFAULT'
		>>> Aligner.make_a_string_from_optionset(a_option_set2, cmdline=True, full=False)
		''
		>>> Aligner.make_a_string_from_optionset(a_option_set2, cmdline=True, full=True)
		''

		>>> a_option_set3 = {'-opt1=': '', '-opt2=': 'a'}
		>>> Aligner.make_a_string_from_optionset(a_option_set3, cmdline=False, full=False)
		'a_opt1F'
		>>> Aligner.make_a_string_from_optionset(a_option_set3, cmdline=False, full=True)
		'opt2=a_opt1F'
		>>> Aligner.make_a_string_from_optionset(a_option_set3, cmdline=True, full=False)
		'-opt2=a -opt1='
		>>> Aligner.make_a_string_from_optionset(a_option_set3, cmdline=True, full=True)
		'-opt2=a -opt1='

		>>> a_option_set4 = {SILENT('-opt1='): '', '-opt2=': 'a'}
		>>> Aligner.make_a_string_from_optionset(a_option_set4, cmdline=False, full=False)
		'a'
		>>> Aligner.make_a_string_from_optionset(a_option_set4, cmdline=False, full=True)
		'opt2=a'


		'''
		a_option_str = ''
		if cmdline:
			# combine a option line to a string
			options = []
			for k,v in a_option_set.items():
				a_cmd = ''
				if k.__class__.__name__ == 'SILENT':
					# silent option i.e. the option will not be appeared in string result
					a_cmd += str(k.value)
				elif v != '':
					# option and value
					a_cmd += str(k)
				else:
					# flag option
					a_cmd += str(k)

				if v != '' and a_cmd[-1] != '=':
					a_cmd += ' '

				a_cmd += str(v)
				options.append(a_cmd)

			a_option_str = ' '.join(options)
		else:
			# combine a option set to a string
			def option_modify(k):
				''' omit the first -,--,space and the last space and = '''
				stripped = str(k).strip()
				if stripped[0] == '-':
					stripped = stripped[1:]
				if stripped[0] == '-':
					stripped = stripped[1:]
				if stripped[-1] == '=':
					stripped = stripped[:-1]
				return stripped

			def value_modify(v):
				''' exchange / to S '''
				stripped = str(v).strip().replace('/','S')
				return stripped

			if full:
				options = []
				for k,v in a_option_set.items():
					if k.__class__.__name__ == 'SILENT':
						# silent option i.e. the option will not be appeared in string result
						pass
					elif v != '':
						# option and value
						options.append(option_modify(k)+DELIM_OPTION_KEY_AND_VALUE+value_modify(v))
					else:
						# flag option
						options.append(option_modify(k)+'F')
				a_option_str = DELIM_OPTION_BETWEEN.join(options)
			else:
				# short version (only values)
				# if an option is FLAG then a string will be key otherwise a string will be key's value
				options = []
				for k,v in a_option_set.items():
					if k.__class__.__name__ == 'SILENT':
						# silent option i.e. the option is not appeared in string
						pass
					elif v != '':
						options.append(value_modify(v))
					else:
						# flag option
						options.append(option_modify(k)+'F')
				a_option_str = DELIM_OPTION_BETWEEN.join(options)
			# if there is no options, i.e. all options are SILENT, then set a string DEFAULT
			if a_option_str == '':
				a_option_str = 'DEFAULT'
		return a_option_str

	# TODO: inFileリストを受け付けるバージョンを作成する。MTRAP高速化に対応させるため。
	def run(self, inFileName_list, outFileName_list, option=None):
		''' execute the aligner.
		outFileName: output filename without extension
		if the type of inFileName,outFileName are the list, run w.r.t each in/out File
		'''
		if not inFileName_list.__class__.__name__ == 'list':
			inFileName_list = [inFileName_list,]
		if not outFileName_list.__class__.__name__ == 'list':
			outFileName_list = [outFileName_list,]

		# --- make dirs ---
		makedirs(os.path.dirname(outFileName_list[0]))

		if self.inStyle.__class__.__name__ == 'IO_LISTMODE':
			# --- make a listfile ---
			# NOTE: now not use tmpDir
			io_listfile = os.path.join(os.path.dirname(outFileName_list[0]), '_iolist.csv')
			with open(io_listfile, 'w') as f:
				for ioFileName in zip(inFileName_list,outFileName_list):
					f.write(','.join(ioFileName) + '\n')
			if self.removeFiles is not None:
				self.removeFiles = list(self.removeFiles).append(io_listfile)
			else:
				self.removeFiles = [io_listfile,]
			# --- make args ---
			cmdline = self.exec_name + self.necessaryOption
			# options line
			if option is not None and option != '':
				cmdline += ' ' + option
			cmdline += ' ' + self.inStyle.value + io_listfile
			# split cmdline
			args = shlex.split(cmdline)
			# --- execute ---
			try:
				p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			except OSError:
				print('Failed to execute command: ' + args[0])
			# read outputs
			(stdoutdata,stderrdata) = p.communicate(input=None)
			# treat errors
			if stderrdata and not self.quiteErr:
				print(stderrdata.decode('utf-8'))

		else:
			for inFileName,outFileName in zip(inFileName_list,outFileName_list):
				# --- make args ---
				cmdline = self.exec_name + self.necessaryOption
				# options line
				if option is not None and option != '':
					cmdline += ' ' + option
				# input style
				if self.inStyle is not None:
					cmdline += ' ' + self.inStyle + inFileName
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
				(stdoutdata,stderrdata) = p.communicate(input=inFile if self.inStyle is None else None)
				# treat stdout as an output if inStyle is None
				if self.outStyle is None:
					f = open(outFileName, 'w')
					f.write(stdoutdata.decode('utf-8'))
					f.close()
				# treat errors
				if stderrdata and not self.quiteErr:
					print(stderrdata.decode('utf-8'))

		for inFileName,outFileName in zip(inFileName_list,outFileName_list):
			# --- change format if necessary ---
			if self.outFormat == 'msf':
				tmp_msf = outFileName + '.msf'
				if os.path.exists(tmp_msf):
					os.remove(tmp_msf)
				try:
					os.rename(outFileName, tmp_msf)
				except OSError:
					print(outFileName, tmp_msf)
					sys.exit()
				path,name = os.path.split(outFileName)
				shortname,extension = os.path.splitext(name)
				msf2fasta(tmp_msf, os.path.join(path, shortname+'.fasta'))
				os.remove(tmp_msf)
