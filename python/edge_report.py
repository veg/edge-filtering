import json

def generate_edge_report(test_filter_results, no_filter_results, transmission_chain):

    report = {}

    # How many clusters are there?
    num_clusters = len(test_filter_results["Cluster sizes"])

    num_edges = test_filter_results["Network Summary"]["Edges"]
    num_nodes = test_filter_results["Network Summary"]["Nodes"]

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

    edges = [tuple(e["sequences"]) for e in test_filter_results["Edges"]]
    flipped_edges = [tuple(reversed(e)) for e in edges]

    expected_edges = list(zip(transmission_chain["Source Node"], transmission_chain["Node ID"]))
    flipped_expected_edges = list(zip(transmission_chain["Node ID"], transmission_chain["Source Node"]))
    expected_edges = filter(lambda x: x[0] != -1, expected_edges)
    flipped_expected_edges = filter(lambda x: x[1] != -1, flipped_expected_edges)
    expected_edges = [('N' + str(x[0]), 'N' + str(x[1])) for x in expected_edges]
    flipped_expected_edges = [('N' + str(x[0]), 'N' + str(x[1])) for x in flipped_expected_edges]


    ## this will gather our true positives ##
    report['true_negatives'] = [e for e in edges if e in expected_edges or e in flipped_expected_edges]

    ## False positives ##
    report["spurious_edges"] = [e for e in edges if e not in expected_edges and e not in flipped_expected_edges]

    ## Remember this is the False Negative!! ##
    wrongfully_purged = [e for e in expected_edges if e not in edges and e not in flipped_edges]

    report['wrongfully_purged_edges'] = wrongfully_purged

    # Edges in hivtrace results match what is expected
    report['edges_equals_expected'] = (len(report['spurious_edges']) + len(report['wrongfully_purged_edges']) == 0)

    return report

def edge_report(results_json, no_filter_json, cycle_json, cycle_report, transmission_chain, output_fn):

    ## has been filtered ##
    results = ''

    ## has NOT been filtered ##
    no_filter_results = ''

    with open(results_json) as f:
        results = json.loads(f.read())

    with open(no_filter_json) as f:
        no_filter_results = json.loads(f.read())

    with open(cycle_json) as f:
        filter_cycle_results = json.loads(f.read())

    # Only read the first line of the cycle report
    with open(cycle_report) as f:
        cycle_report = json.loads(f.readline())

    results = results["trace_results"]
    no_filter_results = no_filter_results["trace_results"]
    filter_cycle_results = filter_cycle_results["trace_results"]

    report = {}
    report['filter-report'] = generate_edge_report(results, no_filter_results, transmission_chain)

    report['cycles'] = cycle_report['cycles']
    report['cycle-report'] = generate_edge_report(filter_cycle_results, no_filter_results, transmission_chain)

    with open(output_fn, 'w') as jsonfile:
        json.dump(report, jsonfile)

    return

