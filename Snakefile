## import all functions from python ## 
from python.temp import *
from python.edge_report import edge_report
import itertools
import os


#NODES = list(itertools.repeat("10", 10))
NODES = ["10", "50", "100", "200", "500", "1000"]
INDEX = [str(pos) for pos, item in enumerate(NODES)]
PAIRS = list(zip(NODES,INDEX))

temp = [p[0]+'_'+p[1] for p in PAIRS]

INTERNAL_LENGTH = 0.005
TIP_LENGTH = 0
FORMAT = "hyphy"

# def expand_all(*args, **wildcards):
#     return expand("data/hivtrace/{node}_nodes.results.json", node=wildcards["node"]) + expand("data/hivtrace/{node}_nodes.nofilter.results.json",node=wildcards["node"])

rule all: 
    input: expand("data/hivtrace/{temp}_edge_report.json", temp=temp)
    #input: expand_all("", node=NODES)

## this rule that will use the python script to make and write matrices to .ibf files ## 
rule matrix_for_BF:
    params: 
        temp=temp
    output: 
        expand("data/matrix/{temp}_nodes.ibf", temp=temp)
    run:
        for pair in zip(params.temp,output):
            node = pair[0].split('_')[0]
            output_fn = pair[1]
            edge_creator(INTERNAL_LENGTH, TIP_LENGTH, node, FORMAT, output_fn)

## this rule will take the matrices and input them into the sim_seq.bf to make fasta files ##
rule seq_gen:
    input:
        os.path.join(os.getcwd(), "data/matrix/{temp}_nodes.ibf")
    output:
        "data/sim_seq/{temp}_sim.fasta"
    shell:  
        "HYPHYMP simulate/SimulateSequence.bf {input} > {output}"


## this rule will take the generated fasta files and input them into HIVtrace 
rule hiv_trace:
    input:
        rules.seq_gen.output
    output:
        "data/hivtrace/{temp}_nodes.results.json"
    shell:
        "hivtrace -i {input} -a resolve -f remove -r HXB2_prrt -t .015 -m 500 -g .05 -o {output}"

## this rule will take the generated fasta files and input them into HIVtrace 
rule hiv_trace_without_edge:
    input:
        rules.seq_gen.output
    output:
        "data/hivtrace/{temp}_nodes.nofilter.results.json"
    shell:
        "hivtrace -i {input} -a resolve -r HXB2_prrt -t .015 -m 500 -g .05 -o {output}"

rule generate_edge_report:
    input:
        wit=rules.hiv_trace.output,
        wit_oot=rules.hiv_trace_without_edge.output
    output:
        "data/hivtrace/{temp}_edge_report.json"
    run:
        transmission_chains=[matrix_maker(INTERNAL_LENGTH,TIP_LENGTH,int(n.split('/')[2].split('_')[0])) for n in input.wit]
        pairs = zip(input.wit, input.wit_oot, transmission_chains, output)
        for p in pairs:
            edge_report(*p)

