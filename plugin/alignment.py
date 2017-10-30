# -*- coding: utf-8 -*-

RESOURCE['aligners'].update({
	# inStyle,outStyle: None->stdin,stdout ''->without prefix option
	'mtrap_slow':{
		'exec_name': 'mtrap',
		'inStyle': '-i ',
		'outStyle': '-o ',
		'outFormat': 'fasta',
		'quiteErr': True
	},
	'mtrap':{
		'exec_name': 'mtrap',
		'inStyle': IO_LISTMODE('-filelist '),
		'outStyle': IO_LISTMODE(),
		'outFormat': 'fasta',
		'quiteErr': True
	},
	'clustalw':{
		'exec_name': 'clustalw',
		'inStyle': '-INFILE=',
		'outStyle': '-OUTFILE=',
		'outFormat': 'fasta',
		'necessaryOption': '-ALIGN -OUTORDER=INPUT -OUTPUT=FASTA -NEWTREE={0}'.format(os.path.join(tmpDir,'_tmp.dnd')),
		'quiteErr': False,
		'removeFiles': [os.path.join(tmpDir,'_tmp.dnd')]
	},
	'mafft':{
		'exec_name': 'mafft',
		'inStyle': '',
		'outStyle': None,
		'outFormat': 'fasta',
		'quiteErr': True
	},
	'muscle':{
		'exec_name': 'muscle',
		'inStyle': '-in ',
		'outStyle': '-out ',
		'outFormat': 'fasta',
		'quiteErr': True
	},
	'tcoffee':{
		'exec_name': 't_coffee',
		'inStyle': '-in=',
		'outStyle': '-outfile=',
		'outFormat': 'fasta',
		'necessaryOption': '-quiet -output=fasta',
		'quiteErr': True
	},
	'pmtrap':{
		'exec_name': 'pmtrap',
		'inStyle': '',
		'outStyle': None,
		'outFormat': 'fasta',
		'quiteErr': False
	},
	'lara':{
		'exec_name': '/home/keru/research/apps/lara-1.3.2a/lara',
		'inStyle': '-i ',
		'outStyle': '-w ',
		'outFormat': 'fasta',
		'necessaryOption': '-o /home/keru/research/apps/lara-1.3.2a/lara.params',
		'quiteErr': False
	},
})
