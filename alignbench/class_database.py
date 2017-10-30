# -*- coding: utf-8 -*-
import tarfile
import os
import glob
import shutil
import re
from alignbench.io import makedirs
from alignbench.fasta import Fasta

class Database:
	''' database class '''

	def __init__(self, name, arcName, tmpDir, id_range=None, toUpper=False, num_max=10000, filter_regex=None):
		self.name = name
		self.arcName = arcName
		self.num_max = num_max
		(self.id_min,self.id_max) = (0.0,1.0) if id_range is None else id_range
		self.toUpper = toUpper
		self.filter_regex = filter_regex

		# generate the database name
		arcExts = ('.zip','.tar.gz','.tgz','.tar.bz2','.tbz')
		for e in arcExts:
			if self.arcName.endswith(e):
				self.arcBaseName = os.path.basename(self.arcName)[:-len(e)]
				
				break
		else:
			raise NameError('archive {0} may have some trouble.'.format(self.arcName))

		self.tmpDir = os.path.join(tmpDir,name)
		#print('The database object {0} is created.'.format(self.name))

		# init instance variable
		self.unpacked = False
		self.listGenerated = False
		self.inFile_refFile_list = []
		self.num = 0


	def unpack(self):
		print('[ROOT PROCESS] unpack ' + self.arcName + ' to ' + self.tmpDir)
		# make a tmp directory
		makedirs(self.tmpDir)

		if not os.path.exists(self.arcName):
			print('[ROOT PROCESS] not found!')

		try:
			arc_file = tarfile.open(self.arcName)
			arc_file.extractall(path=self.tmpDir)
			arc_file.close()
			self.unpacked = True
		except:
			pass


	def refresh_list(self, id_global=False):
		''' make inputfile list
		make a tuple (inFile, refFile, identity)
		inFile: [tmpDir/database.name]/[database.arcBaseName]/in/*.fasta
		refFile: [tmpDir/database.name]/[database.arcBaseName]/ref/*.ref_fasta
		identity: sequence percent identity of refFile

		'''
		if not self.unpacked:
			raise BaseException('archive {0} is not unpacked.'.format(self.arcName))
		if not self.listGenerated:
			searchFiles = os.path.abspath(os.path.join(self.tmpDir, 'in', '*.fasta'))
			for inFile in glob.iglob(searchFiles):
				shortname,extension = os.path.splitext(os.path.basename(inFile))

				# filtering
				if self.filter_regex:
					m = re.search(self.filter_regex, shortname)
					if not m: continue

				# TODO 2012/12/23 ***.ref_fasta
				# が存在するかチェックし、存在しなければmultiple-allpairモードとしてサブフォルダ内のすべての.pair_ref_fastaにたいして%IDを計算する
				# 返す際のrefFileはpair_ref_fastaの格納されているフォルダを返すことにする
				#返されたRefFileのうしろが.ref_fastaならmultiple-multipleモード、それ以外はmultiple-pairwiseモードととらえることができる
				refFile = os.path.abspath(os.path.join(self.tmpDir, 'ref', shortname + '.ref_fasta'))
				with open(refFile) as f:
					fa = Fasta(f, aligned=True, toUpper=self.toUpper)
					num = fa.num
					if id_global:
						identity = fa.id_global
					else:
						identity = fa.id_local

				# filter for the number of sequences
				if num > self.num_max:
					continue
				# id filter
				if identity != 1.0 and self.id_min <= identity < self.id_max:
					self.inFile_refFile_list.append( (inFile, refFile, identity) )
				elif identity == 1.0 and self.id_min <= identity <= self.id_max:
					self.inFile_refFile_list.append( (inFile, refFile, identity) )

			self.num = len(self.inFile_refFile_list)

			self.listGenerated = True

	def clean(self):
		if os.path.exists(self.tmpDir):
			shutil.rmtree(self.tmpDir, ignore_errors=True)

	def gen_list(self):
		''' generator. '''
		if not self.listGenerated: self.refresh_list();
		for inFile,refFile,identity in self.inFile_refFile_list:
			yield (inFile,refFile)

	def gen_identity_list(self):
		''' generate an identity list'''
		if not self.listGenerated: self.refresh_list();
		for inFile,refFile,identity in self.inFile_refFile_list:
			yield identity
