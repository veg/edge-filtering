## import all functions from python ## 
from python.temp import *
#import python.temp

## declare variables, so in our case, files based on matrix node size ## 

NODES = ["10", "50", "100", "200", "500", "1000", "10000"]
#nodes=NODES
#nodes='10'

## this rule colelcts the target file, this cannot contain wildcards ##
## and this 'all' rule must be at the top ## 
rule all:
	input: expand("data/matrix/{NODES}_nodes.ibf", NODES=NODES)


## this is a demo rule that will use the python script to make and write matrices ## 
rule matrix_for_BF:
    #input: script="python/temp.py"
	output: expand("data/matrix/{NODES}_nodes.ibf", NODES=NODES)
	run: edge_creator(0.005,0,{NODES}, "hyphy")
	# import pdb; pdb.set_trace(),
	#"python {input.script} -c {NODES} -f 'hyphy'"
 #edge_creator(0.005,0,{nodes}, "hyphy")


# ## this rule will then traverse the file system and input the matrices into BF to simulate seqs ##
# rule seq_gen:
# 	input:
# 		matrix=rules.matrix_for_BF.output.hyphy
# 	output:
# 		fasta="data/sim_seq/{node}_sim.fasta"
# 	shell:
# 		## is there a way to use an input flag for hyphy so we can throw in the matrix file? ##
# 		HYPHYMP SimulateSequence.bf input.matrix

# rule hyphy_analysis:
# 	input:
# 		seqs=rules.seq_gen.output.fasta
# 	output:
# 		json="data/hyphy/{node}.results.json"
# 	shell:
# 		path/to/hivtrace -i (input.seqs) -other flags
# 		## not only run this but then also immediately open in browser? ##

