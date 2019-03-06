## import all functions from python ## 
from python.temp import *
from python.edge_report import edge_report, consolidate_edge_reports
from python.sum_stats_table import sum_stats_table
from python.graph import sum_stats_graph
import itertools
import os
#import json

shell.prefix("source /home/sweaver/programming/hivtrace/edge/bin/activate;module load aocc/1.2.1;export PATH=/usr/local/bin:$PATH; ")

# size of the networks to create #
network_sizes = list(range(3, 21))
#network_sizes = list([20])

# Evolution parameters #
    #within host Ev #
TIP_LENGTH = 0
    #between host Ev #
INTERNAL_LENGTH = 0.05
FORMAT = "hyphy"

# number of simulations #
sims = 10
number_of_sims = [[i]*sims for i in network_sizes]
flatten = [j for i in number_of_sims for j in i]

INDEX = []
for i in number_of_sims:
    for pos, item in enumerate(i):
        INDEX.append(str(pos))

PAIRS = list(zip(flatten,INDEX))
temp = [str(p[0])+'_'+p[1] for p in PAIRS]



rule all: 
    params: 
        runtime="5:00:00"
    input:        
        "data/summary_statistics_FDR_graph.png",
        "data/summary_statistics_TDR_graph.png",
        "data/summary_statistics_funnel_graph.png",
        "data/summary_statistics_sqrt_funnel_graph.png",
        "data/all_edge_report.json"
        #"data/summary_statistics_table.csv"


## this rule that will use the python script to make and write matrices to .ibf files ## 
rule matrix_for_BF:
    params: 
        temp=temp,
        runtime="5:00:00"
    output: 
        expand(os.path.join(os.getcwd(),"data/matrix/{temp}_nodes.ibf"), temp=temp)
    group:"matrix_generation"
    run:
        #import pdb; pdb.set_trace()
        for pair in zip(params.temp,output):
            node = pair[0].split('_')[0]
            output_fn = pair[1]
            edge_creator(INTERNAL_LENGTH, TIP_LENGTH, node, FORMAT, output_fn)

## this rule will take the matrices and input them into the sim_seq.bf to make fasta files ##
rule seq_gen:
    params:
        runtime="5:00:00"
    input:
        os.path.join(os.getcwd(), "data/matrix/{temp}_nodes.ibf")
    output:
        "data/sim_seq/{temp}_sim.fasta"
    group:"matrix_generation"
    shell:  
        "HYPHYMP simulate/SimulateSequence.bf {input} > {output}"


## this rule will take the generated fasta files and input them into HIVtrace 
rule hiv_trace_with_edge_filtering:
    params:
        runtime="5:00:00"
    input:
        rules.seq_gen.output
    output:
        "data/hivtrace/{temp}_nodes.results.json"
    group:"hivtrace"
    shell:
        "hivtrace --do-not-store-intermediate -i {input} -a resolve -f remove -r HXB2_prrt -t .015 -m 500 -g .05 -o {output}"

## this rule will take the generated fasta files and input them into HIVtrace 
rule hiv_trace_without_edge_filtering:
    params:
        runtime="5:00:00"
    input:
        rules.seq_gen.output
    output:
        "data/hivtrace/{temp}_nodes.nofilter.results.json"
    group:"hivtrace"
    shell:
        "hivtrace --do-not-store-intermediate -i {input} -a resolve -r HXB2_prrt -t .015 -m 500 -g .05 -o {output}"

## this rule will take the generated fasta files and input them into HIVtrace 
rule hiv_trace_with_cycle_filtering:
    params:
        runtime="5:00:00"
    input:
        rules.seq_gen.output
    output:
        "data/hivtrace/{temp}_nodes.cycle.results.json", "data/hivtrace/{temp}_nodes.cycle_report.json"
    group:"hivtrace"
    shell:
        "hivtrace --do-not-store-intermediate -i {input} -a resolve -f remove -r HXB2_prrt -t .015 -m 500 -g .05 -o {output[0]} --filter-cycles --cycle-report-fn {output[1]}"


rule generate_edge_report:
    params:
        runtime="5:00:00"
    input:
        with_edge_filtering=rules.hiv_trace_with_edge_filtering.output,
        with_out_edge_filtering=rules.hiv_trace_without_edge_filtering.output,
        with_cycle_filtering=rules.hiv_trace_with_cycle_filtering.output
    output:
        "data/hivtrace/{temp}_edge_report.json"
    group:"report"
    run:
        transmission_chains=[matrix_maker(INTERNAL_LENGTH,TIP_LENGTH,int(n.split('/')[2].split('_')[0])) for n in input.with_edge_filtering]
        pairs = zip(input.with_edge_filtering, input.with_out_edge_filtering, [input.with_cycle_filtering[0]], [input.with_cycle_filtering[1]], transmission_chains, output)
        for p in pairs:
            edge_report(*p)


# rule emvolz_sim:
#     input:
#         "londonMSM_tree_simulator/model1.R"        
#     output:

#     script:
#         "{input}"

## this rule consumes all the edge reports and creates a table with all the info ##
rule generate_all_edge_report:
    params:
        runtime="5:00:00"
    input:
        expand("data/hivtrace/{temp}_edge_report.json", temp=temp)
    output:
        "data/all_edge_report.json"
    group:"report"
    run:
        consolidate_edge_reports(temp, input, output[0])

rule summary_stats_table:
    params:
        runtime="5:00:00"
    input:
        expand("data/hivtrace/{temp}_edge_report.json", temp=temp)
    output:
        "data/summary_statistics_table.csv"
    group:"report"
    run:
        sum_stats_table(input, output, sims)

## this rule consumes all the edge reports and creates FDR, TDR, and funnel graphs with all the info ##
rule summary_stats_graph:
    params:
        runtime="5:00:00"
    input:
        rules.summary_stats_table.output
    output:
        "data/summary_statistics_FDR_graph.png",
        "data/summary_statistics_TDR_graph.png",
        "data/summary_statistics_funnel_graph.png",
        "data/summary_statistics_sqrt_funnel_graph.png"
    group:"report"
    run:
        sum_stats_graph(input, output[0], output[1], output[2], output[3], sims, TIP_LENGTH, INTERNAL_LENGTH)

