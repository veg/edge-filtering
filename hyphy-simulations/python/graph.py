## graphs from the CSVs ##

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import math

def sum_stats_graph(input, output1, output2, output3, output4, sims, tip_length, internal_length):
    master_file = str(input)

    frame = pd.read_csv(master_file, index_col=0)

    #print(frame)

    d = frame.values.tolist()


    FNR = d[0]
    FPR = d[1]
    TNR = d[2]
    TPR = d[3]
    avg_er = d[4]
    sq_er = [math.sqrt(i) for i in avg_er]
    NM1 = d[5]
    sq_NM1 = [math.sqrt(i) for i in NM1]
    max_con = d[6]
    sq_max = [math.sqrt(i) for i in max_con]

    nodes = frame.columns.values.tolist()

    ## want to plot FDR ##
    # need Y- (FNR, FPR) X- (nodes) 
    plt.figure(0)
    plt.title('FDR, %s sims/Network, Within Host: %s, Between Host: %s'  % (sims, tip_length, internal_length))
    plt.scatter(nodes, FNR, label='FNR (spurious edges remaining)')
    plt.scatter(nodes, FPR, label='FPR (wrongfully purged edges)')
    plt.xticks(nodes, rotation=60)
    plt.xlabel('Nodes in the Network')
    plt.ylabel('False Discovery Rate')
    plt.legend(loc='upper left')
    plt.tick_params(axis='x', labelsize=6)
    plt.savefig(str(output1))


    ## want to plot TDR ##
    # need Y- (TNR, TPR) X- (nodes)
    plt.figure(1)
    plt.title('TDR, %s sims/Network, Within Host: %s, Between Host: %s'  % (sims, tip_length, internal_length))
    plt.scatter(nodes, TNR, label='TNR (only true CT)')
    plt.scatter(nodes, TPR, label='TPR (edges removed)')
    plt.xticks(nodes, rotation=60)
    plt.xlabel('Nodes in the Network')
    plt.ylabel('True Discovery Rate')
    plt.legend(loc='upper left')
    plt.tick_params(axis='x', labelsize=6)
    plt.savefig(str(output2))

    ## funnel graph ##
    # need Y- (Max Connectedness, Avg_Edges_removed, N-1) X- (nodes)
    plt.figure(2)
    plt.title('Funnel, %s sims/Network, Within Host: %s, Between Host: %s'  % (sims, tip_length, internal_length))
    plt.scatter(nodes, max_con, label='Max Connectedness' )
    plt.scatter(nodes, avg_er, label='Avg. Edges Removed')
    plt.scatter(nodes, NM1, label='True Chain Transmission # Edges')
    plt.xticks(nodes, rotation=60)
    plt.xlabel('Nodes in the Network')
    plt.ylabel('Sqrt Edges')
    plt.legend(loc='upper left')
    plt.tick_params(axis='x', labelsize=6)
    plt.savefig(str(output3))

    ## sqrt funnel graph ##
    plt.figure(3)
    plt.title('SQRT Funnel, %s sims/Network, Within Host: %s, Between Host: %s'  % (sims, tip_length, internal_length))
    plt.scatter(nodes, sq_max, label='Max Connectedness' )
    plt.scatter(nodes, sq_er, label='Avg. Edges Removed')
    plt.scatter(nodes, sq_NM1, label='True Chain Transmission # Edges')
    plt.xticks(nodes, rotation=60)
    plt.xlabel('Nodes in the Network')
    plt.ylabel('Sqrt Edges')
    plt.legend(loc='upper left')
    plt.tick_params(axis='x', labelsize=6)
    plt.savefig(str(output4))






