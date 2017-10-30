# -*- coding: utf-8 -*-

RESOURCE['score_generaters'].update({
	'modeler_core':{
		'exec_name': './extra/bin/qscore',
		'option': '-quiet -ignoretestcase -modeler',
		'refStyle': '-ref ',
		'targetStyle': '-test ',
		'outStyle': None,
		'refFormat': 'fasta',
		'testFormat': 'fasta',
		'scores': [('Modeler','Modeler-core')],
		'quiteErr': True
	},
	'modeler_full':{
		'exec_name': './extra/bin/qscore',
		'option': '-quiet -ignoretestcase -ignorerefcase -modeler',
		'refStyle': '-ref ',
		'targetStyle': '-test ',
		'outStyle': None,
		'refFormat': 'fasta',
		'testFormat': 'fasta',
		'scores': [('Modeler','Modeler-full')],
		'quiteErr': True
	},
})
