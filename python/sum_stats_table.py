'''
want to: 
    1. expand on the input, read in a list of the reports
    2. from each file:
        a. total number of nodes
        b. total number of egdes created from network
        c. grab number of edges removed
        d. number of wrongfully purged edges
        e. number of spurious edges still remaining
    3. make a graph that shows 
'''

import json
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
import pandas as pd
from itertools import islice

def sum_stats_table(input, output, sims):
    #print(list(input))

    # this is to separate all the sizes into proper lists
    # I will now have a list of list where the sub list
    # is made up of the same size networks
    def chunk(lst, chunk_size):
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i+ chunk_size]
    
    chunked = list(chunk(input,sims))

    avg_FNR = []
    avg_FPR = []
    avg_TPR = []
    avg_TNR = []
    avg_ER = []

    nodes = []
    for sublist in chunked:
        total_edges_before_filter = []
        current_edges = []
        edges_removed = []
        wrongfully_purged_edges = []
        spurious_still_remaining = []
        true_negatives = []
        for file in sublist:
            #print(file)
            with open(file) as f:
                data = json.load(f)
            #pprint(data)
            nodes.append(data['num_nodes'])
            total_edges_before_filter.append(int(data['num_edges']) + int(data['num_edges_removed']))
            current_edges.append(int(data['num_edges']))
            edges_removed.append(int(data['num_edges_removed']))
            wrongfully_purged_edges.append(len(list(data['wrongfully_purged_edges'])))
            true_negatives.append(len(list(data['true_negatives'])))
            if not 'spurious_edges' in data:
                spurious_still_remaining.append(0)
            else:
                spurious_still_remaining.append(len(data['spurious_edges']))
    
        TP = edges_removed
        ER_avg = sum(edges_removed)/len(edges_removed)
        FN = spurious_still_remaining
        FNR = [int(a) / (int(a) + int(b)) for a,b in zip(FN, TP)]
    
        # FPR = FP/ (FP + TN)
        FP = wrongfully_purged_edges
        TN = true_negatives
        FPR = []
        lines = zip(FP, TN)
        for line in lines:
            if line[0] == 0:
                FPR.append(0)
            else:
                FPR.append(line[0]/ (line[0] + line[1]))
        TPR = [(1-i) for i in FNR]
        TPR_avg = sum(TPR)/len(TPR)
        TNR = [(1-i) for i in FPR]
        TNR_avg = sum(TNR)/len(TNR)
        
        avg_FNR.append(sum(FNR)/len(FNR))
        avg_FPR.append(sum(FPR)/len(FPR))
        avg_TPR.append(sum(TPR)/len(TPR))
        avg_TNR.append(sum(TNR)/len(TNR))
        avg_ER.append(sum(edges_removed)/len(edges_removed))

    

    list_nodes = list(set(nodes))
    NM1 = [i-1 for i in list_nodes]
    max_con = [(i*(i-1))/2 for i in list_nodes]

    table_vals = np.array((avg_FNR, avg_FPR, avg_TNR, avg_TPR, avg_ER, NM1, max_con ), dtype=None)
    table = pd.DataFrame(table_vals, index=['avg_FNR','avg_FPR','avg_TNR','avg_TPR', 'avg_ER','NM1','max_con'])
    
    table.columns = list_nodes
    table.to_csv(str(output))
    #total_nodes_index = [pos for pos, item in enumerate(total_nodes)]


