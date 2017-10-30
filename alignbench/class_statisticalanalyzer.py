# -*- coding: utf-8 -*-
import os
import re
import csv
import shutil
import numpy as np
import warnings
import matplotlib.pyplot as plt
from alignbench.io import makedirs,pack
from alignbench.class_aligner import Aligner
from alignbench.stat import wilcox_paired

DELIM_OUTPUT_CSV = '\t'

class StatisticalAnalyzer:
	def __init__(self, allbenchmarks, a_database, outDir, outFile, tmpDir):
		self.allbenchmarks = allbenchmarks
		self.a_database = a_database
		self.outDir = outDir
		self.outFile = os.path.join(self.outDir, self.a_database.name, outFile)
		self.tmpDir = tmpDir

	def sort_outFile(self):
		header = []
		result_list = []
		key_values = []
		with open(self.outFile) as f:
			reader = csv.reader(f, delimiter=DELIM_OUTPUT_CSV)
			header = next(reader)
			for row in reader:
				result_list.append(row)
				key_values.append(row[4] + row[2] + row[3]) # sort priority: score,aligner,option

		# human (natural) sort
		convert = lambda text: int(text) if text.isdigit() else text
		alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
		order = list(k for k,v in sorted(enumerate(key_values),key=lambda x:alphanum_key(x[1])))

		with open(self.outFile, 'w') as f:
			writer = csv.writer(f, delimiter=DELIM_OUTPUT_CSV)
			writer.writerow(header)
			for index in order:
				writer.writerow(result_list[index])

	def run(self, id_min_max_list=[(0.0,1.0),], compared_with=None):
		# --- make a tmp dir of graphs ---
		graphTmpDir = os.path.join(self.tmpDir, 'benchmark', self.a_database.name, 'graph')
		makedirs(graphTmpDir)

		with open(self.outFile, 'w') as f:
			# output the header
			f.write(DELIM_OUTPUT_CSV.join(('%ID','num','aligner','option','score','mean','mean_compared','median','median_compared','paired wilcoxon p-value','comparing aligner','comparing aligner\'s option')) + '\n')
			# make an identity and a seq name list
			identity_list = [x for x in self.a_database.gen_identity_list()]
			refname_list = [os.path.splitext(os.path.basename(ref_name))[0] for in_name,ref_name in self.a_database.gen_list()]
			# make a tmp dir of scores
			scoreTmpDir = os.path.join(self.tmpDir, 'benchmark', self.a_database.name, 'score')
			makedirs(scoreTmpDir)
			# big loop with the identity
			for (id_min,id_max) in id_min_max_list:
				# --- graph treatment ---
				graph_list = {}

				# compared with an aligner in compared_with
				for aligner_x,a_full_option_list_x in compared_with.items() if compared_with is not None else [(None,None),]:
					scorename_masked_values_x = {}
					if aligner_x is not None:
						for a_option_set_x in a_full_option_list_x:
							aligner_name_x = aligner_x.name
							a_option_str_x = Aligner.make_a_string_from_optionset(a_option_set_x, cmdline=False, full=False)

							# search and set x
							for aligner_name,option_allscores in self.allbenchmarks:
								if aligner_name == aligner_name_x:
									for option,allscores in option_allscores.items():
										if option == a_option_str_x:
											for score_name,array_values in allscores:
												# filtering with identity_list
												v = [ value for identity, value in zip(identity_list, array_values)
															if (identity != 1.0 and id_min <= identity < id_max)
															or (identity == 1.0 and id_min <= identity <= id_max) ]
												scorename_masked_values_x[score_name] = np.ma.masked_array(v , np.isnan(v))
											break
									break
						assert scorename_masked_values_x != {}
					else:
						aligner_name_x = ''
						a_option_str_x = ''

					# parse benchmark result
					for aligner_name,option_allscores in self.allbenchmarks:
						for option,allscores in option_allscores.items():
							for score_name,array_values in allscores:
								# filtering with identity_list
								v = [ value for identity, value in zip(identity_list, array_values)
											if (identity != 1.0 and id_min <= identity < id_max)
											or (identity == 1.0 and id_min <= identity <= id_max) ]
								refname_filtered = [ ref_name for identity, ref_name in zip(identity_list,refname_list)
											if (identity != 1.0 and id_min <= identity < id_max)
											or (identity == 1.0 and id_min <= identity <= id_max) ]
								masked_values = np.ma.masked_array(v , np.isnan(v))

								# statistics for a result
								num = np.ma.count(masked_values)
								(mean,median) = (np.mean(masked_values),np.median(masked_values)) if num > 0 else ('nodata','nodata')

								# add the name and data to a graph list
								if mean != 'nodata':
									graph_list[(aligner_name,option,score_name)] = masked_values

								# statistics for a pair of x and y
								if aligner_x is None:
									z_statistic, p_value = '', ''
									mean_x,median_x = '',''
								elif not (aligner_name == aligner_name_x and option == a_option_str_x):
									# statistics for x
									num_x = np.ma.count(scorename_masked_values_x[score_name])
									(mean_x,median_x) = (np.mean(scorename_masked_values_x[score_name]),np.median(scorename_masked_values_x[score_name])) if num_x > 0 else ('nodata','nodata')
									# statistical test
									with warnings.catch_warnings(record=True) as w:
										# make a not None list
										mask = masked_values.mask + scorename_masked_values_x[score_name].mask
										x = np.ma.masked_array(masked_values.data, mask).compressed()
										y = np.ma.masked_array(scorename_masked_values_x[score_name].data, mask).compressed()
										ref = np.array(refname_filtered)[~mask]
										assert len(x) == len(y)
										if len(x) > 20:
											res = wilcox_paired(x, y)
											z_statistic, p_value = '{0:.3f}'.format(res[0]),'{0:.3f}'.format(res[1])
										elif len(x) > 0:
											z_statistic, p_value = 'n<20', 'n<20'
										else:
											z_statistic, p_value = 'n=0', 'n=0'

										if len(w) > 0:
											warn_message = '/'.join([str(ww.message) for ww in w])
											z_statistic, p_value = 'error', warn_message

										# generate score files for the validation
										score_fullname = os.path.join(scoreTmpDir, '{0}__{1}_{2}.csv'.format(score_name,int(id_min*100),int(id_max*100)))
										with open(score_fullname, 'w') as fscore:
											fscore.write('ref_name,{0}:{1},{2}:{3}\n'.format(aligner_name,option,aligner_name_x,a_option_str_x))
											for t in zip(ref,x,y):
												fscore.write(','.join(map(str, t)) + '\n')
								else:
									z_statistic, p_value = 'samedata', 'samedata'
									mean_x,median_x = 'samedata','samedata'

								# output
								line = []
								line.append('{0}_{1}'.format(int(id_min*100),int(id_max*100)))
								line.append(str(num))
								line.extend((aligner_name, option))
								line.append(score_name)
								line.extend((str(mean), str(mean_x)))
								line.extend((str(median), str(median_x)))
								line.append(str(p_value))
								line.extend((aligner_name_x, a_option_str_x))
								f.write(DELIM_OUTPUT_CSV.join(line) + '\n')
				# --- draw a graph w.r.t each %ID range
				
				for score_name,array_values in allscores:
					a_graph_data = [ a_values for (a_aligner_name,a_option,a_score_name),a_values in sorted(graph_list.items()) if a_score_name == score_name]
					if a_graph_data == []: continue
					a_graph_name = [ '{0}\n{1}'.format(a_aligner_name, a_option[:40] + '...' if len(a_option) >= 40 else a_option)
						for (a_aligner_name,a_option,a_score_name),a_values in sorted(graph_list.items()) if a_score_name == score_name]
					
					fullGraphName = os.path.join(graphTmpDir,score_name,'boxplot_{0}_{1}.png'.format(int(id_min*100),int(id_max*100)))
					makedirs(os.path.dirname(fullGraphName))

					fig = plt.figure()
					ax = fig.add_subplot(1,2,2) # 234 means 2x3 grid 4th subplot
					ax.grid()
					ax.set_xlim(0.0,1.0)
					ax.set_yticklabels(a_graph_name)
					ax.set_xlabel(score_name)
					bp = ax.boxplot(a_graph_data, vert=False)
					# get x of medians
					line2D_list = bp['boxes']
					plt.savefig(fullGraphName)


		# sorting the result
		self.sort_outFile()

		# pack the graphs
		storedArcName = pack(graphTmpDir, erase=True)
		finalGraphDir = os.path.join(self.outDir, self.a_database.name)
		if os.path.isfile(os.path.join(finalGraphDir, os.path.basename(storedArcName))):
			os.remove(os.path.join(finalGraphDir, os.path.basename(storedArcName)))
		shutil.move(storedArcName, finalGraphDir)

		# pack the scores
		storedArcName = pack(scoreTmpDir, erase=True)
		finalScoreDir = os.path.join(self.outDir, self.a_database.name)
		if os.path.isfile(os.path.join(finalScoreDir, os.path.basename(storedArcName))):
			os.remove(os.path.join(finalScoreDir, os.path.basename(storedArcName)))
		shutil.move(storedArcName, finalScoreDir)
