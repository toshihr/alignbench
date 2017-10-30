# -*- coding: utf-8 -*-

RESOURCE['score_generaters'].update({
	'qscore_core':{
		'exec_name': './extra/bin/qscore',
		'option': '-quiet -ignoretestcase -cline',
		'refStyle': '-ref ',
		'targetStyle': '-test ',
		'outStyle': None,
		'refFormat': 'fasta',
		'testFormat': 'fasta',
		'scores': [('Q','Q-core'),('TC','TC-core'),('Cline','Cline-core')],
		'quiteErr': True
	},
	'qscore_core_Q':{
		'exec_name': './extra/bin/qscore',
		'option': '-quiet -ignoretestcase',
		'refStyle': '-ref ',
		'targetStyle': '-test ',
		'outStyle': None,
		'refFormat': 'fasta',
		'testFormat': 'fasta',
		'scores': [('Q','Q-core')],
		'quiteErr': True
	},
	'qscore_full':{
		'exec_name': './extra/bin/qscore',
		'option': '-quiet -ignoretestcase -ignorerefcase -cline',
		'refStyle': '-ref ',
		'targetStyle': '-test ',
		'outStyle': None,
		'refFormat': 'fasta',
		'testFormat': 'fasta',
		'scores': [('Q','Q-full'),('TC','TC-full'),('Cline','Cline-full')],
		'quiteErr': True
	},
	'qscore_full_Q':{
		'exec_name': './extra/bin/qscore',
		'option': '-quiet -ignoretestcase -ignorerefcase -cline',
		'refStyle': '-ref ',
		'targetStyle': '-test ',
		'outStyle': None,
		'refFormat': 'fasta',
		'testFormat': 'fasta',
		'scores': [('Q','Q-full')],
		'quiteErr': True
	},
})
