## import all functions from python ## 

## declare variables, so in our case, files based on matrix node size ## 

NODES = ["10","50","100", "200", "500", "1000", "10000"]


rule all:
	input


## this is a demo rule that will use the python script to make and write matrices ## 

# rule matrix_for_BF:
# 	input:
# 		just the node, one at a time
# 	output:
# 		csv="data/matrix/{node}_nodes.csv"
# 	run:
# 		## these are the two functions in temp.py that will run on the input data)
# 		matrix_maker(input.blah)
# 		matrix_writer(input.blah)

## this rule will then traverse the file system and input the matrices into BF to simulate seqs ##

# rule seq_gen:
# 	input:
# 		matrix=rules.matrix_for_BF.output.csv
# 	output:
# 		fasta="data/sim_seq/{node}_sim.fasta"
# 	shell:
# 		## is there a way to use an input flag for hyphy so we can throw in the matrix file? ##
# 		HYPHYMP SimulateSequence.bf -i input.matrix

# rule hyphy_analysis:
# 	input:
# 		seqs=rules.seq_gen.output.fasta
# 	output:
# 		json="data/hyphy/{node}.results.json"
# 	shell:
# 		path/to/hivtrace -i (input.seqs) -other flags
# 		## not only run this but then also immediately open in browser? ##

