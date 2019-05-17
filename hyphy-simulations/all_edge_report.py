import json
import glob
import os
import itertools
import numpy as np

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

def consolidate_replicates(files):
    report = {}

    report['reps'] = [ get_json(files[i]) for i in range(len(files)) ]

    report['avg-edges-removed'] = np.mean([f['filter-report']['num_edges_removed'] for f in report['reps']])
    report['std-edges-removed'] = np.std([f['filter-report']['num_edges_removed'] for f in report['reps']])

    report['avg-cycles-removed'] = np.mean([f['cycle-report']['num_edges_removed'] for f in report['reps']])
    report['std-cycles-removed'] = np.std([f['cycle-report']['num_edges_removed'] for f in report['reps']])

    report['avg-spurious'] = np.mean([len(f['filter-report']['spurious_edges']) for f in report['reps']])
    report['std-spurious'] = np.std([len(f['filter-report']['spurious_edges']) for f in report['reps']])

    report['avg-cycle-spurious'] = np.mean([len(f['cycle-report']['spurious_edges']) for f in report['reps']])
    report['std-cycle-spurious'] = np.std([len(f['cycle-report']['spurious_edges']) for f in report['reps']])

    report['avg-wrongfully-purged'] = np.mean([len(f['filter-report']['wrongfully_purged_edges']) for f in report['reps']])
    report['std-wrongfully-purged'] = np.std([len(f['filter-report']['wrongfully_purged_edges']) for f in report['reps']])

    report['avg-cycle-wrongfully-purged'] = np.mean([len(f['cycle-report']['wrongfully_purged_edges']) for f in report['reps']])
    report['std-cycle-wrongfully-purged'] = np.std([len(f['cycle-report']['wrongfully_purged_edges']) for f in report['reps']])


    return report

def get_all_chain_reports():
    return glob.glob("./p*/data/hivtrace/8*edge_report.json")

if __name__ == "__main__":

    report_files = get_all_chain_reports()
    report_files = sorted(report_files, key=os.path.basename)

    groups = []
    uniquekeys = []

    for k, g in itertools.groupby(report_files, os.path.basename):
        groups.append(list(g))      # Store group iterator as a list
        uniquekeys.append('_'.join(k.split('_')[0:4]))

    grouped = list(zip(uniquekeys,groups))

    reports = {}
    for k,g in grouped:
        reports[k] = consolidate_replicates(g)

    with open('all-report.json', 'w') as jsonfile:
        json.dump(reports, jsonfile)

