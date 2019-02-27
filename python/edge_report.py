import json

def edge_report(results_json, no_filter_json, transmission_chain, output_fn):

    ## has been filtered ##
    results = ''
    
    ## has NOT been filtered ##
    no_filter_results = ''

    with open(results_json) as f:
        results = json.loads(f.read())

    with open(no_filter_json) as f:
        no_filter_results = json.loads(f.read())


    results = results["trace_results"]
    no_filter_results = no_filter_results["trace_results"]

    report = {}

    # How many clusters are there?
    num_clusters = len(results["Cluster sizes"])

    # How many edges are there?
    ## from our filtered results how many edges are left ##
    num_edges = results["Network Summary"]["Edges"]
    num_nodes = results["Network Summary"]["Nodes"]

    ## this IS the number of edges removed BY edge filtering, 
    ## but NOT the true number of total edges that should have been removed...
    ## ... if we were to compare back to the original TRUTH of the CT

    ## so FP = edges that WERE removed PLUS spurious edges that still persist.
    ## because both of these types of edges WERE NOT in the original CT.
    num_edges_removed = no_filter_results["Network Summary"]["Edges"] - num_edges

    report['num_edges'] = num_edges
    report['num_nodes'] = num_nodes
    report['num_edges_removed'] = num_edges_removed


    ## this is where the true positives would be ##
    # Do the number of edges equal N - 1?
    expected_num_edges = (num_nodes - num_edges) == 1
    report['meets_edge_count_expectations'] = expected_num_edges

    edges = [tuple(e["sequences"]) for e in results["Edges"]]

    expected_edges = list(zip(transmission_chain["Source Node"], transmission_chain["Node ID"]))
    expected_edges = filter(lambda x: x[0] != -1, expected_edges)
    expected_edges = [('N' + str(x[0]), 'N' + str(x[1])) for x in expected_edges]

    ## this will gather our true positives ##
    report['true_negatives'] = [e for e in edges if e in expected_edges]

    # Edges in hivtrace results match what is expected
    report['edges_equals_expected'] = edges == expected_edges

    if not report['edges_equals_expected']:
        ## False positives ##
        report["spurious_edges"] = [e for e in edges if e not in expected_edges]

    ## Remember this is the False Negative!! ## 
    wrongfully_purged = [e for e in expected_edges if e not in edges]

    report['wrongfully_purged_edges'] = wrongfully_purged

    with open(output_fn, 'w') as jsonfile:
        json.dump(report, jsonfile)

    return

