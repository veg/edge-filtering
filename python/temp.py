print('\n 		generating the matrix... \n' )
import numpy as np
import pandas as pd



def matrix_maker(internal, tip, matrix_node_counts):
	dfs = []
	for i in matrix_node_counts[0:3]:
		nodes = list(range(i))
		## payload for column 1 (node ID) ##
		j = [i +1 for i in nodes]
		print('Total number of  nodes in the network: ' + str(j[-1]) + '\n')


		## payload for column 2 (source nodes) ##
		nodes[0] = -1

		## payload for columns 3 ( internal length) and 4 (tip length) ## 
		temp_internal = [0.005 for i in nodes]
		temp_tip = [0 for i in nodes]
		#print(len(j), len(nodes), len(temp_internal), len(temp_tip))
		d = {'Node ID': j, 'Source Node': nodes, 'Internal Length': temp_internal, 'Tip Length':temp_tip}
		df = pd.DataFrame(d)
		dfs.append(df)
	return dfs 

def matrix_writer(matrices):
	for i in matrices:
		number = str(len(i))
		filename =  ('../data/%s_nodes.csv' % number)
		print(filename)
		i.to_csv(filename, sep=',', index=False)



internal_length = 0.005
tip_length = 0
matrix_node_counts = [10, 50, 100, 200, 500, 1000, 10000]

results = matrix_maker(internal_length,tip_length,matrix_node_counts)

matrix_writer(results)
