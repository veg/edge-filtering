## import all functions from python ## 
from python.temp import *

NODES = ["10", "50", "100", "200", "500", "1000", "10000"]
#nodes=NODES
#nodes='10'

#### debugger:     #run: import pdb; pdb.set_trace() ####

## this rule colelcts the target file, this cannot contain wildcards ##
## and this 'all' rule must be at the top ## 

rule all:
    #input: expand("data/matrix/{NODES}_nodes.ibf", NODES=NODES)
    input: expand("data/sim_seq/{node}_sim.fasta", node=NODES)


## this is a demo rule that will use the python script to make and write matrices ## 
rule matrix_for_BF:
    params: 
        node_cnts = expand("{node}", node=NODES)
    output: 
        expand("data/matrix/{NODES}_nodes.ibf", NODES=NODES)
    run: 
        for n in params.node_cnts:
            edge_creator(0.005,0, n, "hyphy")

## this rule will take the matrices and input them into the sim_seq.bf to make fasta files ##
rule seq_gen:
    input:
         "data/matrix/{NODES}_nodes.ibf"
    output:
        "data/sim_seq/{NODES}_sim.fasta"
    shell:
        "HYPHYMP simulate/SimulateSequence.bf {input} > {output}"

## this rule will take the generated fasta files and input them into HIVtrace 
# rule hiv_trace:
#     input:
#         "data/sim_seq/{NODES}_sim.fasta"
#     output:
#         json="data/hyphy/{node}.results.json"
#     shell:
#         path/to/hivtrace -i (input.seqs) -other flags
#         ## not only run this but then also immediately open in browser? ##

