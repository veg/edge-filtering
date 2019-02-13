import json

def edge_report(results_json, transmission_chain, output_fn):

    results = ''

    with open(results_json) as f:
        results = json.loads(f.read())

    results = results["trace_results"]

    report = {}

    # How many clusters are there?
    num_clusters = len(results["Cluster sizes"])

    # How many edges are there?
    num_edges = results["Network Summary"]["Edges"]
    num_nodes = results["Network Summary"]["Nodes"]

    report['num_edges'] = num_edges
    report['num_nodes'] = num_nodes

    # Do the number of edges equal N - 1?
    expected_num_edges = (num_nodes - num_edges) == 1
    report['meets_edge_count_expectations'] = expected_num_edges

    edges = [tuple(e["sequences"]) for e in results["Edges"]]

    expected_edges = list(zip(transmission_chain["Source Node"], transmission_chain["Node ID"]))
    expected_edges = filter(lambda x: x[0] != -1, expected_edges)
    expected_edges = [('N' + str(x[0]), 'N' + str(x[1])) for x in expected_edges]

    # Edges in hivtrace results match what is expected
    report['edges_equals_expected'] = edges == expected_edges

    if not report['edges_equals_expected']:
        report["spurious_edges"] = [e for e in edges if e not in expected_edges]

    with open(output_fn, 'w') as jsonfile:
        json.dump(report, jsonfile)

    return

