# -*- coding: utf-8 -*-

# utility function
def RANGES(d):
	''' return a list of ranges with length 1/d.

	>>> RANGES(5)
	[(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0)]
	>>> RANGES(1)
	[(0.0, 1.0)]
	>>> RANGES(0)
	[]
	'''
	return [(float(i)/d,float(i+1)/d) for i in range(d)]

class SILENT:
	def __init__(self, value):
		self.value = value
	def __repr__(self):
		return 'SILENT[{0}]'.format(self.value)

# some constants used for easy setting
FLAG = ('',)

class bcolors:
	HEADER = '\033[95m'
	BOLD = "\033[1m"
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

	def disable(self):
		self.HEADER = ''
		self.OKBLUE = ''
		self.OKGREEN = ''
		self.WARNING = ''
		self.FAIL = ''
		self.ENDC = ''

class IO_LISTMODE:
	def __init__(self, value=None):
		self.value = value
	def __repr__(self):
		return 'IO_LISTMODE[{0}]'.format(self.value)
