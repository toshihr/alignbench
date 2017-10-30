# -*- coding: utf-8 -*-
import numpy as np

STAT_MODE = ''

def init_mode(a_mode):
	global STAT_MODE
	STAT_MODE = a_mode

def import_module():
	global robjects
	global wilcoxon
		
	if STAT_MODE == 'coin':
		import rpy2.robjects as robjects
		R = robjects.r
		R('suppressMessages(library(coin))')
	elif STAT_MODE == 'R':
		import rpy2.robjects as robjects
	elif STAT_MODE == 'python':
		from scipy.stats import wilcoxon


def wilcox_paired(x,y):
	''' wilcoxon signed-rank test
	wilcoxon rank sum test (Mann Whitney test)ではないことに注意
	TODO: 標本数n<10の場合に正しい結果がでない。exact p-valueを求めたいがあとまわし。
	Rpyを用いて内部でRを呼ぶのが楽かも。一度Rオブジェクトを生成してしまえば速度もそんなに犠牲にならないと思われる。
	青木先生のところと同じアルゴリズム

	Rと同じで、小数の場合おかしな値を返す場合がある
	'''

	if STAT_MODE == '':
		print('should be initialized before using wilcox_paired().')
		return (np.nan,np.nan)

	import_module()

	# 欠損値対策
	data = np.array([x,y])
	data = data[:,~np.isnan(data).any(0)]

	if sum(np.abs(data[0] - data[1])) < 1.0e-10:
		return (np.nan,np.nan)

	for i in range(10):
		if np.all(np.abs(data*(10**i) - np.floor(data*(10**i))) < 1.0e-10):
			if STAT_MODE == 'coin':
				rx = robjects.FloatVector(data[0]*(10**i))
				ry = robjects.FloatVector(data[1]*(10**i))
				robjects.globalenv['x'] = rx
				robjects.globalenv['y'] = ry
				R = robjects.r
				R('w <- wilcoxsign_test(x ~ y, zero.method="Pratt")')
				pvalue = R('pvalue(w)')[0]
				W = R('statistic(w)[1][["neg"]]')[0]
				return (W,pvalue)
			elif STAT_MODE == 'R':
				print('NOT IMPLEMENTED YET!!')
				return (np.nan,np.nan)
			elif STAT_MODE == 'python':
				return wilcoxon(data[0] - data[1])

	# give up!
	return (np.nan,np.nan)

