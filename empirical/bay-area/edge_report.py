import json

def get_json(fn):
    with open(fn) as f:
        return json.loads(f.read())

def consolidate_edge_reports(pairs, input, output):

    report = {}
    # for each edge report, create key based on filename
    for pair, fn in zip(pairs, input):
        report[pair] = get_json(fn)

    with open(output, 'w') as jsonfile:
        json.dump(report, jsonfile)

    return

def generate_edge_report(test_filter_results, no_filter_results, transmission_chain):

    report = {}

    # How many clusters are there?
    num_clusters = len(test_filter_results["Cluster sizes"])

    num_edges = test_filter_results["Network Summary"]["Edges"]
    num_nodes = test_filter_results["Network Summary"]["Nodes"]

    report['num_edges'] = num_edges
    report['num_nodes'] = num_nodes
    report['num_edges_removed'] = num_edges_removed

    edges = [tuple(e["sequences"]) for e in test_filter_results["Edges"]]
    flipped_edges = [tuple(reversed(e)) for e in edges]

    return report

def edge_report(results_json, no_filter_json, cycle_json, cycle_report, output_fn):

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

