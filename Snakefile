## import all functions from python ## 
from python.temp import *
from python.edge_report import edge_report
import itertools


#NODES = list(itertools.repeat("10", 10))
NODES = ["10", "50", "100", "200", "500", "1000", "10000"]
#nodes=NODES
#nodes='10'


INTERNAL_LENGTH = 0.005
TIP_LENGTH = 0
FORMAT = "hyphy"

#### debugger:     #run: import pdb; pdb.set_trace() ####

## this rule collects the target file, this cannot contain wildcards ##
## and this 'all' rule must be at the top ## 

def expand_all(*args, **wildcards):
    return expand("data/hivtrace/{node}_nodes.results.json", node=wildcards["node"]) + expand("data/hivtrace/{node}_nodes.nofilter.results.json",node=wildcards["node"])

rule all: 
    #input: expand_all("", node=NODES)
    input:  expand("data/hivtrace/{node}_edge_report.json", node=NODES)

    ## use this if you want to just check rule 'matrix_for_BF' ##
    #input: expand("./data/matrix/{NODES}_nodes.ibf", NODES=NODES)
    
    ## use this if you want to just check rule 'seq_gen' ##
    #input: expand("./data/sim_seq/{node}_sim.fasta", node=NODES)

    ## use this if you want to just check rule 'hiv_trace' ##
    #input: expand("data/hivtrace/{node}_nodes.results.json", node=NODES)


## this rule that will use the python script to make and write matrices to .ibf files ## 
rule matrix_for_BF:
    params: 
        node_cnts = expand("{node}", node=NODES)
    output: 
        expand("data/matrix/{nodes}_nodes.ibf", nodes=NODES),
    run: 
        for n in params.node_cnts:
            edge_creator(INTERNAL_LENGTH,TIP_LENGTH, n, FORMAT)

## this rule will take the matrices and input them into the sim_seq.bf to make fasta files ##
rule seq_gen:
    input:
        "data/matrix/{NODES}_nodes.ibf"
    output:
        "data/sim_seq/{NODES}_sim.fasta"
    params:
        in_path=os.getcwd() + "/" + "data/matrix/{NODES}_nodes.ibf",
        out_path=os.getcwd()+ "/" +  "data/sim_seq/{NODES}_sim.fasta"
    shell:
        "HYPHYMP simulate/SimulateSequence.bf {params.in_path} > {params.out_path}"

## this rule will take the generated fasta files and input them into HIVtrace 
rule hiv_trace:
    input:
        "data/sim_seq/{NODES}_sim.fasta"
    output:
        "data/hivtrace/{NODES}_nodes.results.json"
    shell:
        # this is giving me an odd error message, CalledProcessError ?? is this a me or hivtrace thing? #
        "hivtrace -i {input} -a resolve -f remove -r HXB2_prrt -t .015 -m 500 -g .05 -o {output}"

## this rule will take the generated fasta files and input them into HIVtrace 
rule hiv_trace_without_edge:
    input:
        "data/sim_seq/{NODES}_sim.fasta"
    output:
        "data/hivtrace/{NODES}_nodes.nofilter.results.json"
    shell:
        # this is giving me an odd error message, CalledProcessError ?? is this a me or hivtrace thing? #
        "hivtrace -i {input} -a resolve -r HXB2_prrt -t .015 -m 500 -g .05 -o {output}"

rule generate_edge_report:
    input:
        results=expand("data/hivtrace/{nodes}_nodes.results.json", nodes=NODES)
    params:
        transmission_chains=[matrix_maker(INTERNAL_LENGTH,TIP_LENGTH,n) for n in NODES]
    output:
        expand("data/hivtrace/{nodes}_edge_report.json", nodes=NODES)
    run:
        pairs = zip(input.results, params.transmission_chains, output)
        for p in pairs:
            edge_report(*p)

