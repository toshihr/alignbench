# -*- coding: utf-8 -*-

### BENCHMARK DETAILS ###

# ============================== ALIGNER'S OPTION =============================
# HOW TO DEFINE:
#   OPTION = { 'aligner1': { option1:value2, option2:value2, ... }, 'aligner2': ... }
# NOTE:
#   - these options are used in the BENCH
#   - FLAG: the value FLAG means just the flag
#   - SILENT('option'): do not show the option details
# =============================================================================
OPTION = {
	# [PMTRAP]
	'pmtrap':{
		'-mtrap': 0.3,
		'-mtrap_eps': 0.775,
		'-mtrap_gamma': 0.0,
	},

	# [OLD MTRAP]
	'oldmtrap_default':{
		'-itr': [0,10],
		'-msaprobs': 0,
		'-e': 0.775,
	},

	# [MTRAP]
	'mtrap':{
	#'-dna': FLAG,
	#	'-averageExtendedAA': FLAG,
	#	'-m': ['CGONNET250','/home/keru/project/mtrap/make_tq/TQ/SABmark1.63_sup_weighted_20120803.mat'],
	#	'-m': ['CGONNET250'],
	#	'-m': ['VTML200I','/home/keru/project/mtrap/make_tq/TQ/SABmark1.63_sup_weighted_20120803.mat'],
		'-m': ['VTML200I'],
	#	'-m': ['/home/keru/project/mtrap/resource/homstrad/homstrad200.mat'],
	#	'-m': ['VTML200I','/home/keru/project/mtrap/resource/homstrad/homstrad150.mat'
	#			,'/home/keru/project/mtrap/resource/homstrad/homstrad200.mat'
	#			,'/home/keru/project/mtrap/resource/homstrad/homstrad250.mat'],
		'-pm': ['VTML200I'],
	#	'-noestimation': FLAG,
	#	'-itr': [0,5,10],
	#	'-tm': ['SABmark1.63_sup_weighted.btq','/home/keru/research/make_tq/TQ/SABmark1.63_sup_weighted_20120731.btq'],
	#	'-tm': ['SABmark1.63_sup_weighted.btq','/home/keru/project/mtrap/make_tq/TQ/SABmark1.63_sup_weighted_20120803.btq'],
		'-tm': ['SABmark1.63_sup_weighted.btq'],
	#	'-pf': [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
		'-pf': 0.0,
		'-beta': 0.2,
		'-beta2': 1.5, # best with VTML200I + SABmark1.63_sup_weighted.btq
	#	'-beta2': [0.0,0.1,0.2,0.3,0.4,0.5],
		'-go': -11,
		'-ge': -0.3,
		'-pgo': -22,
		'-pge': -1,
	#	'-e': [0.1,0.5,0.9],
	#	'-e': 0.0,
	#	'-e': [0.0,0.775],
	#	'-e': [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
		'-e': 0.775,
	},

	# [MTRAP RNA]
	'option_mtrap_rna':{
	#	'-m': ['CID','/home/keru/project/mtrap/make_tq/TQ/bralibase2_U5_weighted_20121010.mat'],
	#	'-m': ['/home/keru/project/mtrap/make_tq/TQ/bralibase2_U5_p_training_weighted_20121010.mat',],
	#	'-m': ['/home/keru/project/mtrap/make_tq/TQ/bralibase2_tRNA_p_training_weighted_20121010.mat',],
		'-m': ['/home/keru/project/mtrap/make_tq/TQ/bralibase2_rRNA_p_training_weighted_20121010.mat',],
	#	'-m': ['/home/keru/project/mtrap/make_tq/TQ/bralibase2_SRP_p_training_weighted_20121010.mat',],
	#	'-m': ['/home/keru/project/mtrap/make_tq/TQ/bralibase2_rRNA_p_test_weighted_20121010.mat',],
	#	'-m': ['/home/keru/project/mtrap/make_tq/TQ/bralibase2_U5_p_test_weighted_20121010.mat',],
	#	'-itr ': [0,10],
	#	'-tm ': ['/home/keru/project/mtrap/make_tq/TQ/bralibase2_U5_p_training_weighted_20121010.btq'],
	#	'-tm ': ['/home/keru/project/mtrap/make_tq/TQ/bralibase2_tRNA_p_training_weighted_20121010.btq'],
		'-tm ': ['/home/keru/project/mtrap/make_tq/TQ/bralibase2_rRNA_p_training_weighted_20121010.btq'],
	#	'-tm ': ['/home/keru/project/mtrap/make_tq/TQ/bralibase2_SRP_p_training_weighted_20121010.btq'],
	#	'-tm ': ['/home/keru/project/mtrap/make_tq/TQ/bralibase2_rRNA_p_test_weighted_20121010.btq'],
	#	'-tm ': ['/home/keru/project/mtrap/make_tq/TQ/bralibase2_U5_p_test_weighted_20121010.btq'],
		'-pf ': 0.1, # for rRNA database
	#	'-pf': [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
		'-beta2 ': 0.0,
	#	'-go': -9,
		'-go': -11, # for rRNA database
	#	'-go': [-9,-11,-12,-13,-15],
		'-ge': -0.5,
	#	'-e ': [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
		'-e ': 0.4, # for rRNA database
	},

	# [CLUSTALW]
	'clustalw_pam':{
		'-PWMATRIX=': 'PAM',
		'-MATRIX=': 'PAM'
	},
	'clustalw_blosum':{
		'-PWMATRIX=': 'BLOSUM',
		'-MATRIX=': 'BLOSUM'
	},
	'clustalw_gonnet':{
		'-PWMATRIX=': 'GONNET',
		'-MATRIX=': 'GONNET'
	},

	# [CLUSTALW-RNA]
	'clustalw_rna_default':{
		SILENT('-TYPE='): 'DNA',
	},


	# [MAFFT]
	'mafft_linsi':{
		'--maxiterate': 1000,
		'--localpair': FLAG
	},

	# DEFAULT
	'default': {}
}


BENCH = {
# ============================== [1] ALIGNER ==================================
# HOW TO DEFINE:
#   'alignerset': [ (aligner1,option1), (aligner2,option2), ... ]
# NOTE:
#   - aligners are defined in the file 'environment.py'
#   - options are defined above
#   - duplicate is automatically omitted
# =============================================================================
	'alignerset': [
#		('mtrap', option_mtrap_rna),
#		('mtrap', option_oldmtrap_default),
		('mtrap', OPTION['mtrap']),
#		('mtrap', OPTION['default']),
#		('pmtrap', option_pmtrap),
#		('clustalw', OPTION['default']),
#		('clustalw', option_clustalw_default),
#		('clustalw', option_clustalw_pam),
#		('clustalw', option_clustalw_blosum),
#		('clustalw', option_clustalw_gonnet),
#		('clustalw', option_clustalw_rna_default),
#		('mafft', OPTION_DEFAULT),
#		('mafft', option_mafft_linsi),
#		('muscle', OPTION_DEFAULT),
#		('tcoffee', OPTION_DEFAULT),
#		('lara', OPTION_DEFAULT),
	],
# ======================= [2] STATISTICAL ANALYSIS ============================
# -------------- TARGET ALIGNERS FOR THE STATISTICAL TEST ---------------------
# HOW TO DEFINE:
#   same as above
# -----------------------------------------------------------------------------
	'alignerset_compared': [
		('clustalw', OPTION['default']),
#		('clustalw', option_clustalw_rna_default),
	],
# ---------------------------- BENCHMARK SCORES -------------------------------
# HOW TO DEFINE:
#   'scoremakers': [ score1,score2, ... ]
# NOTE:
#   - scores are defined in the file 'environment.py'
# -----------------------------------------------------------------------------
	'scoremakers': [
#		'qscore_core',
#		'qscore_full',
#		'modeler_core',
#		'modeler_full',
		'qscore_core_Q',
#		'qscore_full_Q',
	],
# -----------------------------BENCHMARK RANGES -------------------------------
# HOW TO DEFINE:
#   'id_range_list': [ (left1,right1),(left2,right2),, ... ]
#   'id_global': True or False
# NOTE:
#   - the range (left,right) means that [left,right) in a real space, for right < 1
#   - the range (left,1) means that [left,right] in a real space
#   - you can use the function RANGES(n) = [ (0,1/n),(1/n,2/n),...,(n-1/n,1) ]
#   - 'id_global': True means that to use global percent identity
#                     False means that to use local percent identity
# -----------------------------------------------------------------------------
	'id_range_list': [(0.0,0.15),(0.15,0.30),(0.30,0.45),(0.45,0.60)]
		+ RANGES(5) + RANGES(4) + RANGES(2) + RANGES(1),
	'id_global': False,
# ============================== [3] DATABASES ================================
# HOW TO DEFINE:
#   'databases': [ database1,database2, ... ]
# NOTE:
#   - databases are defined in the file 'environment.py'
# =============================================================================
	'databases': [
#		'minipairwise',
#		'prefab4',
#		'pali2.8b',
		'pali2.8b_class_a',
#		'pali2.8b_class_b',
#		'pali2.8b_class_c',
#		'pali2.8b_class_d',
#		'pali2.8b_class_e',
#		'pali2.8b_class_g',
#		'homstrad',
#		'balibase3rv11',
#		'balibase3rv11s',
#		'balibase3rv12',
#		'balibase3rv12s',
#		'balibase3rv20',
#		'balibase3rv20s',
#		'balibase3rv30',
#		'balibase3rv30s',
#		'balibase3rv40',
#		'balibase3rv50',
#		'balibase3rv50s',
#		'bralibase2_SRP',
#		'bralibase2_SRP_p_pairwise',
#		'bralibase2_U5',
#		'bralibase2_U5_p_pairwise',
#		'bralibase2_U5_p_test_pairwise',
#		'bralibase2_U5_p_training_pairwise',
#		'bralibase2_g2intron',
#		'bralibase2_g2intron_p_pairwise',
#		'bralibase2_g2intron_p_test_pairwise',
#		'bralibase2_g2intron_p_training_pairwise',
#		'bralibase2_rRNA',
#		'bralibase2_rRNA_p_pairwise',
#		'bralibase2_rRNA_p_test_pairwise',
#		'bralibase2_rRNA_p_training_pairwise',
#		'bralibase2_tRNA',
#		'bralibase2_tRNA_p_pairwise',
#		'bralibase2_tRNA_p_test_pairwise',
#		'bralibase2_tRNA_p_training_pairwise',
#		'homstrad_pairwise',
	],
}
