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
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
import pandas as pd

def sum_stats(input, output1, output2, output3, output4):
    #print(type(output))
    flatten = [j for i in input for j in i]
    #print(flatten)
    total_nodes = []
    total_edges_before_filter = []
    current_edges = []
    edges_removed = []
    wrongfully_purged_edges = []
    spurious_still_remaining = []
    true_negatives = []
    for file in flatten:
        with open(file) as f:
            data = json.load(f)
        #pprint(data)
        total_nodes.append(data['num_nodes'])
        total_edges_before_filter.append(int(data['num_edges']) + int(data['num_edges_removed']))
        current_edges.append(int(data['num_edges']))
        edges_removed.append(int(data['num_edges_removed']))
        wrongfully_purged_edges.append(len(list(data['wrongfully_purged_edges'])))
        true_negatives.append(len(list(data['true_negatives'])))
        if not 'spurious_edges' in data:
            spurious_still_remaining.append(0)
        else:
            spurious_still_remaining.append(len(data['spurious_edges']))

    
    total_nodes_index = [pos for pos, item in enumerate(total_nodes)]

    # separate plot to show percentage of nodes removed for each network #
        # save as its own plot #
    edge_removal_percentage = [100*(int(a) / int(b)) for a,b in zip(edges_removed, total_edges_before_filter)]
    percent_avg = sum(edge_removal_percentage)/len(edge_removal_percentage)
    percent_avg = round(percent_avg, 2)
    print('this is for networks of 10 ' + str(percent_avg))

    plt.figure(0)
    plt.scatter(total_nodes_index, edge_removal_percentage)
    plt.xticks(total_nodes_index, rotation=60)
    plt.xlabel('Nodes in the Network')
    plt.ylabel('Percent Edges Removed %')
    plt.tick_params(axis='x', labelsize=6)
    #plt.plot(np.unique(total_nodes), np.poly1d(np.polyfit(total_nodes, edge_removal_percentage, 1))(np.unique(total_nodes)))
    plt.text(1, 55, 'average % edge removal is: ' +str(round(percent_avg,2)))
    plt.savefig(str(output1))

    
    # this is the FALSE discovery rate plot #
        # save as its own plot #

    # FNR = FN / (FN + TP)
    TP = edges_removed
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

    FNR_avg = sum(FNR)/len(FNR)
    plt.figure(1)
    plt.scatter(total_nodes_index, FNR, label='FNR (spurious edges remaining')
    plt.scatter(total_nodes_index, FPR, label='FPR (wrongfully purged edges')
    plt.xticks(total_nodes_index, rotation=60)
    plt.tick_params(axis='x', labelsize=6)
    plt.xlabel('Nodes in the Network')
    plt.ylabel('False Discovery Rates')
    plt.legend(loc='upper left')
    plt.text(0, .01, 'average % FNR: ' +str(round(FNR_avg,2)))
    plt.savefig(str(output2))

    # this is the TRUE discovery rate plot #
        # save aas its own plot #
    
    # TPR = 1- FNR
    # TNR = 1- FPR
    TPR = [(1-i) for i in FNR]
    TNR = [(1-i) for i in FPR]
    plt.figure(2)
    plt.scatter(total_nodes_index, TNR, label='TNR (only true CT)')
    plt.scatter(total_nodes_index, TPR, label='TPR (edges removed)')
    plt.xticks(total_nodes_index, rotation=60)
    plt.tick_params(axis='x', labelsize=6)
    plt.xlabel('Nodes in the Network')
    plt.ylabel('True Discovery Rates')
    #plt.text(0, .01, 'average % edge removal is: ' +str(FNR_avg) + '%')
    plt.legend(loc='upper left')
    plt.savefig(str(output3)) 
    
    ## table of the values in CVS output ##
    table_vals = np.array((edge_removal_percentage, FN, FNR, FP, FPR, TPR, TNR), dtype=None)
    table = pd.DataFrame(table_vals, index=['Edge Percent', 'Spurious Remaining', 'FNR', 'Wrongfully Purged','FPR', 'TPR (edges removed)', 'TNR (only true CT)'])
    table.columns = total_nodes_index
    table.to_csv(str(output4))



