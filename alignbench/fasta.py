# -*- coding: utf-8 -*-

import subprocess # for execute an external process

def msf2fasta(inFile, outFile):
	args = ['/usr/bin/seqret', '-auto', inFile, 'fasta:'+outFile]
	try:
		p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except OSError:
		print('Failed to execute command: ' + args[0])
	(stdoutdata,stderrdata) = p.communicate()

class Fasta:
	def __init__(self, inFileIO, aligned=False, toUpper=False):
		self.inFileIO = inFileIO
		self.blocks = []
		self.num = 0
		self.id_global = 0.0
		self.id_local = 0.0
		self.read(toUpper)
		if aligned:
			self.calc_id()

	def read(self, toUpper):
		self.blocks = []
		self.num = 0
		seq_buffer = []
		name = ''
		for line in self.inFileIO:
			# skip empty line
			if line is None:
				continue
			if len(line) == 0:
				continue
			# read
			if line[0] == '>':
				if name != '':
					self.blocks.append( (name, ''.join(seq_buffer) ) )
				# start new fasta block
				name = line[1:].rstrip()
				self.num += 1
				seq_buffer = []
			else:
				if not toUpper:
					seq_buffer.append(line.rstrip())
				else:
					seq_buffer.append(line.rstrip().upper())

		if name != '':
			self.blocks.append( (name, ''.join(seq_buffer)) )

	def calc_id(self):
		''' calculate sequence identity
		2012/7/18 昔使っていたeerdistはeertools::getMultiFastaが改行コードを文字と認識してしまうバグをひきずっていたため値が違っていた

		>>> import io
		>>> import fasta
		>>> i = ">seq1\\n" + "AABBCC-DEE\\n" \
		      + ">seq2\\n" + "ABBBCCCD-E\\n"
		>>> f = fasta.Fasta(io.StringIO(i), aligned=True,toUpper=True)
		>>> print('{0},{1},{2},{3}'.format(f.id_local,f.match,f.length,f.num_gap))
		0.875,7,10,2

		>>> import io
		>>> import fasta
		>>> i2 = '>1dk5A\\n' \
		+ 'hhhmasltvpahvpSAAEDCEQLRSAFKGWGTNEKLIISILAHRTAAQRKLIRQTYAETF' \
		+ 'GEDLLKELDRELTHDFEKLVLVWTLDPSERDAHLAKEATKRWTKSNFVLVELACTRSPKE' \
		+ 'LVLAREAYHARYKKSLEEDVAYHTTGDHRKLLVPLVSSYRYGGEEVDLRLAKAESKILHE' \
		+ 'KISdkaysd---DEVIRILATRSKAQLNATLNHYKDEHGEDILKQLED--GDEFVALLRA' \
		+ 'TIKGLVYPEHYFVEVLRDAINRRGTEEDHLTRVIATRAEVDLKIIADEYQKRDSIPLGRA' \
		+ 'IAKDTRGDYESMLLALLGQe--\\n' \
		+ '>1aow\\n' \
		+ '---------asgf-NAAEDAQTLRKAMKGLGTDEDAIINVLAYRSTAQRQEIRTAYKTTI' \
		+ 'GRDLMDDLKSELSGNFEQVILGMMTPTVLYDVQEVRKAMKGAGTDEGCLIEILASRTPEE' \
		+ 'IRRINQTYQLQYGRSLEDDIRSDTSFMFQRVLVSLSAGGRDESNYLDDALMRQDAQDLYE' \
		+ 'AGE-kkwg-tdeVKFLTVLCSRNRNHLLHVFDEYKRIAQKDIEQSIKSetSGSFEDALLA' \
		+ 'IVKCMRNKSAYFAERLYKSMKGLGTDDDTLIRVMVSRAEIDMLDIRANFKRLYGKSLYSF' \
		+ 'IKGDTSGDYRKVLLILCGG-dd\\n'
		>>> f2 = fasta.Fasta(io.StringIO(i2), aligned=True,toUpper=True)
		>>> print('{0},{1},{2},{3}'.format(f2.id_local,f2.match,f2.length,f2.num_gap))
		0.31125827814569534,94,322,20
		>>> f2 = fasta.Fasta(io.StringIO(i2), aligned=True,toUpper=False)
		>>> print('{0},{1},{2},{3}'.format(f2.id_local,f2.match,f2.length,f2.num_gap))
		0.31125827814569534,94,322,20
		'''

		match = 0
		num_gap = 0
		length = len(self.blocks[0][1])
		for index in range(0,length):
			site_gapped = False
			site_match = True
			symbol = ''
			for name,seq in self.blocks:
				c = seq[index]
				if c == '-':
					num_gap += 1
					site_gapped = True
					break
				if symbol == '':
					symbol = c
				elif symbol != c:
					site_match = False
					break
				else:
					pass
			if (not site_gapped) and site_match:
				match += 1
		self.id_global = float(match) / length
		self.id_local = float(match) / (length - num_gap)
		self.match = match
		self.length = length
		self.num_gap = num_gap

if __name__ == '__main__':
	import doctest
	doctest.testmod(verbose=False)

